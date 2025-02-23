import tkinter as tk
from tkinter import messagebox


class InsufficientFundsError(Exception):
    """Custom exception for insufficient funds."""
    pass


class Account:
    def __init__(self, account_number, account_holder, initial_balance=0):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = initial_balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
        else:
            raise ValueError("Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFundsError(f"Insufficient funds. Available balance: {self.balance}.")
        elif amount > 0:
            self.balance -= amount
        else:
            raise ValueError("Withdrawal amount must be positive.")

    def get_balance(self):
        return self.balance

    def display_account_info(self):
        return f"Account Number: {self.account_number}\nAccount Holder: {self.account_holder}\nBalance: {self.balance}"


class BankingSystem:
    def __init__(self, root):
        self.accounts = {}

        self.root = root
        self.root.title("Banking System")
        self.root.geometry("600x500")
        self.root.configure(bg="#000000")  # Black background

        # Custom font styles
        self.default_font = ("Helvetica", 12)
        self.title_font = ("Helvetica", 16, "bold")

        # Title Label
        self.title_label = tk.Label(root, text="Banking System", font=self.title_font, bg="#000000", fg="white")
        self.title_label.pack(pady=10)

        # Account Creation Frame
        self.create_account_frame = tk.LabelFrame(root, text="Create Account", font=self.default_font,
                                                  bg="#000000", fg="white", padx=10, pady=10)
        self.create_account_frame.pack(pady=10, padx=20, fill="x")

        self.acc_num_entry = self.create_entry(self.create_account_frame, "Account Number:", 0)
        self.acc_holder_entry = self.create_entry(self.create_account_frame, "Account Holder:", 1)
        self.initial_balance_entry = self.create_entry(self.create_account_frame, "Initial Balance:", 2)

        self.create_acc_button = tk.Button(self.create_account_frame, text="Create Account", font=self.default_font,
                                           bg="#1B5E20", fg="black", command=self.create_account)
        self.create_acc_button.grid(row=3, columnspan=2, pady=10)

        # Transaction Frame
        self.transaction_frame = tk.LabelFrame(root, text="Transactions", font=self.default_font,
                                               bg="#000000", fg="white", padx=10, pady=10)
        self.transaction_frame.pack(pady=10, padx=20, fill="x")

        self.trans_acc_num_entry = self.create_entry(self.transaction_frame, "Account Number:", 0)
        self.amount_entry = self.create_entry(self.transaction_frame, "Amount:", 1)

        self.deposit_button = tk.Button(self.transaction_frame, text="Deposit", font=self.default_font,
                                        bg="#0D47A1", fg="black", command=self.deposit)
        self.deposit_button.grid(row=2, column=0, pady=10, padx=5)

        self.withdraw_button = tk.Button(self.transaction_frame, text="Withdraw", font=self.default_font,
                                         bg="#B71C1C", fg="black", command=self.withdraw)
        self.withdraw_button.grid(row=2, column=1, pady=10, padx=5)

        # Account Info Frame
        self.info_frame = tk.LabelFrame(root, text="Account Information", font=self.default_font,
                                        bg="#000000", fg="white", padx=10, pady=10)
        self.info_frame.pack(pady=10, padx=20, fill="x")

        self.info_acc_num_entry = self.create_entry(self.info_frame, "Account Number:", 0)

        self.info_button = tk.Button(self.info_frame, text="Display Info", font=self.default_font,
                                     bg="#4A148C", fg="black", command=self.display_info)
        self.info_button.grid(row=1, columnspan=2, pady=10)

    def create_entry(self, frame, label_text, row):
        """Helper function to create labeled entry fields."""
        label = tk.Label(frame, text=label_text, font=self.default_font, bg="#000000", fg="white")
        label.grid(row=row, column=0, padx=5, pady=5, sticky="w")
        entry = tk.Entry(frame, font=self.default_font)
        entry.grid(row=row, column=1, padx=5, pady=5)
        return entry

    def create_account(self):
        acc_num = self.acc_num_entry.get()
        acc_holder = self.acc_holder_entry.get()
        initial_balance = self.initial_balance_entry.get()

        if acc_num and acc_holder:
            try:
                initial_balance = float(initial_balance) if initial_balance else 0
                self.accounts[acc_num] = Account(acc_num, acc_holder, initial_balance)
                messagebox.showinfo("Success", "Account created successfully!")
            except ValueError:
                messagebox.showwarning("Error", "Invalid initial balance!")
        else:
            messagebox.showwarning("Error", "Account number and holder name cannot be empty!")

    def deposit(self):
        acc_num = self.trans_acc_num_entry.get()
        amount = self.amount_entry.get()

        if acc_num in self.accounts:
            try:
                amount = float(amount)
                self.accounts[acc_num].deposit(amount)
                messagebox.showinfo("Success", f"Deposited {amount}. New balance: {self.accounts[acc_num].get_balance()}.")
            except ValueError:
                messagebox.showwarning("Error", "Invalid deposit amount!")
        else:
            messagebox.showwarning("Error", "Account not found!")

    def withdraw(self):
        acc_num = self.trans_acc_num_entry.get()
        amount = self.amount_entry.get()

        if acc_num in self.accounts:
            try:
                amount = float(amount)
                self.accounts[acc_num].withdraw(amount)
                messagebox.showinfo("Success", f"Withdrew {amount}. New balance: {self.accounts[acc_num].get_balance()}.")
            except InsufficientFundsError as e:
                messagebox.showwarning("Error", str(e))
            except ValueError:
                messagebox.showwarning("Error", "Invalid withdrawal amount!")
        else:
            messagebox.showwarning("Error", "Account not found!")

    def display_info(self):
        acc_num = self.info_acc_num_entry.get()

        if acc_num in self.accounts:
            account_info = self.accounts[acc_num].display_account_info()
            messagebox.showinfo("Account Info", account_info)
        else:
            messagebox.showwarning("Error", "Account not found!")


if __name__ == "__main__":
    root = tk.Tk()
    app = BankingSystem(root)
    root.mainloop()

