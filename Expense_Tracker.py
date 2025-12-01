import datetime
from tabulate import tabulate

expenses = []


def store_data_csv(expenses):
    
                                      # Write  the   csv file file 
                                      # Append the  expenses to the file
    
    
    pass
    

def summary_of_expense():
                                       # Show the total calculation of the month 
    pass
    
    
def delete_expense(expenses):
                                        # search  the  relevent file and read the file 
    
   pass
    
def update_expense(expenses):
    while True:
        update_input = input(str("Do You Want to Update the file")).lower()
        if update_input =="y":
            update_exp = dict(expenses)
            update_date = input(str("Enter the Date : "))
            
            # update the csv file
        else:
            main()
            break# Update the relevent file 
    
    


def View_Expense(expenses):
    if not expenses:
        print("No expenses yet.")
        return

    rows = [list(exp.values()) for exp in expenses]
    headers = expenses[0].keys()
    data =tabulate(rows, headers=headers, tablefmt="grid")
    print(data)
    

    
    
    
    
    
def Add_Expense():
    id_num = 0
    while True:
        description =input(str("expense-tracker add --description : "))
        amount =int(input("expense-tracker add --amount : "))
        date_old =input(str("Is this bill spend in today :(y/n) ? : ")).lower()
        if date_old=="n":
            date = input(str("Enter the Date : "))
        else:
            date = datetime.date.today()
        id_num = len(expenses)+1
        #print(id_num)
        expense ={
            "Id":id_num,
            "Description":description,
            "Amount":amount,
            "Date":date
        }
        
        expenses.append(expense)
        #View_Expense(expenses)
        more = input(str("Do you want to add More expenses (y/n) : ")).lower()
        if more == "n":
            main()
            break
#def menu()             

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
             
            number= int(input("Enter the number : "))
    
            if number ==1:
                Add_Expense()
            elif number ==2:
                View_Expense(expenses)
            elif number ==3:
                update_expense(expenses)
            elif number ==4:
                delete_expense(expenses)
            elif number ==5:
                summary_of_expense(expenses)
            elif number ==6:
                store_data_csv(expenses) 
            elif number ==7:
                break
        except:
            print("Enter the correct Number!!!!!!!!!!!!!!!!!!!!!!!!!!")
main()    
    