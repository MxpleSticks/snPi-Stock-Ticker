import tkinter as tk
from tkinter import ttk
import finnhub
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from datetime import datetime, timedelta


class StockTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Tracker")
        self.root.configure(bg='#1E1E1E')  

        # Configure styles
        self.style = ttk.Style()
        self.style.configure('Custom.TFrame', background='#1E1E1E')
        self.style.configure('Custom.TLabel', background='#1E1E1E', foreground='white', font=('Helvetica', 12))

        # Main container
        self.main_frame = ttk.Frame(root, style='Custom.TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40) 

        # Stock info section
        self.header_frame = ttk.Frame(self.main_frame, style='Custom.TFrame')
        self.header_frame.pack(fill=tk.X, pady=(0, 30))  

        # Left side container for stock symbol
        self.symbol_frame = ttk.Frame(self.header_frame, style='Custom.TFrame')
        self.symbol_frame.pack(side=tk.LEFT)

        # Stock symbol (changed to LEFT anchor)
        self.stock_name = ttk.Label(self.symbol_frame, text="VOO", 
                                  style='Custom.TLabel', 
                                  font=('Helvetica', 36, 'bold'))
        self.stock_name.pack(anchor=tk.W)

        # Market status (moved under VOO)
        self.market_status = ttk.Label(self.symbol_frame, text="MARKET CLOSED", 
                                     style='Custom.TLabel', 
                                     foreground='#FF4B4B',  # Default to red
                                     font=('Helvetica', 12, 'bold'))
        self.market_status.pack(anchor=tk.W)

        # Price and change container (right side)
        self.price_frame = ttk.Frame(self.header_frame, style='Custom.TFrame')
        self.price_frame.pack(side=tk.RIGHT)

        # Current price
        self.current_value = tk.Canvas(self.price_frame, width=200, height=50, bg='#1E1E1E', highlightthickness=0)
        self.current_value.pack(anchor=tk.E)
        self.current_value_text = self.current_value.create_text(100, 25, text="$0.00", font=('Helvetica', 36, 'bold'), fill='white')

        # Percentage change
        self.percentage = tk.Canvas(self.price_frame, width=150, height=50, bg='#1E1E1E', highlightthickness=0)
        self.percentage.pack(anchor=tk.E)
        self.percentage_text = self.percentage.create_text(75, 25, text="+0.00%", font=('Helvetica', 24), fill='white')

        # Additional info frame (new)
        self.info_frame = ttk.Frame(self.main_frame, style='Custom.TFrame')
        self.info_frame.pack(fill=tk.X, pady=(0, 20))

        # Previous close (new)
        self.prev_close_label = ttk.Label(self.info_frame, text="Previous Close:", style='Custom.TLabel', font=('Helvetica', 14))
        self.prev_close_label.pack(side=tk.LEFT, padx=(0, 10))
        self.prev_close_value = ttk.Label(self.info_frame, text="$0.00", style='Custom.TLabel', font=('Helvetica', 14, 'bold'))
        self.prev_close_value.pack(side=tk.LEFT)

        # Graph frame (made smaller)
        self.graph_frame = ttk.Frame(self.main_frame, style='Custom.TFrame')
        self.graph_frame.pack(fill=tk.BOTH, expand=True)

        # Create matplotlib figure with smaller size
        self.fig = Figure(figsize=(10, 4), dpi=100, facecolor='#1E1E1E')  
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#1E1E1E')

        # Style the graph
        self.ax.spines['bottom'].set_color('#666666')
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_color('#666666')
        self.ax.tick_params(colors='#666666')
        self.ax.grid(False)

        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Initialize Finnhub client
        self.finnhub_client = finnhub.Client("YOUR_API_KEY_HERE")

        # Add price history storage
        self.price_history = []
        self.time_history = []
        self.max_history_points = 120  

        # Store previous values for animation
        self.prev_price = None
        self.prev_percentage = None

        # Start updating
        self.update_data()

    def is_market_open(self):
        now = datetime.now()
        # Check if it's a weekday (0 = Monday, 4 = Friday)
        if now.weekday() > 4:
            return False
        
        # Convert to EST/EDT
        market_time = now - timedelta(hours=4)  # Simple EST conversion
        
        # Check if within market hours (9:30 AM - 4:00 PM EST)
        return (
            (market_time.hour > 9 or (market_time.hour == 9 and market_time.minute >= 30)) and
            (market_time.hour < 16)
        )

    def update_data(self):
        try:
            print("Updating data...")  
            # Update market status
            is_open = self.is_market_open()
            self.market_status.configure(
                text="MARKET OPEN" if is_open else "MARKET CLOSED",
                foreground='#00D964' if is_open else '#FF4B4B'  # Green when open, red when closed
            )

            # Get current quote
            quote = self.finnhub_client.quote('VOO')
            current_price = quote['c']
            previous_close = quote['pc']  # This is the starting price of the day
            change_pct = ((current_price - previous_close) / previous_close * 100)

            # Update price history
            current_time = datetime.now()
            self.price_history.append(current_price)
            self.time_history.append(current_time)
            
            # Keep only the last max_history_points
            if len(self.price_history) > self.max_history_points:
                self.price_history.pop(0)
                self.time_history.pop(0)

            print(f"Current price: ${current_price:.2f}, Change: {change_pct:.2f}%")

            # Update labels
            if self.prev_price is not None and current_price != self.prev_price:
                self.animate_price(current_price)
            else:
                self.current_value.itemconfig(self.current_value_text, text=f"${current_price:.2f}")

            # Update percentage with color
            percent_text = f"{'+' if change_pct >= 0 else ''}{change_pct:.2f}%"
            if self.prev_percentage is not None and change_pct != self.prev_percentage:
                self.animate_percentage(change_pct)
            else:
                self.percentage.itemconfig(self.percentage_text, text=percent_text)
                color = '#00D964' if change_pct >= 0 else '#FF4B4B'  # Changed from -0.01 to 0
                self.percentage.itemconfig(self.percentage_text, fill=color)

            # Update previous close value (new)
            self.prev_close_value.configure(text=f"${previous_close:.2f}")

            # Update graph with history
            self.ax.clear()
            self.ax.set_facecolor('#1E1E1E')

            if len(self.price_history) > 1:
                # Change color based on comparison with previous close (start of day)
                color = '#00D964' if current_price >= previous_close else '#FF4B4B'
                
                # Plot the entire price history
                self.ax.plot(self.time_history, self.price_history, color=color, linewidth=2)
                
                # Add gradient fill
                self.ax.fill_between(self.time_history, self.price_history, 
                                   min(self.price_history)*0.9999,
                                   color=color, alpha=0.1)

                # Set axis limits with some padding
                self.ax.set_xlim(min(self.time_history), max(self.time_history))
                self.ax.set_ylim(min(self.price_history)*0.9999, max(self.price_history)*1.0001)

            # Style the axes
            self.ax.spines['bottom'].set_color('#666666')
            self.ax.spines['top'].set_visible(False)
            self.ax.spines['right'].set_visible(False)
            self.ax.spines['left'].set_color('#666666')
            self.ax.tick_params(colors='#666666')
            
            # Remove labels and update layout
            self.ax.set_xlabel('')
            self.ax.set_ylabel('')
            self.fig.tight_layout()

            # Refresh canvas
            self.canvas.draw()
            print("Graph updated") 

            # Store current values for next update
            self.prev_price = current_price
            self.prev_percentage = change_pct

        except Exception as e:
            print(f"Error updating data: {e}")

       
        self.root.after(3000, self.update_data)  

    def animate_price(self, new_price):
        current_price = float(self.current_value.itemcget(self.current_value_text, 'text').replace('$', ''))
        if new_price > current_price:
            self.animate_up(self.current_value, self.current_value_text, current_price, new_price)
        else:
            self.animate_down(self.current_value, self.current_value_text, current_price, new_price)

    def animate_percentage(self, new_percentage):
        current_percentage = float(self.percentage.itemcget(self.percentage_text, 'text').replace('%', '').replace('+', ''))
        if new_percentage > current_percentage:
            self.animate_up(self.percentage, self.percentage_text, current_percentage, new_percentage)
        else:
            self.animate_down(self.percentage, self.percentage_text, current_percentage, new_percentage)

    def animate_up(self, canvas, text_id, start_value, end_value):
        current_value = start_value
        step = (end_value - start_value) / 10
        for _ in range(10):
            current_value += step
            if canvas == self.current_value:
                canvas.itemconfig(text_id, text=f"${current_value:.2f}")
            else:
                canvas.itemconfig(text_id, text=f"{'+' if current_value >= 0 else ''}{current_value:.2f}%")
                color = '#00D964' if current_value >= 0 else '#FF4B4B'
                canvas.itemconfig(text_id, fill=color)
            self.root.update()
            time.sleep(0.1)

    def animate_down(self, canvas, text_id, start_value, end_value):
        current_value = start_value
        step = (end_value - start_value) / 10
        for _ in range(10):
            current_value += step
            if canvas == self.current_value:
                canvas.itemconfig(text_id, text=f"${current_value:.2f}")
            else:
                canvas.itemconfig(text_id, text=f"{'+' if current_value >= 0 else ''}{current_value:.2f}%")
                color = '#00D964' if current_value >= 0 else '#FF4B4B'
                canvas.itemconfig(text_id, fill=color)
            self.root.update()
            time.sleep(0.1)


def main():
    root = tk.Tk()
    root.configure(bg='#1E1E1E')
    app = StockTrackerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
