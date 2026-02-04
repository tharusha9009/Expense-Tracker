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

    def compare_with_previous_month(self):
        """Compare current month's total with previous month's total.
        Returns a dict with keys: current_total, previous_total, difference, percent_change,
        prev_month_name, prev_exists, status
        """
        today = datetime.date.today()
        # compute previous month (handle January -> December)
        prev_month = today.month - 1 if today.month > 1 else 12
        prev_month_name = calendar.month_name[prev_month]
        prev_filename = f"{prev_month_name}.csv"

        prev_exists = os.path.exists(prev_filename)
        previous_total = 0.0
        if prev_exists:
            with open(prev_filename, "r", newline="") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                if rows:
                    try:
                        previous_total = sum(float(r["Amount"]) for r in rows)
                    except Exception:
                        previous_total = 0.0

        current_summary = self.get_summary_data()
        current_total = current_summary["total_amount"] if current_summary else 0.0

        difference = current_total - previous_total
        percent_change = None
        if previous_total != 0:
            percent_change = (difference / previous_total) * 100

        if not prev_exists:
            status = "no_prev_file"
        else:
            if previous_total == 0 and current_total == 0:
                status = "no_data"
            elif difference > 0:
                status = "increase"
            elif difference < 0:
                status = "decrease"
            else:
                status = "same"

        return {
            "current_total": current_total,
            "previous_total": previous_total,
            "difference": difference,
            "percent_change": percent_change,
            "prev_month_name": prev_month_name,
            "prev_exists": prev_exists,
            "status": status
        }

    def _row_key(self, row):
        """Create a normalized key for a row to detect duplicates."""
        desc = str(row.get("Description", "")).strip()
        etype = str(row.get("Expense_Type", "")).strip()
        try:
            amt = f"{float(row.get('Amount', 0)):.2f}"
        except Exception:
            amt = str(row.get("Amount", "")).strip()
        date = str(row.get("Date", "")).strip()
        return (desc, etype, amt, date)

    def sync_missing_from_previous_months(self):
        """Backward-compatible wrapper that syncs from all months (same behavior as before).
        Returns dict with imported_count and imported list.
        """
        months = [calendar.month_name[m] for m in range(1, 13)]
        return self.perform_sync(months)

    def get_all_monthly_totals(self):
        """Return dict mapping month name to total amount for all month CSV files present."""
        totals = {}
        for m in range(1, 13):
            fname = f"{calendar.month_name[m]}.csv"
            if os.path.exists(fname):
                with open(fname, "r", newline="") as f:
                    reader = csv.DictReader(f)
                    total = 0.0
                    for r in reader:
                        try:
                            total += float(r.get("Amount", 0))
                        except Exception:
                            pass
                    totals[calendar.month_name[m]] = total
        return totals

    def preview_missing_from_previous_months(self, months=None):
        """Return list of rows (dicts) that would be imported from the given months, without writing."""
        current_file = self.filename
        current_rows = self.load_expenses()
        current_keys = {self._row_key(r) for r in current_rows}
        candidates = []

        months_to_check = months if months is not None else [calendar.month_name[m] for m in range(1, 13)]

        for mname in months_to_check:
            fname = f"{mname}.csv"
            if fname == current_file or not os.path.exists(fname):
                continue
            with open(fname, "r", newline="") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    key = self._row_key(r)
                    if key not in current_keys:
                        candidates.append({"from_file": fname, **r})
        return candidates

    def perform_sync(self, months=None):
        """Actually import missing rows from the given months into the current month's file.
        Returns dict with imported_count and imported list (rows written).
        """
        current_file = self.filename
        current_rows = self.load_expenses()
        current_keys = {self._row_key(r) for r in current_rows}
        imported = []

        months_to_check = months if months is not None else [calendar.month_name[m] for m in range(1, 13)]

        for mname in months_to_check:
            fname = f"{mname}.csv"
            if fname == current_file or not os.path.exists(fname):
                continue
            with open(fname, "r", newline="") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    key = self._row_key(r)
                    if key not in current_keys:
                        # assign new ID
                        try:
                            max_id = max(int(x["Id"]) for x in current_rows) if current_rows else 0
                        except Exception:
                            max_id = len(current_rows)
                        new_id = max_id + 1

                        new_row = {
                            "Id": new_id,
                            "Description": r.get("Description", ""),
                            "Expense_Type": r.get("Expense_Type", ""),
                            "Amount": r.get("Amount", "0"),
                            "Date": r.get("Date", "")
                        }

                        with open(current_file, "a", newline="") as cf:
                            writer = csv.DictWriter(cf, fieldnames=["Id", "Description", "Expense_Type", "Amount", "Date"])
                            if os.path.getsize(current_file) == 0:
                                writer.writeheader()
                            writer.writerow(new_row)

                        current_rows.append(new_row)
                        current_keys.add(key)
                        imported.append({"from_file": fname, **new_row})

        return {"imported_count": len(imported), "imported": imported}
