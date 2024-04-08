import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
import pyaudio
import wave
import numpy as np
import scipy
from scipy.signal import periodogram
import time 


def make_plot(wav):

    f, t, Zxx = scipy.stft(wav, RATE, nperseg=512)  # nperseg determines the size of the window
    # Plot heatmap
    plt.figure(figsize=(10, 6))
    plt.pcolormesh(t, f, np.abs(Zxx), shading='gouraud')  # Use absolute value of Zxx
    plt.title("SHORT TIME FFT")
    plt.xlabel('Time [s]')
    plt.ylabel('Frequency [Hz]')
    plt.colorbar(label='Magnitude')
    plt.ylim(0, 5500)  # Limit frequency range for better visualization
    # Adding title and labels
    #plt.xticks=np.linspace(0,6000,16)
    # Show plot
    plt.show()

def load_audio(filename):
    wf = wave.open(filename, 'rb')
    # Read audio in chunks
    data = wf.readframes(CHUNK)
    wave_data=[]
    data_list=[]
    # Create scatter plot
    while data:
        wave_data=np.frombuffer(data, dtype=np.int16)
        #stream.write(data)
        data = wf.readframes(CHUNK)

        #print(len(wave_data))
        if len(wave_data)==CHUNK:
             if len(data_list)<800:
                print(len(data_list))
                data_list.append(wave_data)
    wav=np.concatenate(data_list)
    return wav
    
   

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

sg.theme("TanBlue")  # let's add a little color
#globals
RATE = 11025
CHUNK=512
SIZE_X = 100
SIZE_Y = 100
NUMBER_MARKER_FREQUENCY = 25

# Window layout
data = np.random.rand(10, 10)

# Initial plot
fig, ax = plt.subplots(figsize=(5, 4))
heatmap = ax.imshow(data, interpolation='nearest')
plt.colorbar(heatmap, ax=ax)

layout = [
    [
        sg.Text(
            "GUI analyzer",
            justification="center",
            size=(50, 1)
        )
    ],
    [sg.Canvas(key='-CANVAS-')],

    [
        sg.Text("x1"),
        sg.Slider((0, 200), orientation="h", enable_events=True, key="_SLIDER_"),
    ],
    [
        sg.Text("x2"),
        sg.Slider((1, 200), orientation="h", enable_events=True, key="_SLIDER2_"),
    ],
    [
       sg.Text("Current file= "),sg.Input(default_text='test.wav',size=(20,1), key="-INPUT-")
    ]   ,
    [
        sg.Button('Load File', key = "_LOAD_FILE_")
    ]

]
window = sg.Window("SONIO analysis", layout,finalize=True)


# Draw the initial figure in the PySimpleGUI window
canvas_elem = window['-CANVAS-']
canvas = canvas_elem.TKCanvas
fig_agg = draw_figure(canvas, fig)


while True:
    event, values = window.read()
    if event is None:
        break
    prev_x = prev_y = None
    for x in range(-SIZE_X, SIZE_X):
        y = math.sin(x / int(values["_SLIDER2_"])) * int(values["_SLIDER_"])
        if prev_x is not None:
            pass
