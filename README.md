# Expense Tracker

A simple expense tracker written in Python to record, view, filter, and summarize personal expenses.

## Features

- Add new expenses with amount, category, and date
- View all recorded expenses
- Filter expenses by category or date
- Edit or delete existing expense entries
- Generate summary reports (monthly/weekly totals)
- Simple CSV-backed storage for portability

## Quick Start

Requirements:
- Python 3.8+
- (Optional) Create a virtual environment

Install dependencies (if any):
```bash
pip install -r requirements.txt
```

Run the app:
```bash
python main.py
```

## Project Structure

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
│   └── expenses.csv      # Expense data storage (CSV)
├── requirements.txt      # Python dependencies (optional)
└── README.md
```

## Data format (expenses.csv)

Expected CSV columns (example header):
```
id,amount,category,date,notes
1,12.50,Food,2025-08-03,Lunch at cafe
2,45.00,Transport,2025-08-04,Monthly pass
```

- `id`: unique identifier
- `amount`: numeric value (use dot for decimals)
- `category`: category name (Food, Transport, Bills, etc.)
- `date`: ISO format `YYYY-MM-DD`
- `notes`: optional

## Usage examples

- Add a new expense:
  - Run the app and follow prompts to enter amount, category, date, and notes.
- View expenses:
  - Use the "view" command or option in the app to list stored expenses.
- Filter:
  - Use built-in filters to see expenses by category or date range.
- Edit/Delete:
  - Select an expense by ID to edit or delete it.
- Generate summary:
  - Choose the summary option to see totals grouped by week or month.

(Adjust these examples to match your CLI/menu design in `main.py`.)

## Development

- Run tests (if present):
```bash
pytest
```
- Add or edit functionality under `models/`, `controllers/`, and `utils/`.
- Keep `data/expenses.csv` backed up—it's the primary storage.

## Contributing

Contributions are welcome. Suggested workflow:
1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Add tests and implement your change
4. Open a pull request describing your changes

## License

Add a LICENSE file to clearly indicate the project license (MIT, Apache-2.0, etc.).

## Contact

Maintainer: tharusha9009