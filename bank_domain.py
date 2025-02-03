from datetime import datetime
import json
import os


class BankAccount:
    def __init__(self, account_number, account_holder, balance=0.0):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        try:
            if amount > 0:
                self.balance += amount
                self.record_transaction("Deposit", amount)
                print(f"Deposited ${amount} into account {self.account_number}. New Balance: ${self.balance}")
            else:
                print("Deposit amount must be positive.")
        except Exception as e:
            print(f"Error during deposit: {e}")

    def withdraw(self, amount):
        try:
            if 0 < amount <= self.balance:
                self.balance -= amount
                self.record_transaction("Withdrawal", amount)
                print(f"Withdrew ${amount} from account {self.account_number}. New Balance: ${self.balance}")
            else:
                print("Invalid amount or insufficient balance.")
        except Exception as e:
            print(f"Error during withdrawal: {e}")

    def transfer(self, target_account, amount):
        try:
            if 0 < amount <= self.balance:
                self.withdraw(amount)
                target_account.deposit(amount)
                print(f"Transferred ${amount} to account {target_account.account_number}.")
            else:
                print("Insufficient balance or invalid amount.")
        except Exception as e:
            print(f"Error during transfer: {e}")

    def record_transaction(self, transaction_type, amount):
        try:
            transaction = {
                "type": transaction_type,
                "amount": amount,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.transactions.append(transaction)
        except Exception as e:
            print(f"Error recording transaction: {e}")

    def show_transaction(self):
        try:
            print(f"Transaction History for Account {self.account_number}:")
            for txn in self.transactions:
                print(f"{txn['date']} - {txn['type']}: ${txn['amount']}")
        except Exception as e:
            print(f"Error showing transactions: {e}")

    def to_dict(self):
        return {
            "account_number": self.account_number,
            "account_holder": self.account_holder,
            "balance": self.balance,
            "transactions": self.transactions
        }

    @staticmethod
    def from_dict(data):
        account = BankAccount(data["account_number"], data["account_holder"], data["balance"])
        account.transactions = data["transactions"]
        return account

    @staticmethod
    def save_accounts(accounts, filename="accounts.json"):
        try:
            with open(filename, "w") as file:
                json.dump([acc.to_dict() for acc in accounts], file, indent=4)
            print("Accounts saved successfully.")
        except Exception as e:
            print(f"Error saving accounts: {e}")

    @staticmethod
    def load_accounts(filename="accounts.json"):
        try:
            if os.path.exists(filename):
                with open(filename, "r") as file:
                    data = json.load(file)
                    return [BankAccount.from_dict(acc) for acc in data]
        except json.JSONDecodeError:
            print("Error reading the accounts file, corrupted.")
        except Exception as e:
            print(f"Error loading accounts: {e}")
        return []

    @staticmethod
    def create_accounts(accounts):
        try:
            account_number = input("Enter Account Number: ")
            account_holder = input("Enter Account Holder Name: ")
            balance = float(input("Enter Initial Balance: "))
            new_account = BankAccount(account_number, account_holder, balance)
            accounts.append(new_account)
            print("Account created successfully.")
        except ValueError:
            print("Invalid input. Balance must be a number.")
        except Exception as e:
            print(f"Error creating account: {e}")

    @staticmethod
    def main():
        accounts = BankAccount.load_accounts()

        while True:
            print("\nBanking Application Menu:")
            print("1. Create Account")
            print("2. Deposit")
            print("3. Withdraw")
            print("4. Transfer")
            print("5. Show Transactions")
            print("6. Save and Exit")

            choice = input("Choose an option (1-6): ")

            if choice == "1":
                BankAccount.create_accounts(accounts)
            elif choice == "2":
                acc_number = input("Enter Account Number: ")
                account = next((acc for acc in accounts if acc.account_number == acc_number), None)
                if account:
                    try:
                        amount = float(input("Enter amount to deposit: "))
                        account.deposit(amount)
                    except ValueError:
                        print("Invalid input. Amount must be a number.")
                else:
                    print("Account not found.")
            elif choice == "3":
                acc_number = input("Enter Account Number: ")
                account = next((acc for acc in accounts if acc.account_number == acc_number), None)
                if account:
                    try:
                        amount = float(input("Enter amount to withdraw: "))
                        account.withdraw(amount)
                    except ValueError:
                        print("Invalid input. Amount must be a number.")
                else:
                    print("Account not found.")
            elif choice == "4":
                src_acc_number = input("Enter Your Account Number: ")
                target_acc_number = input("Enter Target Account Number: ")
                src_account = next((acc for acc in accounts if acc.account_number == src_acc_number), None)
                target_account = next((acc for acc in accounts if acc.account_number == target_acc_number), None)
                if src_account and target_account:
                    try:
                        amount = float(input("Enter amount to transfer: "))
                        src_account.transfer(target_account, amount)
                    except ValueError:
                        print("Invalid input. Amount must be a number.")
                else:
                    print("Source or target account not found.")
            elif choice == "5":
                acc_number = input("Enter Account Number: ")
                account = next((acc for acc in accounts if acc.account_number == acc_number), None)
                if account:
                    account.show_transaction()
                else:
                    print("Account not found.")
            elif choice == "6":
                BankAccount.save_accounts(accounts)
                print("Exiting the application. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    BankAccount.main()
