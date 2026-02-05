# Expense Tracker

A comprehensive Expense Tracker application built with Python. Start managing your finances with a modern Graphical User Interface (GUI) or a simple Command Line Interface (CLI).

## Features
- **Modern GUI**: Built with `customtkinter` for a sleek, dark-mode compatible look.
- **Visual Analytics**: Interactive Dashboards with:
    - **Pie Charts**: Visualize spending by category.
    - **Daily Charts**: Track daily spending habits.
- **Theme Switching**: Toggle between Light and Dark modes.
- **Data Persistence**: Automatically parses and saves data to monthly CSV files.
- **CRUD Operations**: Add, View, Update, and Delete expenses easily.

## Installation

1. Clone the repository or download the source code.
2. Install the required dependencies:
   ```bash
   pip install customtkinter matplotlib packaging
   ```

## Usage

### GUI Application (Recommended)
Run the modern GUI version:
```bash
python Expense_Tracker_GUI.py
```
- Use the sidebar to navigate between the Dashboard, Add Expense, and View Expense pages.
- Change Appearance Mode (Light/Dark) from the sidebar.

### CLI Application
Run the classic command-line version:
```bash
python Expense_Tracker.py
```

## Structure
- `Expense_Tracker_GUI.py`: The main entry point for the GUI.
- `Expense_Tracker.py`: The classic CLI application.
- `expense_logic.py`: Core logic handling CSV operations (shared).
- `[Month].csv`: Data storage files (generated automatically).

## Requirements
- Python 3.x
- `customtkinter`
- `matplotlib`
