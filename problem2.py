import pyaudio
import wave
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.signal import periodogram
import time 

def plot_audio(filename):
    wf = wave.open(filename, 'rb')
    # Read audio in chunks
    data = wf.readframes(CHUNK)
    wave_data=[]
    PSdata_list=[]
    # Create scatter plot
    while data:
        wave_data=np.frombuffer(data, dtype=np.int16)
        #stream.write(data)
        data = wf.readframes(CHUNK)
        frequencies, power_spectrum = periodogram(wave_data, fs=RATE,scaling="spectrum")
        #print(len(wave_data))
        if len(wave_data)==CHUNK:
             if len(PSdata_list)<800:
                print(len(PSdata_list))
                PSdata_list.append(power_spectrum)

    
    
    PSdata=np.vstack(PSdata_list)
    heatmap = plt.imshow(PSdata, interpolation='nearest', animated=False,aspect=0.2)
    plt.show()
    

    x=np.arange(np.shape(PSdata)[1])
    y=np.arange(np.shape(PSdata)[0])
    x, y = np.meshgrid(x, y)
    # Initial setup


    # Plotting a surface
    
    plt.contour(x, y, PSdata)
    plt.colorbar()  # To show the scale of values
    # Adding title and labels
    #plt.xticks=np.linspace(0,6000,16)
    plt.title('Spectrograph')
    plt.xlabel('freq')
    plt.ylabel('time')

    # Show plot
    plt.show()


def play_audio(filename):
    """
    Plays a WAV file using PyAudio.
    Args:
        filename (str): Path to the WAV file.
    """
    
    wf = wave.open(filename, 'rb')

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open an audio stream
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    print(f"Playing {filename}...")

    # Read and play audio in chunks
    data = wf.readframes(CHUNK)
    wave_data=[]
    # Create scatter plot
    while data:
        wave_data.append( np.frombuffer(data, dtype=np.int16))
        #stream.write(data)
        data = wf.readframes(CHUNK)
        stream.write(data)
        
    # y= [item for sublist in wave_data for item in sublist]
    # x=np.linspace(1,len(y),len(y))
    # plt.plot(x, y)

    # # Adding title and labels
    # plt.title('Scatter plot')
    # plt.xlabel('x')
    # plt.ylabel('y')
    # # Show plot
    # plt.show()

    
        
    # Cleanup
    stream.stop_stream()
    stream.close()
    p.terminate()

def analyze_audio():
    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Setup the figure and axis for plotting
    plt.ion()  # Turn on interactive mode
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_title('Evolving Power Spectrum')
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Power')
    ax.set_ylim(1e-5, 1e5)
    ax.set_xlim(0, 5600)
    ax.grid(True)
    ax.semilogy()
    plt.show()
 
    line1, = ax.semilogy([], [], lw=2)

    # Open stream
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Listening...")

    
    while True:
        data = stream.read(CHUNK)
        nd=np.frombuffer(data, dtype=np.int16)
        maxd=np.max(nd)
        frequencies, power_spectrum = periodogram(nd, fs=RATE)
        #update plot
        line1.set_xdata(frequencies)
        line1.set_ydata(power_spectrum)
        fig.canvas.draw()
        fig.canvas.flush_events()

    stream.stop_stream()
    stream.close()


def record_audio(fname,rec=False,log=False):
    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Setup the figure and axis for plotting
    plt.ion()  # Turn on interactive mode
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_title('Evolving Power Spectrum')
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Power')
    ax.set_ylim(1e-5, 1e5)
    ax.set_xlim(0, 5600)
    ax.grid(True)
    if log:
        ax.semilogy()
    plt.show()
 
    line1, = ax.semilogy([], [], lw=2)
    
    # Open stream
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Listening...")

    frames = []
    start=False
    MAX_RECORD_SECONDS = 60
    stop_time=time.time()
    # Record for RECORD_SECONDS
    first_time=True
    
    while start==False:
        data = stream.read(CHUNK)
        nd=np.frombuffer(data, dtype=np.int16)
        maxd=np.max(nd)
        #frequencies, power_spectrum = periodogram(nd, fs=RATE)
        print(maxd)

#update plot
        # line1.set_xdata(frequencies)
        # line1.set_ydata(power_spectrum)
        # fig.canvas.draw()
        # fig.canvas.flush_events()
        
        if rec:
            if abs(maxd)>2000:
                start=True
                stop_time=time.time()+10
                print("Start recording.")
                frames=[]
                while time.time()<stop_time:
                    data = stream.read(CHUNK)
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
            wf.setnchannels(CHANNELS)
            wf.setframerate(RATE)
            wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
            wf.writeframes(bytestream)
            wf.close()
    print("Finished writting to file")

    

if __name__ == "__main__":
    CHUNK = 512
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 11025
    RECORD_SECONDS = 15
    p = pyaudio.PyAudio()

    rec_filename="new_rec.wav"
    #record_audio(rec_filename,True,False)

    #filename="max_smooth_tone.wav"
    #filename="colby_smooth_tone.wav"
    #filename="michael_generated_waveform_windowed.WAV"
    #filename="EE310_HW7_1.wav"
    filename="new_rec.wav"
    #play_audio(filename)
    
    
    plot_audio(filename)
    input("press any key to quit")

    p.terminate()

    