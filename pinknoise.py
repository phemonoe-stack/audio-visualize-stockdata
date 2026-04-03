import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

def analyze_pink_noise(ticker, period="60d", interval="5m"):
    # 1. Pull the data (The "Telescope")
    data = yf.download(ticker, period=period, interval=interval)
    prices = data['Close'].values
    
    # 2. Calculate Volatility (The "Wobble")
    # Voss (1992) suggests looking at the absolute increments: |Δ$(t)|
    returns = np.diff(prices)
    volatility = np.abs(returns)
    
    # 3. Fast Fourier Transform (The "Prism")
    n = len(volatility)
    freqs = np.fft.fftfreq(n)
    fft_values = np.fft.fft(volatility)
    psd = np.abs(fft_values)**2  # Power Spectral Density
    
    # 4. Filter for Positive Frequencies
    mask = freqs > 0
    f_plot = freqs[mask]
    psd_plot = psd[mask]
    
    # 5. Log-Log Plot (The "Voss Test")
    # If the slope is ~ -1, you've found Pink Noise (1/f)
    plt.figure(figsize=(10, 6))
    plt.loglog(f_plot, psd_plot, label=f'PSD of {ticker} Volatility')
    
    # Add a reference 1/f line
    plt.loglog(f_plot, 1/f_plot * (psd_plot[0]*f_plot[0]), '--', label='Ideal 1/f Noise')
    
    plt.title(f"Spectral Density of {ticker} (The Voss Test)")
    plt.xlabel("Frequency (f)")
    plt.ylabel("Power (S(f))")
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.5)
    plt.show()

# Run it on your target
analyze_pink_noise("ASTS")