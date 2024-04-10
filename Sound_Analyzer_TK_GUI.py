###Sound_Analyzer_TK_GUI
from tkinter import filedialog
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pyaudio
import wave
import time
from scipy.signal import periodogram
from scipy.signal import stft

class Sound_Analyzer_App(ctk.CTk):
    CHUNK = 512
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 11025
    RECORD_SECONDS = 30
    rec_fname=""
    read_fname=""
    
    def __init__(self):
        super().__init__()
        self.wav=np.zeros(self.CHUNK)
        self.title('SONIO analyzer')
        self.geometry('1200x800')

        # Create a frame to hold everything
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Container for plots
        self.plots_frame = ctk.CTkFrame(self.main_frame)
        self.plots_frame.pack(pady=10, padx=10, fill='both', expand=True)

        # Create a frame for controls at the bottom
        self.controls_frame = ctk.CTkFrame(self.main_frame)
        self.controls_frame.pack(side='bottom',fill="x", padx=10, pady=10)

        #-----------------------------------------------------------------------
        # Create figure and axis for the left and right plot
        self.fig_left, (self.ax_left,self.ax_right) = plt.subplots(1, 2, figsize=(12, 4))
        self.canvas = FigureCanvasTkAgg(self.fig_left, master=self.plots_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack( expand=True)

        #-----------------------------------------------------------------------
        # Label and input for starting range
        self.label_range_start = ctk.CTkLabel(master=self.controls_frame, text="Start time:")
        self.label_range_start.grid(row=0, column=0, pady=4, padx=(0, 2))
        self.txt_start_time = ctk.CTkEntry(master=self.controls_frame, placeholder_text="Start time", width=120)
        self.txt_start_time.grid(row=0, column=1, pady=4, padx=(0, 2))

        # Label and input for ending range
        self.label_range_end = ctk.CTkLabel(master=self.controls_frame, text="Stop Time:")
        self.label_range_end.grid(row=1, column=0, pady=4, padx=(0, 2))
        self.txt_stop_time = ctk.CTkEntry(master=self.controls_frame, placeholder_text="Stop time", width=120)
        self.txt_stop_time.grid(row=1, column=1, pady=4, padx=(0, 2))

        # Button to update the plots
        self.update_button = ctk.CTkButton(master=self.controls_frame, text='Update Plots', command=self.update_plots)
        self.update_button.grid(row=0, column=2, pady=4, padx=(0, 2))

        # Button to open the file dialog
        self.open_file_button = ctk.CTkButton(master=self.controls_frame, text='Open File', command=self.open_file_dialog)
        self.open_file_button.grid(row=2, column=2, pady=4, padx=(0, 2))
        self.file_path_label = ctk.CTkLabel(master=self.controls_frame, text='File path will appear here')
        self.file_path_label.grid(row=2, column=0,columnspan=2, pady=4, padx=(0, 2))

        # Label to display the record file name and button
        self.rec_filename_label = ctk.CTkLabel(master=self.controls_frame, text='File name for recording')
        self.rec_filename_label.grid(row=3, column=0, pady=4, padx=(0, 2))
        self.rec_filename_input = ctk.CTkEntry(master=self.controls_frame, placeholder_text="test.wav", width=240)
        self.rec_filename_input.grid(row=3, column=1, pady=4, padx=(0, 2))
        self.update_button = ctk.CTkButton(master=self.controls_frame, text='RECORD', command=self.record_file)
        self.update_button.grid(row=3, column=2, pady=4, padx=(0, 2))
        
        # Initial plots
        x = np.linspace(0, 2 * np.pi, 100)
        y = np.sin(x)
        self.ax_left.plot(x, y)
        self.ax_left.set_title("Time domain")
        self.canvas.draw()

        fig_right, ax_right = plt.subplots()
        data = np.random.rand(10, 10)
        im = self.ax_right.imshow(data, cmap="viridis")
        self.ax_right.set_title("Spectrogram")
        #self.fig_right.colorbar(im, ax=self.ax_right)
        self.canvas.draw()

    def record_file(self):
    # Initialize PyAudio
        p = pyaudio.PyAudio()

    # Open stream
        stream = p.open(format=self.FORMAT,
                    channels=self.CHANNELS,
                    rate=self.RATE,
                    input=True,
                    frames_per_buffer=self.CHUNK)

        print("Listening...")

        frames = []
        start=False
        MAX_RECORD_SECONDS = self.RECORD_SECONDS
        stop_time=time.time()
        # Record for RECORD_SECONDS
        
        data = stream.read(self.CHUNK)
        nd=np.frombuffer(data, dtype=np.int16)
        maxd=np.max(nd)
        #frequencies, power_spectrum = periodogram(nd, fs=RATE)
        #            print(maxd)
        start=True
        stop_time=time.time()+10
        print("Start recording.")
        frames=[]
        while time.time()<stop_time:
            data = stream.read(self.CHUNK)
            print(stop_time-time.time())
            frames.append(data)

            print("Finished recording.")

        # Stop and close the stream
        stream.stop_stream()
        stream.close()
    
        print("Writting to file")
        bytestream = b''.join(frames)
        print("Len=",len(bytestream))
        with wave.open(fname, 'wb') as wf:
                wf.setnchannels(self.CHANNELS)
                wf.setframerate(self.RATE)
                wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
                wf.writeframes(bytestream)
                wf.close()
        print("Finished writting to file")


    def open_file_dialog(self):
        # Open the file dialog and get the selected file path
        file_path = filedialog.askopenfilename(title='Select a file',
                                               filetypes=(("Wave files", "*.wav*"), ("All files", "*.*")))
        # Update the label with the selected file path
        if file_path:  # If a file was selected
            self.file_path_label.configure(text=file_path)
            self.read_fname=file_path
            self.read_file()
        else:
            self.file_path_label.configure(text='No file selected')

    def read_file(self):
        wf = wave.open(self.read_fname, 'rb')
        # Read audio in chunks
        data = wf.readframes(self.CHUNK)
        wave_data=[]
        data_list=[]
        # Create scatter plot
        while data:
            wave_data=np.frombuffer(data, dtype=np.int16)
            
            data = wf.readframes(self.CHUNK)

            #print(len(wave_data))
            if len(wave_data)==self.CHUNK:
                print(len(data_list),np.max(wave_data))
                data_list.append(wave_data)
        self.wav=np.concatenate(data_list)
        self.txt_start_time.delete(0,ctk.END)
        self.txt_start_time.insert(0,str(0))
        self.txt_stop_time.delete(0,ctk.END)
        self.txt_stop_time.insert(0,"{:.3f}".format(len(self.wav)/self.RATE))
        self.update_plots()

    def update_plots(self):
    #update left plot
        left_lim=int(float(self.txt_start_time.get())*self.RATE)
        right_lim=int(float(self.txt_stop_time.get())*self.RATE)
        wav=self.wav[left_lim:right_lim]
        self.ax_left.clear()
        self.ax_right.clear()
        if len(self.wav)>self.CHUNK:
            x = np.linspace(1, len(wav)/self.RATE,len(wav))
            y = wav
            self.ax_left.plot(x, y)
            self.ax_left.set_title("Time domain")
            
    #update right plot
            f, t, Zxx = stft(self.wav, self.RATE, nperseg=500)  # nperseg determines the size of the window
            # Plot 
            # data = np.random.rand(200, 200)
            # self.ax_right.pcolormesh(data, cmap="viridis")
            # self.ax_right.set_title("Pcolormesh")
            # self.ax_right.set_aspect("equal")
            im = self.ax_right.pcolormesh(t, f, np.abs(Zxx), shading='gouraud')  # Use absolute value of Zxx
            self.ax_right.set_aspect('auto', adjustable='datalim')
            self.ax_right.set_title("Spectrogram")
            self.ax_right.axhline(y=0, color='red', linewidth=1.5, linestyle='--')
            
            self.canvas.draw()
        else:
            data = np.random.rand(10, 10)
            im = self.ax_right.imshow(data, cmap="viridis")
            self.ax_right.set_title("Random")
            #self.fig_right.colorbar(im, ax=self.ax_right)
        self.canvas.draw()

if __name__ == '__main__':
    app = Sound_Analyzer_App()
    app.mainloop()
