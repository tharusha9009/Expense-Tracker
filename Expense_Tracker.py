import datetime
from tabulate import tabulate
import csv
import os
import calendar

expenses = []
#print(expenses)

def store_data_csv(expenses):
    filename = f"{calendar.month_name[datetime.date.today().month]}.csv"
    fieldnames = list(expenses[0].keys())
    if not expenses:
        print("No expenses to save.")
        return
    else:
        file_exists = os.path.exists(filename)
        with open(filename, "a+", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
           

          # Write header only if file is new
            if not file_exists:
                writer.writeheader()
                writer.writerows(expenses)
            else:
                writer.writerows(expenses)
                summary_of_expense(filename)
        print(f"Saved {len(expenses)} expenses to {filename}")

        

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
        
        outcomes = {
            "Total_Expense":0,
            "Total_amount":0
            
        }
        outcomes["Total_Expense"] = len(data)
        total_amount = sum(float(row["Amount"]) for row in data)
        outcomes["Total_amount"] = total_amount
        
        
        print(f"----------- Summary of the {filename}----------------------")
        print(f"Total expense amount for this  moment : {outcomes["Total_amount"]}")        
        print(f"Total number of expenses : {outcomes["Total_Expense"]}")
        
    else:
        print(f"The file You Entered does not exsits...")
    
    
    
    
 
    
    
    


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
        # Delete Part
        
        
        
        
    else:
        print(f"The file You Entered does not exsits...")



def update_expense(filename):
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
            # Update Part
       
        
        
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
            main()
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
            print(" 7). Quit the Data ")                                                                       
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
