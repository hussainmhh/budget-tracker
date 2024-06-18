import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class BudgetTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Tracker")
        self.transactions = []
        
        self.setup_ui()
    
    def setup_ui(self):
        # Frame for inputs
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(frame, text="Description:").grid(row=0, column=0, padx=5, pady=5)
        self.desc_entry = ttk.Entry(frame, width=20)
        self.desc_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Amount:").grid(row=1, column=0, padx=5, pady=5)
        self.amount_entry = ttk.Entry(frame, width=20)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Add Income", command=self.add_income).grid(row=2, column=0, padx=5, pady=5)
        ttk.Button(frame, text="Add Expense", command=self.add_expense).grid(row=2, column=1, padx=5, pady=5)

        # Frame for balance
        balance_frame = ttk.Frame(self.root, padding="10")
        balance_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(balance_frame, text="Current Balance:").grid(row=0, column=0, padx=5, pady=5)
        self.balance_label = ttk.Label(balance_frame, text="0.00")
        self.balance_label.grid(row=0, column=1, padx=5, pady=5)

        # Frame for pie chart
        self.chart_frame = ttk.Frame(self.root, padding="10")
        self.chart_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Button(self.root, text="Show Chart", command=self.show_chart).grid(row=3, column=0, padx=5, pady=5)

    def add_income(self):
        self.add_transaction("Income")

    def add_expense(self):
        self.add_transaction("Expense")

    def add_transaction(self, t_type):
        desc = self.desc_entry.get()
        amount = self.amount_entry.get()
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid amount")
            return

        self.transactions.append({"type": t_type, "description": desc, "amount": amount})
        self.update_balance()

    def update_balance(self):
        balance = sum(t["amount"] if t["type"] == "Income" else -t["amount"] for t in self.transactions)
        self.balance_label.config(text=f"{balance:.2f}")

    def show_chart(self):
        income = sum(t["amount"] for t in self.transactions if t["type"] == "Income")
        expenses = sum(t["amount"] for t in self.transactions if t["type"] == "Expense")

        fig, ax = plt.subplots()
        ax.pie([income, expenses], labels=["Income", "Expenses"], autopct='%1.1f%%')
        ax.set_title("Income vs Expenses")

        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.get_tk_widget().grid(row=0, column=0)
        canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetTracker(root)
    root.mainloop()
