import numpy as np
import yfinance as yf
from IPython.display import Audio

def get_market_tone(ticker='^GSPC', start='1929-01-01', end='1935-12-31', bpm=120):
    # 1. Grab the data
    data = yf.download(ticker, start=start, end=end)
    # Using 'Close' but 'Adj Close' is better for long-term historicals
    prices = data['Close'].values
    
    # 2. Time constants
    fs = 44100  # Sample rate
    seconds_per_beat = 60 / bpm
    t = np.linspace(0, seconds_per_beat, int(fs * seconds_per_beat), False)
    
    # 3. Logarithmic Pitch Mapping (Perfect 4th to High C)
    # This ensures a 10% move in price sounds like a consistent interval
    p_min, p_max = np.min(prices), np.max(prices)
    # Map to MIDI notes (60 is Middle C) then to Hz
    midi_notes = 48 + (np.log(prices) - np.log(p_min)) / (np.log(p_max) - np.log(p_min)) * 36
    freqs = 440 * (2 ** ((midi_notes - 69) / 12))
    
    audio_buffer = []
    
    # 4. Synthesize with a Smooth Envelope
    window = np.hanning(len(t)) # Removes the "pop" between days
    
    for f in freqs:
        # Generate Sine Wave
        note = np.sin(2 * np.pi * f * t) * window
        audio_buffer.append(note)
    
    # Concatenate and Normalize
    final_audio = np.concatenate(audio_buffer)
    final_audio /= np.max(np.abs(final_audio))
    
    return final_audio, fs

# Run it for the 1929 -> 1930 "Dual-Rupture"
audio, sr = get_market_tone()
print("Rendering the Frequency of 1929...")
Audio(audio, rate=sr)