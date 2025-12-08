import datetime
from tabulate import tabulate
import csv
import os
import calendar

expenses = []


def store_data_csv(expenses):
    try:
        if not expenses:
            print("No expenses to save.")
            return

        filename = f"{calendar.month_name[datetime.date.today().month]}.csv"
        fieldnames = list(expenses[0].keys())
        file_exists = os.path.exists(filename)

        # If file exists → read and update IDs
        if file_exists:
            try:
                with open(filename, "r", newline="") as file:
                    reader = csv.DictReader(file)
                    existing_data = list(reader)
            except Exception as e:
                print(f"Error reading existing CSV: {e}")
                existing_data = []

            # Get last ID
            max_id = 0
            try:
                if existing_data:
                    max_id = max(int(row["Id"]) for row in existing_data)
            except Exception:
                print("Warning: Invalid ID found in CSV. Starting ID from 0.")
                max_id = 0

            # Assign new IDs
            for i, expense in enumerate(expenses):
                expense["Id"] = max_id + i + 1

            # Merge old + new
            all_expenses = existing_data + expenses

            # Write back to CSV
            with open(filename, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(all_expenses)

        else:
            # Create new file
            with open(filename, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(expenses)

        print(f"Saved {len(expenses)} expenses to {filename}")

    except PermissionError:
        print("Error: Permission denied. Close the file if it's open.")
    except FileNotFoundError:
        print("Error: Directory not found.")
    except Exception as e:
        print(f"Unexpected error: {e}")


        

def summary_of_expense(filename):
    filename = input(str("Enter the file to check the Summary : "))
    if  os.path.exists(filename):
        with open(filename , "r+") as file:
            lines = file.readlines()
        #print(lines)
        header = lines[0].strip().split(",")
        data = []
        for line  in lines[1:]:
            values = line.strip().split(",")
            row = dict(zip(header, values))
            data.append(row)
        
        if not data:
            print("No expenses found in this file.")
            return
        
        # Calculate basic statistics
        amounts = [float(row["Amount"]) for row in data]
        total_amount = sum(amounts)
        avg_amount = total_amount / len(amounts)
        highest_expense = max(amounts)
        lowest_expense = min(amounts)
        
        # Breakdown by Expense Type
        expense_by_type = {}
        expense_count_by_type = {}
        for row in data:
            exp_type = row["Expense_Type"]
            amount = float(row["Amount"])
            expense_by_type[exp_type] = expense_by_type.get(exp_type, 0) + amount
            expense_count_by_type[exp_type] = expense_count_by_type.get(exp_type, 0) + 1
        
        # Find most frequent category
        most_frequent = max(expense_count_by_type, key=expense_count_by_type.get)
        
        # Get date range
        dates = [row["Date"] for row in data]
        first_date = dates[0]
        last_date = dates[-1]
        
        # Print Summary
        print(f"\n{'='*60}")
        print(f"EXPENSE SUMMARY - {filename}")
        print(f"{'='*60}")
        print(f"\n📊 OVERALL STATISTICS:")
        print(f"  • Total Expenses: {len(data)}")
        print(f"  • Total Amount Spent: ${total_amount:.2f}")
        print(f"  • Average Expense: ${avg_amount:.2f}")
        print(f"  • Highest Expense: ${highest_expense:.2f}")
        print(f"  • Lowest Expense: ${lowest_expense:.2f}")
        print(f"  • Date Range: {first_date} to {last_date}")
        
        print(f"\n💰 BREAKDOWN BY EXPENSE TYPE:")
        for exp_type, amount in sorted(expense_by_type.items(), key=lambda x: x[1], reverse=True):
            count = expense_count_by_type[exp_type]
            percentage = (amount / total_amount) * 100
            print(f"  • {exp_type}: ${amount:.2f} ({count} expenses, {percentage:.1f}%)")
        
        print(f"\n🔝 MOST FREQUENT CATEGORY: {most_frequent} ({expense_count_by_type[most_frequent]} expenses)")
        print(f"{'='*60}\n")
        
    else:
        print(f"The file You Entered does not exist...")
    
    
    
    
 
    
    
    


def delete_expense(filename):
    filename = input(str("Enter the file to Delete expense: "))
    if  os.path.exists(filename):
        with open(filename , "r+") as file:
            lines = file.readlines()
        #print(lines)
        header = lines[0].strip().split(",")
        data = []
        for line  in lines[1:]:
            values = line.strip().split(",")
            row = dict(zip(header, values))
            data.append(row)
        
        # Display expenses with their IDs
        print("\n--- Expenses ---")
        for exp in data:
            print(f"ID: {exp['Id']}, Description: {exp['Description']}, Amount: {exp['Amount']}, Type: {exp['Expense_Type']}, Date: {exp['Date']}")
        
        # Delete Part
        try:
            id_delete = input("Enter ID to delete: ")
            initial_count = len(data)
            data = [exp for exp in data if exp["Id"] != id_delete]
            
            if len(data) < initial_count:
                # Rewrite the file without the deleted expense
                with open(filename, "w", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=header)
                    writer.writeheader()
                    writer.writerows(data)
                print(f"Expense with ID {id_delete} deleted successfully!")
            else:
                print(f"ID {id_delete} not found.")
        except Exception as e:
            print(f"Error: {e}")
        
    else:
        print(f"The file You Entered does not exist...")



def update_expense(filename):
    filename = input(str("Enter the file to Update expense: "))
    if  os.path.exists(filename):
        with open(filename , "r+") as file:
            lines = file.readlines()
        #print(lines)
        header = lines[0].strip().split(",")
        data = []
        for line  in lines[1:]:
            values = line.strip().split(",")
            row = dict(zip(header, values))
            data.append(row)
            # Update Part
            try:
                id_update = input("Enter ID to update : ") 
                for exp in data:
                    if exp["Id"]==id_update:
                        exp["Description"]=input("New Description : ")
                        exp["Amount"]=input("New amount : ")
                        exp["Expense_Type"]=input("New Expense Type : ")
                        exp["Date"]=input("New Date : ")
                    else:
                        print("ID not found")
            except Exception as e:
                print("Error :",e)   
               
    else:
        print(f"The file You Entered does not exsits...")
    
    
    


def View_Expense(expenses):
    if not expenses:
        print("No expenses yet.")
        return

    rows = [list(exp.values()) for exp in expenses]
    headers = expenses[0].keys()
    data = tabulate(rows, headers=headers, tablefmt="grid")
    print(data)
    

def Add_Expense():
    id_num = 0
    while True:
        description = input(str("expense-tracker add --description : "))
        amount = float(input("expense-tracker add --amount : "))
        expense_type = input(str("Enter the type of expense : "))
        date = datetime.date.today()
        id_num = len(expenses) + 1
        expense = {
            "Id": id_num,
            "Description": description,
            "Expense_Type":  expense_type ,
            "Amount": amount,
            "Date": date
        }
        expenses.append(expense)
        #View_Expense(expenses)
        more = input(str("Do you want to add More expenses (y/n) : ")).lower()
        if more == "n":
            break
    
        
         


def main():
    while True:
        try:
            print("Enter the correct Number")
            print(" 1). Add expense ")
            print(" 2). View expense ")
            print(" 3). Update the expense ")
            print(" 4). Delete the expense ")
            print(" 5). Summery of the expense ")
            print(" 6). Store the data to csv ")
            print(" 7). Quit the Program ")                                                                       
            number = int(input("Enter the number : "))
            if number == 1:
                Add_Expense()
            elif number == 2:
                View_Expense(expenses)
            elif number == 3:
                update_expense(expenses)
            elif number == 4:
                delete_expense(expenses)
            elif number == 5:
                summary_of_expense(expenses)
            elif number == 6:
                store_data_csv(expenses)
            elif number == 7:
                break
        except ValueError:
            print("Please enter a valid integer for the menu selection.")
if __name__ == "__main__":
    main()
