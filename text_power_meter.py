import time
import pyaudio
import numpy as np
from scipy.signal import stft
from scipy.signal import welch


# Set the chunk size and sample rate
CHUNK = 512
RATE = 11025

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open the microphone stream
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)


# Create a Hanning window for the STFT
#window = np.hanning(n_fft)
ptime=time.time()
try:
    while True:
        # Read audio data from the microphone
        data = stream.read(CHUNK)

        # Convert the audio data to a numpy array
        signal = np.frombuffer(data, dtype=np.int16)

        f, Pxx = welch(signal, fs=RATE, nperseg=CHUNK)

        # # Perform the STFT
        # f, t, Zxx = stft(signal, fs=RATE, nperseg=CHUNK, noverlap=CHUNK/2)
        # # Calculate the power spectrum
        # power_spectrum = np.abs(Zxx) ** 2

        # Convert the power spectrum to decibels
        #power_spectrum_db = np.log10(Pxx + 1e-10)
        power_spectrum_db =np.log2( Pxx)
        power_spectrum_db =( Pxx/100)

        P32_8 = power_spectrum_db[1:].reshape(16, 16)
        # Sum along the second axis (axis=1) to get the sum of each group of 8 elements
        P32 = P32_8.sum(axis=1)
        if time.time()>ptime+.25:
            #Print the power spectrum as a text waterfall
            for i in range(len(P32)):
                print("{:6d}".format(int(P32[i]/5)),end="")
            print("{:7d}".format(int(np.sum(P32)/5/32)),end="")
            print("")
            ptime=time.time()

except KeyboardInterrupt:
    # Stop the stream and terminate PyAudio
    stream.stop_stream()
    stream.close()
    p.terminate()