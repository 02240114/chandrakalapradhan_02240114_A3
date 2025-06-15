import tkinter as tk
from tkinter import messagebox, simpledialog
import random

class InvalidAmountError(Exception):
    """Exception raised when an invalid (non-positive) amount is used in a transaction."""
    pass

class InsufficientFundsError(Exception):
    """Exception raised when an account does not have enough balance for a transaction."""
    pass

class BankAccount:
    """
    Represents a bank account with basic operations such as deposit, withdraw, transfer, and mobile top-up.

    Attributes:
        account_number (str): The unique account number.
        name (str): The account holder's name.
        passcode (str): The account's passcode.
        balance (float): The current balance of the account.
        transactions (list): A list of transaction descriptions.
    """
    def __init__(self, account_number, name, passcode, balance=0):
        """
        Initialize a new BankAccount.

        Args:
            account_number (str): The unique account number.
            name (str): The account holder's name.
            passcode (str): The account's passcode.
            balance (float, optional): The initial balance. Defaults to 0.
        """
        self.account_number = account_number
        self.name = name
        self.passcode = passcode
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        """
        Deposit a positive amount into the account.

        Args:
            amount (float): The amount to deposit.

        Raises:
            InvalidAmountError: If the amount is not positive.
        """
        if amount <= 0:
            raise InvalidAmountError("Amount must be positive")
        self.balance += amount
        self.transactions.append(f"Deposited Nu.{amount}")

    def withdraw(self, amount):
        """
        Withdraw a positive amount from the account.

        Args:
            amount (float): The amount to withdraw.

        Raises:
            InvalidAmountError: If the amount is not positive.
            InsufficientFundsError: If the balance is insufficient.
        """
        if amount <= 0:
            raise InvalidAmountError("Amount must be positive")
        if amount > self.balance:
            raise InsufficientFundsError("Not enough balance")
        self.balance -= amount
        self.transactions.append(f"Withdrew Nu.{amount}")

    def transfer(self, amount, target):
        """
        Transfer a positive amount to another account.

        Args:
            amount (float): The amount to transfer.
            target (BankAccount): The target account.

        Raises:
            InvalidAmountError: If the amount is not positive or target is self.
            InsufficientFundsError: If the balance is insufficient.
        """
        if amount <= 0:
            raise InvalidAmountError("Amount must be positive")
        if amount > self.balance:
            raise InsufficientFundsError("Not enough balance")
        if target == self:
            raise InvalidAmountError("Cannot transfer to same account")
        self.balance -= amount
        target.balance += amount
        self.transactions.append(f"Sent Nu.{amount} to {target.name} ({target.account_number})")
        target.transactions.append(f"Received Nu.{amount} from {self.name} ({self.account_number})")

    def mobile_topup(self, amount, number):
        """
        Perform a mobile top-up from the account.

        Args:
            amount (float): The amount to top-up.
            number (str): The mobile number to top-up.

        Raises:
            InvalidAmountError: If the amount is not positive.
            InsufficientFundsError: If the balance is insufficient.
        """
        if amount <= 0:
            raise InvalidAmountError("Amount must be positive")
        if amount > self.balance:
            raise InsufficientFundsError("Not enough balance")
        self.balance -= amount
        self.transactions.append(f"Mobile top-up Nu.{amount} to {number}")

    def get_transactions(self):
        """
        Get the list of transaction descriptions.

        Returns:
            list: List of transaction strings.
        """
        return self.transactions

