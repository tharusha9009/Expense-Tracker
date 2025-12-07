# Expense Tracker

This project is based on Python programming language.

## Current Features

- Add new expenses with amount, category, and date
- View all recorded expenses
- Filter expenses by category or date
- Edit or delete existing expense entries
- Generate summary reports (monthly/weekly totals)

## Programming Structure

The project follows a modular structure using Object-Oriented Programming (OOP):

```
Expense-Tracker/
├── main.py               # Entry point for the application
├── models/
│   └── expense.py        # Expense class definition
├── controllers/
│   └── tracker.py        # Main logic for tracking expenses
├── utils/
│   └── helpers.py        # Helper functions for data handling
├── data/
│   └── expenses.csv      # Expense data storage
└── README.md
```

- **models/**: Contains data model classes such as `Expense`.
- **controllers/**: Handles core application logic.
- **utils/**: Utility functions, like data validation and formatting.
- **data/**: Stores expense data files.

Feel free to adjust the features and structure to match your actual implementation!