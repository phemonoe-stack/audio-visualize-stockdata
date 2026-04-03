import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from IPython.display import Audio, display

def create_fast_diagnostic(ticker='^GSPC', start='1929-01-01', end='1930-12-31'):
    # 1. Fetch Data
    df = yf.download(ticker, start=start, end=end, auto_adjust=True)
    if df.empty: return print("No data found.")
    
    # Clean extraction
    prices = df['Close'].to_numpy().flatten()
    prices = prices[~np.isnan(prices)].astype(float)
    
    # 2. Seed Data (64-step sequence)
    seed = [0, 2, 3, 2, 4, 1, 3, 2, 3, 4, 4, 4, 1, 6, 2, 2, 3, 4, 3, 2, 1, 6, 3, 6, 3, 6, 2, 4, 4, 4, 3, 2, 
            4, 2, 4, 6, 2, 2, 4, 2, 2, 6, 3, 4, 3, 2, 2, 2, 3, 4, 2, 6, 2, 6, 3, 2, 3, 4, 4, 4, 2, 4, 6, 4]
    novelty_wave = np.array([seed[i % len(seed)] for i in range(len(prices))])
    
    # 3. Audio (Sine-Wave Sonification)
    fs = 44100
    duration = 0.05 # Fast playback for efficiency
    t = np.linspace(0, duration, int(fs * duration), False)
    window = np.hanning(len(t))
    
    p_min, p_max = np.min(prices), np.max(prices)
    midi = 48 + (np.log(prices) - np.log(p_min)) / (np.log(p_max) - np.log(p_min)) * 36
    freqs = 440 * (2 ** ((midi - 69) / 12))
    
    audio_signal = np.concatenate([np.sin(2 * np.pi * f * t) * window for f in freqs])
    
    # 4. Static "Score" Visualization
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 8), facecolor='#0b0e11', sharex=True)
    plt.subplots_adjust(hspace=0.05)
    
    for ax in [ax1, ax2]:
        ax.set_facecolor('#0b0e11')
        ax.tick_params(colors='white', which='both')
        for s in ax.spines.values(): s.set_color('#333')

    # Price Chart
    ax1.plot(prices, color='#00ffcc', lw=1.5, label='Market Frequency')
    ax1.fill_between(range(len(prices)), prices, np.min(prices), color='#00ffcc', alpha=0.1)
    ax1.set_ylabel("Price / Pitch", color='white')
    
    # Novelty Seed
    ax2.step(range(len(prices)), novelty_wave, color='#ff00ff', lw=1, where='post')
    ax2.set_ylabel("Seed Value", color='white')
    
    plt.suptitle(f"SONIFICATION SCORE: {ticker}", color='white', fontsize=16)
    plt.show()
    
    # Play Audio
    display(Audio(audio_signal, rate=fs))

create_fast_diagnostic()