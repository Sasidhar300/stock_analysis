import tkinter as tk
from tkinter import messagebox
import yfinance as yf
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

start_date = '1995-01-01'
end_date = datetime.datetime.now().strftime('%Y-%m-%d')

sp500 = yf.Ticker('^GSPC').history(start=start_date, end=end_date)['Close']

# Function to calculate CAPM expected return
def calculate_capm_expected_return(risk_free_rate, beta, market_expected_return):
    expected_return = risk_free_rate + beta * (market_expected_return - risk_free_rate)
    return expected_return

# Function to fetch historical data and calculate CAPM
def calculate_best_stocks():
    stocks = entry_stocks.get().split(',')
    num_stocks = int(entry_num_stocks.get())
    risk_free_rate = float(entry_risk_free_rate.get()) / 100  # Convert to decimal

    # Fetch historical data
    

    sp500_returns = sp500.pct_change().dropna()

    best_stocks = []

    for stock_symbol in stocks:
        try:
            stock = yf.Ticker(stock_symbol.strip()).history(start=start_date, end=end_date)['Close']
            stock_returns = stock.pct_change().dropna()

            # Calculate beta
            cov_stock_market = stock_returns.cov(sp500_returns)
            var_market = sp500_returns.var()
            beta = cov_stock_market / var_market

            # Calculate CAPM expected return
            expected_return = calculate_capm_expected_return(risk_free_rate, beta, sp500_returns.mean())

            best_stocks.append((stock_symbol, expected_return))
        except:
            messagebox.showerror("Error", f"Failed to fetch data for {stock_symbol}")

    # Sort stocks by expected return
    best_stocks.sort(key=lambda x: x[1], reverse=True)

    # Display the best-performing stocks
    display_results(best_stocks[:num_stocks], sp500)

def display_results(best_stocks, sp500):
    # Create a new window for displaying results
    result_window = tk.Toplevel(root)
    result_window.title("Best Performing Stocks and Comparison to S&P 500")

    # Display the best-performing stock names
    label_best_stocks = tk.Label(result_window, text="Best Performing Stocks:")
    label_best_stocks.pack()

    for stock_symbol, _ in best_stocks:
        label_stock = tk.Label(result_window, text=stock_symbol)
        label_stock.pack()

    # Plot the performance of the best stocks compared to S&P 500
    fig, ax = plt.subplots()
    for stock_symbol, _ in best_stocks:
        stock_data = yf.Ticker(stock_symbol).history(start=start_date, end=end_date)['Close']
        stock_returns = stock_data.pct_change().dropna()
        ax.plot(stock_returns.index, stock_returns, label=stock_symbol)

    sp500_returns = sp500.pct_change().dropna()
    ax.plot(sp500_returns.index, sp500_returns, label="S&P 500", linestyle='--')

    ax.set_xlabel('Date')
    ax.set_ylabel('Daily Returns')
    ax.legend()

    # Embed the Matplotlib plot into the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=result_window)
    canvas.get_tk_widget().pack()
    canvas.draw()

# Create the main application window
root = tk.Tk()
root.title("CAPM-based Stock Selection")

# Create and place widgets for stocks
label_stocks = tk.Label(root, text="Enter stock symbols (comma-separated):")
label_stocks.pack()

entry_stocks = tk.Entry(root)
entry_stocks.pack()

# Create and place widgets for the number of stocks
label_num_stocks = tk.Label(root, text="Enter the number of stocks to select:")
label_num_stocks.pack()

entry_num_stocks = tk.Entry(root)
entry_num_stocks.pack()

# Create and place widgets for the risk-free rate
label_risk_free_rate = tk.Label(root, text="Enter the risk-free rate (%):")
label_risk_free_rate.pack()

entry_risk_free_rate = tk.Entry(root)
entry_risk_free_rate.pack()

# Create button to calculate best stocks
calculate_button = tk.Button(root, text="Calculate Best Stocks", command=calculate_best_stocks)
calculate_button.pack()

# Run the main event loop
root.mainloop()

