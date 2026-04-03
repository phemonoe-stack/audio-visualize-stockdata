!pip install yfinance

import numpy as np
import yfinance as yf
from IPython.display import Audio

def sonify_market(ticker, start_date, end_date, duration_per_bar=0.1):
    # 1. Fetch Data
    df = yf.download(ticker, start=start_date, end=end_date)
    prices = df['Close'].values
    
    # 2. Normalize Prices to Frequency (Hz)
    # Mapping price range to a 2-octave musical range (220Hz to 880Hz)
    min_p, max_p = np.min(prices), np.max(prices)
    freqs = 220 + (prices - min_p) / (max_p - min_p) * (880 - 220)
    
    # 3. Generate Audio Signal
    fs = 44100  # Sample rate
    full_audio = []
    
    t = np.linspace(0, duration_per_bar, int(fs * duration_per_bar), False)
    
    for f in freqs:
        # Create a sine wave for this price point
        note = np.sin(f * t * 2 * np.pi)
        # Apply a quick fade-out to prevent "clicking" between notes
        envelope = np.exp(-3 * t / duration_per_bar)
        full_audio.append(note * envelope)
    
    audio_signal = np.concatenate(full_audio)
    
    return audio_signal, fs

# --- EXECUTION ---
# Let's hear the "Sound of the 1929 Crash" (Jan to Dec)
audio, sample_rate = sonify_market('^GSPC', '1929-01-01', '1929-12-31')

print("Playing the sonification of the 1929 Crash...")
Audio(audio, rate=sample_rate)