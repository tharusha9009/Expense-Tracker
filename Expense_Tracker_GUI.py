import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
from expense_logic import ExpenseLogic
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import datetime

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class ExpenseTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.logic = ExpenseLogic()
        
        self.title("Expense Tracker")
        self.geometry("1100x700")
        
        # Grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.create_sidebar()
        self.create_main_frames()
        
        self.show_frame("dashboard") # Show dashboard by default

    def create_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Expense Tracker", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.sidebar_button_1 = ctk.CTkButton(self.sidebar_frame, text="Dashboard", command=lambda: self.show_frame("dashboard"))
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        
        self.sidebar_button_2 = ctk.CTkButton(self.sidebar_frame, text="Add Expense", command=lambda: self.show_frame("add_expense"))
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        
        self.sidebar_button_3 = ctk.CTkButton(self.sidebar_frame, text="View Expenses", command=lambda: self.show_frame("view_expenses"))
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        self.scaling_label = ctk.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # Set Defaults
        self.appearance_mode_optionemenu.set("System")
        self.scaling_optionemenu.set("100%")

    def create_main_frames(self):
        # Dashboard Frame
        self.dashboard_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        
        # Add Expense Frame
        self.add_expense_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.setup_add_expense_ui()
        
        # View Expenses Frame
        self.view_expenses_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.setup_view_expenses_ui()

    def show_frame(self, name):
        # Hide all
        self.dashboard_frame.grid_forget()
        self.add_expense_frame.grid_forget()
        self.view_expenses_frame.grid_forget()
        
        if name == "dashboard":
            self.dashboard_frame.grid(row=0, column=1, sticky="nsew")
            self.update_dashboard()
        elif name == "add_expense":
            self.add_expense_frame.grid(row=0, column=1, sticky="nsew")
        elif name == "view_expenses":
            self.view_expenses_frame.grid(row=0, column=1, sticky="nsew")
            self.refresh_expense_list()

    # --- Add Expense UI ---
    def setup_add_expense_ui(self):
        self.add_label = ctk.CTkLabel(self.add_expense_frame, text="Add New Expense", font=ctk.CTkFont(size=24))
        self.add_label.pack(pady=20)
        
        self.desc_entry = ctk.CTkEntry(self.add_expense_frame, placeholder_text="Description", width=300)
        self.desc_entry.pack(pady=10)
        
        self.amount_entry = ctk.CTkEntry(self.add_expense_frame, placeholder_text="Amount", width=300)
        self.amount_entry.pack(pady=10)
        
        self.type_entry = ctk.CTkEntry(self.add_expense_frame, placeholder_text="Category (e.g., Food, Travel)", width=300)
        self.type_entry.pack(pady=10)
        
        self.date_entry = ctk.CTkEntry(self.add_expense_frame, placeholder_text="Date (YYYY-MM-DD)", width=300)
        self.date_entry.insert(0, str(datetime.date.today()))
        self.date_entry.pack(pady=10)
        
        self.add_btn = ctk.CTkButton(self.add_expense_frame, text="Save Expense", command=self.save_expense_action)
        self.add_btn.pack(pady=20)

    def save_expense_action(self):
        desc = self.desc_entry.get()
        amount = self.amount_entry.get()
        cat = self.type_entry.get()
        date = self.date_entry.get()
        
        if not desc or not amount or not cat or not date:
            messagebox.showerror("Error", "All fields are required!")
            return
            
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number!")
            return
            
        success, msg = self.logic.save_expense(desc, amount, cat, date)
        if success:
            messagebox.showinfo("Success", msg)
            self.desc_entry.delete(0, "end")
            self.amount_entry.delete(0, "end")
            self.type_entry.delete(0, "end")
        else:
            messagebox.showerror("Error", msg)

    # --- View Expenses UI ---
    def setup_view_expenses_ui(self):
        self.view_label = ctk.CTkLabel(self.view_expenses_frame, text="All Expenses", font=ctk.CTkFont(size=24))
        self.view_label.pack(pady=10)
        
        # Treeview Scrollbar
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", 
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=25,
                        fieldbackground="#343638",
                        bordercolor="#343638",
                        borderwidth=0)
        style.map('Treeview', background=[('selected', '#22559b')])
        
        style.configure("Treeview.Heading",
                        background="#565b5e",
                        foreground="white",
                        relief="flat")
        style.map("Treeview.Heading",
                  background=[('active', '#3484F0')])
        
        self.tree_frame = ctk.CTkFrame(self.view_expenses_frame)
        self.tree_frame.pack(pady=10, fill="both", expand=True, padx=20)
        
        columns = ("Id", "Description", "Type", "Amount", "Date")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
            
        self.tree.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Buttons
        self.btn_frame = ctk.CTkFrame(self.view_expenses_frame, fg_color="transparent")
        self.btn_frame.pack(pady=10)
        
        self.refresh_btn = ctk.CTkButton(self.btn_frame, text="Refresh", command=self.refresh_expense_list)
        self.refresh_btn.pack(side="left", padx=10)
        
        self.delete_btn = ctk.CTkButton(self.btn_frame, text="Delete Selected", fg_color="red", hover_color="darkred", command=self.delete_selected_action)
        self.delete_btn.pack(side="left", padx=10)

    def refresh_expense_list(self):
        # clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        expenses = self.logic.load_expenses()
        for exp in expenses:
            self.tree.insert("", "end", values=(exp["Id"], exp["Description"], exp["Expense_Type"], f"${exp['Amount']}", exp["Date"]))

    def delete_selected_action(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No expense selected")
            return
            
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this expense?")
        if confirm:
            item = self.tree.item(selected[0])
            exp_id = item['values'][0]
            self.logic.delete_expense(exp_id)
            self.refresh_expense_list()

    # --- Dashboard UI ---
    def update_dashboard(self):
        # clear existing widgets in dashboard frame
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        data = self.logic.get_summary_data()
        
        if not data:
            lbl = ctk.CTkLabel(self.dashboard_frame, text="No Data Available", font=ctk.CTkFont(size=20))
            lbl.pack(expand=True)
            return

        # Top Stats
        stats_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        stats_frame.pack(fill="x", pady=10, padx=10)
        
        total_lbl = ctk.CTkLabel(stats_frame, text=f"Total Expenses: ${data['total_amount']:.2f}", font=ctk.CTkFont(size=18, weight="bold"))
        total_lbl.pack(side="left", padx=20)
        
        count_lbl = ctk.CTkLabel(stats_frame, text=f"Total Transactions: {data['count']}", font=ctk.CTkFont(size=18))
        count_lbl.pack(side="left", padx=20)

        # Charts Area
        charts_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        charts_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 1. Pie Chart - Category Distribution
        fig1, ax1 = plt.subplots(figsize=(5, 4))
        fig1.patch.set_facecolor('#242424') # Dark background match
        ax1.set_facecolor('#242424')
        
        types = list(data["expense_by_type"].keys())
        amounts = list(data["expense_by_type"].values())
        
        wedges, texts, autotexts = ax1.pie(amounts, labels=types, autopct='%1.1f%%', startangle=90, textprops={'color':"white"})
        ax1.axis('equal')
        ax1.set_title("Expenses by Category", color='white')
        
        canvas1 = FigureCanvasTkAgg(fig1, master=charts_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side="left", fill="both", expand=True, padx=5)

        # 2. Bar Chart - Daily Expenses (or just transactions if single month)
        # Using date keys
        fig2, ax2 = plt.subplots(figsize=(5, 4))
        fig2.patch.set_facecolor('#242424')
        ax2.set_facecolor('#242424')
        
        dates = list(data["expense_by_date"].keys())
        daily_amounts = list(data["expense_by_date"].values())
        
        # Sort by date
        sorted_pairs = sorted(zip(dates, daily_amounts))
        if sorted_pairs:
            dates, daily_amounts = zip(*sorted_pairs)
            
        ax2.bar(dates, daily_amounts, color='#1f6aa5')
        ax2.tick_params(axis='x', colors='white', rotation=45)
        ax2.tick_params(axis='y', colors='white')
        ax2.set_title("Daily Expenses", color='white')
        
        # Adjust layout for rotation
        fig2.tight_layout()
        
        canvas2 = FigureCanvasTkAgg(fig2, master=charts_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side="right", fill="both", expand=True, padx=5)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
        # Re-draw charts to match theme if needed, but simple re-navigation to dashboard works 
        # or we can force update. Ideally we'd update plotting colors too.
        if self.dashboard_frame.winfo_ismapped():
            self.update_dashboard()

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)


if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.mainloop()