class BankingApp:
    """
    GUI application for Ace Bank operations using Tkinter.

    Attributes:
        master (tk.Tk): The root Tkinter window.
        accounts (dict): Dictionary of account_number to BankAccount.
        current (BankAccount or None): The currently logged-in account.
    """
    def __init__(self, master):
        """
        Initialize the banking app GUI.

        Args:
            master (tk.Tk): The root Tkinter window.
        """
        self.master = master
        master.title("Ace Bank")
        self.accounts = {}  # key: account_number, value: BankAccount
        self.current = None

        tk.Label(master, text="Welcome to Ace Bank").pack()

        tk.Button(master, text="Open Account", command=self.open_account).pack()
        tk.Button(master, text="Login", command=self.login).pack()

        self.deposit_btn = tk.Button(master, text="Deposit", command=self.deposit, state=tk.DISABLED)
        self.deposit_btn.pack()
        self.withdraw_btn = tk.Button(master, text="Withdraw", command=self.withdraw, state=tk.DISABLED)
        self.withdraw_btn.pack()
        self.transfer_btn = tk.Button(master, text="Send Money", command=self.transfer, state=tk.DISABLED)
        self.transfer_btn.pack()
        self.topup_btn = tk.Button(master, text="Mobile Top-Up", command=self.mobile_topup, state=tk.DISABLED)
        self.topup_btn.pack()
        self.delete_btn = tk.Button(master, text="Close Account", command=self.close_account, state=tk.DISABLED)
        self.delete_btn.pack()

        self.balance_label = tk.Label(master, text="No account selected")
        self.balance_label.pack()

        self.txn_text = tk.Text(master, height=8, width=40, state=tk.DISABLED)
        self.txn_text.pack()

        tk.Button(master, text="Logout", command=self.logout).pack()

    def generate_account_number(self):
        """
        Generate a unique 5-digit account number.

        Returns:
            str: Unique account number.
        """
        while True:
            acc_num = str(random.randint(10000, 99999))
            if acc_num not in self.accounts:
                return acc_num

    def open_account(self):
        """
        Open a new bank account via dialog prompts.
        """
        name = simpledialog.askstring("Open Account", "Enter account holder name:")
        if not name:
            return
        for acc in self.accounts.values():
            if acc.name == name:
                messagebox.showerror("Error", "Account with this name already exists")
                return
        passcode = simpledialog.askstring("Set Passcode", "Set a numeric passcode (min 4 digits):", show="*")
        if not passcode or not passcode.isdigit() or len(passcode) < 4:
            messagebox.showerror("Error", "Invalid passcode. Must be at least 4 digits.")
            return
        bal = simpledialog.askfloat("Open Account", "Enter opening balance (Nu.):", minvalue=0)
        if bal is not None:
            acc_num = self.generate_account_number()
            self.accounts[acc_num] = BankAccount(acc_num, name, passcode, bal)
            messagebox.showinfo("Success", f"Account opened for {name}\nAccount Number: {acc_num}")

    def login(self):
        """
        Log in to an existing account using account number and passcode.
        """
        if not self.accounts:
            messagebox.showerror("Error", "No accounts yet")
            return
        acc_num = simpledialog.askstring("Login", "Enter account number:")
        if acc_num in self.accounts:
            passcode = simpledialog.askstring("Passcode", "Enter your passcode:", show="*")
            if passcode != self.accounts[acc_num].passcode:
                messagebox.showerror("Error", "Incorrect passcode")
                return
            self.current = self.accounts[acc_num]
            self.update_display()
            for btn in [self.deposit_btn, self.withdraw_btn, self.transfer_btn, self.topup_btn, self.delete_btn]:
                btn.config(state=tk.NORMAL)
        else:
            messagebox.showerror("Error", "Account not found")

    def update_display(self):
        """
        Update the GUI display with the current account's balance and transactions.
        """
        if self.current:
            self.balance_label.config(
                text=f"{self.current.name} (Acc: {self.current.account_number}) Balance: Nu.{self.current.balance:.2f}"
            )
            self.txn_text.config(state=tk.NORMAL)
            self.txn_text.delete(1.0, tk.END)
            for t in self.current.transactions:
                self.txn_text.insert(tk.END, f"{t}\n")
            self.txn_text.config(state=tk.DISABLED)

    def deposit(self):
        """
        Prompt for and deposit an amount into the current account.
        """
        amt = simpledialog.askfloat("Deposit", "Enter amount (Nu.):", minvalue=0.01)
        if amt:
            try:
                self.current.deposit(amt)
                self.update_display()
                messagebox.showinfo("Success", f"Deposited Nu.{amt}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def withdraw(self):
        """
        Prompt for and withdraw an amount from the current account.
        """
        amt = simpledialog.askfloat("Withdraw", "Enter amount (Nu.):", minvalue=0.01)
        if amt:
            try:
                self.current.withdraw(amt)
                self.update_display()
                messagebox.showinfo("Success", f"Withdrew Nu.{amt}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def transfer(self):
        """
        Prompt for and transfer an amount to another account.
        """
        if len(self.accounts) < 2:
            messagebox.showerror("Error", "Need at least 2 accounts")
            return
        target_acc_num = simpledialog.askstring("Send Money", "Enter recipient's account number:")
        if target_acc_num and target_acc_num in self.accounts and target_acc_num != self.current.account_number:
            amt = simpledialog.askfloat("Send Money", "Enter amount (Nu.):", minvalue=0.01)
            if amt:
                try:
                    self.current.transfer(amt, self.accounts[target_acc_num])
                    self.update_display()
                    messagebox.showinfo("Success", f"Sent Nu.{amt} to {self.accounts[target_acc_num].name} ({target_acc_num})")
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Invalid recipient account number")

    def mobile_topup(self):
        """
        Prompt for and perform a mobile top-up from the current account.
        """
        number = simpledialog.askstring("Mobile Top-Up", "Enter mobile number:")
        if number:
            amt = simpledialog.askfloat("Mobile Top-Up", "Enter amount (Nu.):", minvalue=0.01)
            if amt:
                try:
                    self.current.mobile_topup(amt, number)
                    self.update_display()
                    messagebox.showinfo("Success", f"Topped up Nu.{amt} to {number}")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

    def close_account(self):
        """
        Close the current account after confirmation.
        """
        if self.current:
            confirm = messagebox.askyesno("Close Account", f"Close account for {self.current.name} ({self.current.account_number})?")
            if confirm:
                del self.accounts[self.current.account_number]
                self.current = None
                self.balance_label.config(text="No account selected")
                self.txn_text.config(state=tk.NORMAL)
                self.txn_text.delete(1.0, tk.END)
                self.txn_text.config(state=tk.DISABLED)
                for btn in [self.deposit_btn, self.withdraw_btn, self.transfer_btn, self.topup_btn, self.delete_btn]:
                    btn.config(state=tk.DISABLED)
                messagebox.showinfo("Success", "Account closed")

    def logout(self):
        """
        Log out from the current account and reset the GUI.
        """
        self.current = None
        self.balance_label.config(text="No account selected")
        self.txn_text.config(state=tk.NORMAL)
        self.txn_text.delete(1.0, tk.END)
        self.txn_text.config(state=tk.DISABLED)
        for btn in [self.deposit_btn, self.withdraw_btn, self.transfer_btn, self.topup_btn, self.delete_btn]:
            btn.config(state=tk.DISABLED)
        messagebox.showinfo("Logout", "You have been logged out.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BankingApp(root)
    root.mainloop()