import tkinter as tk
from tkinter import messagebox , ttk ,font
import  sqlite3
from datetime import datetime
import sys


class OnlineShoppingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Online Shopping Application")
        self.root.geometry("1200x600")

        self.conn = sqlite3.connect('orinoco.db')
        
        #temporary status to show connection status
        status_label = tk.Label(self .root,
                                text = "Database connected successfully",
                                fg = "red",
                                font = ("Arial", 10) )
        status_label.pack(side=tk.BOTTOM, fill=tk.X)
                                
        
        
        
        
def main():
    root = tk.Tk()
    app = OnlineShoppingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()