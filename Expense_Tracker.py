import datetime
from tabulate import tabulate
import csv
import os
expenses = []


def store_data_csv(expenses):
    filename = f"{datetime.date.today().month}.csv"
    fieldnames = list(expenses[0].keys())

    if not expenses:
        print("No expenses to save.")
        return

    file_exists = os.path.exists(filename)

    with open(filename, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write header only if file is new
        if not file_exists:
            writer.writeheader()

        writer.writerows(expenses)

    print(f"Saved {len(expenses)} expenses to {filename}")

        

def summary_of_expense():
    pass


def delete_expense(expenses):
    pass


def update_expense(expenses):
    pass


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
        date_old = input(str("Is this bill spend in today :(y/n) ? : ")).lower()
        if date_old == "n":
            date = input(str("Enter the Date : "))
        else:
            date = datetime.date.today()
        id_num = len(expenses) + 1
        expense = {
            "Id": id_num,
            "Description": description,
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
