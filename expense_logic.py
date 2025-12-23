import csv
import os
import datetime
import calendar

class ExpenseLogic:
    def __init__(self):
        self.filename = f"{calendar.month_name[datetime.date.today().month]}.csv"
        self.ensure_file_exists()

    def ensure_file_exists(self):
        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=["Id", "Description", "Expense_Type", "Amount", "Date"])
                writer.writeheader()

    def load_expenses(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", newline="") as file:
                reader = csv.DictReader(file)
                return list(reader)
        return []

    def save_expense(self, description, amount, expense_type, date):
        expenses = self.load_expenses()
        
        # Calculate new ID
        max_id = 0
        if expenses:
            try:
                max_id = max(int(row["Id"]) for row in expenses)
            except ValueError:
                max_id = len(expenses) 
        
        new_id = max_id + 1
        
        new_expense = {
            "Id": new_id,
            "Description": description,
            "Expense_Type": expense_type,
            "Amount": amount,
            "Date": date
        }
        
        # Append to file
        with open(self.filename, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Id", "Description", "Expense_Type", "Amount", "Date"])
            if os.path.getsize(self.filename) == 0:
                writer.writeheader()
            writer.writerow(new_expense)
            
        return True, "Expense added successfully"

    def delete_expense(self, expense_id):
        expenses = self.load_expenses()
        initial_count = len(expenses)
        expenses = [exp for exp in expenses if str(exp["Id"]) != str(expense_id)]
        
        if len(expenses) < initial_count:
            self._rewrite_file(expenses)
            return True, f"Expense ID {expense_id} deleted."
        return False, "ID not found."

    def update_expense(self, expense_id, new_data):
        expenses = self.load_expenses()
        updated = False
        for exp in expenses:
            if str(exp["Id"]) == str(expense_id):
                exp.update(new_data)
                updated = True
                break
        
        if updated:
            self._rewrite_file(expenses)
            return True, "Expense updated successfully."
        return False, "ID not found."

    def _rewrite_file(self, expenses):
        with open(self.filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Id", "Description", "Expense_Type", "Amount", "Date"])
            writer.writeheader()
            writer.writerows(expenses)

    def get_summary_data(self):
        expenses = self.load_expenses()
        if not expenses:
            return None
            
        amounts = [float(row["Amount"]) for row in expenses]
        total_amount = sum(amounts)
        
        # Breakdown by Type
        expense_by_type = {}
        for row in expenses:
            exp_type = row["Expense_Type"]
            amount = float(row["Amount"])
            expense_by_type[exp_type] = expense_by_type.get(exp_type, 0) + amount
            
        # Group by Date
        expense_by_date = {} # Dictionary mapping date strings to total amount
        for row in expenses:
             date_str = row["Date"] # Assuming YYYY-MM-DD format from input
             amount = float(row["Amount"])
             # If date format is YYYY-MM-DD
             try:
                 # Group by day for the monthly chart, or passing raw date expenses
                 expense_by_date[date_str] = expense_by_date.get(date_str, 0) + amount
             except:
                 pass

        return {
            "total_amount": total_amount,
            "expense_by_type": expense_by_type,
            "expense_by_date": expense_by_date,
            "count": len(expenses)
        }
