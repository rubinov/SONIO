import pyaudio
import wave
import math
import matplotlib.pyplot as plt
import numpy as np
import time 

def sweep1(start,stop,sec):

    if stop<400: stop=400
    if start<300: start=300
    if stop>5000: stop=5000
    if sec<1: sec=1
    if sec>30: sec=30

    wav=np.zeros(math.floor(sec*RATE),dtype=np.int16)
    num_samples=len(wav)
    #np.linspace(0, sec, int(RATE * sec), endpoint=False)
 
    # would like to spend an equal amount of time at each step
    # but a minimum of 
    t=0    
    wav[0]=0
    ang=0
    while (t<num_samples):
        freq=(start+t/num_samples*(stop-start))
        #ang,turn=math.modf(np.pi*2*freq/RATE)
        ang+=np.pi*freq*2/RATE     
        wav[t]=((2**15)-1)*math.sin(ang)
        t+=1
        print(t,freq)
    print("done!")
    return wav

def sweep2(start,stop,sec):

    if stop<400: stop=400
    if start<300: start=300
    if stop>5000: stop=5000
    if sec<1: sec=1
    if sec>30: sec=30

    wav=np.zeros(math.floor(sec*RATE),dtype=np.int16)
    num_samples=len(wav)
    #np.linspace(0, sec, int(RATE * sec), endpoint=False)
 
    # would like to spend an equal amount of time at each step
    # but a minimum of 
    t=0    
    wav[0]=0
    ang=0
    freq=np.linspace(start,stop,RATE*sec)
    ang,rot=freq/RATE*np.pi*2
    #ang=np.cumsum(ang)
    wav=np.sin(ang)
    wav=wav*(2**15-1)
    print("done!")
    return wav

def generate(plot,preview,filename):
    print("* Generating sample...")
    tone_out_np = sweep1(500,4500,5)
    tone_out=tone_out_np.astype(np.int16).tolist()

    if plot:
        y= tone_out
        x=np.linspace(1,len(y),len(y))
        plt.plot(x, y)

        # Adding title and labels
        plt.title('Scatter Plot Example')
        plt.xlabel('x')
        plt.ylabel('y')
        # Show plot

        plt.show()
        next=input("press any key to continue...")

        
    if preview:
        print("* Previewing audio file...")

        bytestream = tone_out_np.tobytes()
        pya = pyaudio.PyAudio()
        stream = pya.open(format=pya.get_format_from_width(width=2), channels=1, rate=RATE, output=True)
        stream.write(bytestream)
        stream.stop_stream()
        stream.close()

        pya.terminate()
        print("* Preview completed!")
    else:
        frames = tone_out_np.tobytes()
        print("* Starting to write audio file!")
        # Save recorded data to a WAV file

        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setframerate(RATE)
            wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
            wf.writeframes(frames)
            wf.close()
        
        print("* Wrote audio file!")
        

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
    while data:
        stream.write(data)
        data = wf.readframes(CHUNK)

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

    filename="EE310_HW7_1.wav"
    generate(False,False,filename)
    #play_audio(filename)
    