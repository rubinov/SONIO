import pyaudio
import wave
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.signal import periodogram
from scipy.signal import stft

import time 

def plot_audio(filename):
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

    
    x=np.concatenate(data_list)
    f, t, Zxx = stft(x, RATE, nperseg=500)  # nperseg determines the size of the window
    # Plot heatmap
    plt.figure(figsize=(10, 6))
    plt.pcolormesh(t, f, np.abs(Zxx), shading='gouraud')  # Use absolute value of Zxx
    plt.title(filename)
    plt.xlabel('Time [s]')
    plt.ylabel('Frequency [Hz]')
    plt.colorbar(label='Magnitude')
    plt.ylim(0, 5500)  # Limit frequency range for better visualization
    # Adding title and labels
    #plt.xticks=np.linspace(0,6000,16)
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

if __name__ == "__main__":
    CHUNK = 512
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 11025
    RECORD_SECONDS = 15
    p = pyaudio.PyAudio()

    
    #filename="max_smooth_tone.wav"
    filename="colby_smooth_tone.wav"
    #filename="michael_generated_waveform_windowed.WAV"
    #filename="EE310_HW7_1.wav"
    #play_audio(filename)
    
    
    plot_audio(filename)
    input("press any key to quit")

    p.terminate()

    