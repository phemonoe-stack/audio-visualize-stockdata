import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm

def create_spectral_chart(ticker='GOSS', start='2023-01-01', end='2026-03-26'):
    # 1. Fetch & Clean Data
    df = yf.download(ticker, start=start, end=end, auto_adjust=True)
    if df.empty: return print("No data found.")
    prices = df['Close'].to_numpy().flatten()
    prices = prices[~np.isnan(prices)].astype(float)
    
    # 2. Map Price to Hue (Red to Violet)
    # We normalize prices and map them to a 0.0 - 0.8 range in HSV 
    # (0.8 is roughly Violet, 0.0 is Red)
    p_min, p_max = np.min(prices), np.max(prices)
    norm_prices = (prices - p_min) / (p_max - p_min)
    
    # Invert so high prices = violet (high freq), low = red (low freq)
    hues = norm_prices * 0.8 
    
    # 3. Create Colored Line Segments
    points = np.array([np.arange(len(prices)), prices]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    
    # Create a colormap from the HSV values
    # We use 'jet' or 'turbo' because they mimic the visible light spectrum
    cmap = plt.get_cmap('turbo')
    lc = LineCollection(segments, cmap=cmap, linewidth=2.5)
    lc.set_array(norm_prices) # Color based on price height

    # 4. Visualization
    fig, ax = plt.subplots(figsize=(15, 7), facecolor='#0b0e11')
    ax.set_facecolor('#0b0e11')
    
    # Add the colored line to the plot
    line = ax.add_collection(lc)
    
    # Aesthetics
    ax.set_xlim(0, len(prices))
    ax.set_ylim(p_min * 0.95, p_max * 1.05)
    ax.tick_params(colors='white')
    for s in ax.spines.values(): s.set_color('#333')
    
    # Colorbar to show the "Frequency" scale
    cbar = fig.colorbar(line, ax=ax)
    cbar.set_label('Relative Frequency (Red=Low, Violet=High)', color='white')
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')

    plt.title(f"Spectral Frequency Chart: {ticker}", color='white', fontsize=14)
    plt.show()

# Run it
create_spectral_chart()
