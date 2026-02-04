import customtkinter as ctk
from tkinter import messagebox, ttk, filedialog
import tkinter as tk
from expense_logic import ExpenseLogic
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt 
import datetime
import calendar
import csv

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

        # New: Current Month Expenses
        self.sidebar_button_current = ctk.CTkButton(self.sidebar_frame, text="Current Month Expense", command=lambda: self.show_frame("current"))
        self.sidebar_button_current.grid(row=4, column=0, padx=20, pady=10)

        self.sidebar_button_4 = ctk.CTkButton(self.sidebar_frame, text="Monthly Comparison", command=lambda: self.show_frame("monthly"))
        self.sidebar_button_4.grid(row=5, column=0, padx=20, pady=10)

        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 10))

        self.scaling_label = ctk.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 20))

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

        # Current Month Frame
        self.current_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.setup_current_month_ui()

        # Monthly Comparison Frame
        self.monthly_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.setup_monthly_ui()

    def show_frame(self, name):
        # Hide all
        self.dashboard_frame.grid_forget()
        self.add_expense_frame.grid_forget()
        self.view_expenses_frame.grid_forget()
        self.current_frame.grid_forget()
        self.monthly_frame.grid_forget()
        
        if name == "dashboard":
            self.dashboard_frame.grid(row=0, column=1, sticky="nsew")
            self.update_dashboard()
        elif name == "add_expense":
            self.add_expense_frame.grid(row=0, column=1, sticky="nsew")
        elif name == "view_expenses":
            self.view_expenses_frame.grid(row=0, column=1, sticky="nsew")
            self.refresh_expense_list()
        elif name == "current":
            self.current_frame.grid(row=0, column=1, sticky="nsew")
            self.refresh_current_list()
        elif name == "monthly":
            self.monthly_frame.grid(row=0, column=1, sticky="nsew")
            self.update_monthly_view()

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

    # --- Current Month UI ---
    def setup_current_month_ui(self):
        self.current_label = ctk.CTkLabel(self.current_frame, text="Current Month Expenses", font=ctk.CTkFont(size=24))
        self.current_label.pack(pady=10)

        self.current_tree_frame = ctk.CTkFrame(self.current_frame)
        self.current_tree_frame.pack(padx=20, pady=10, fill="both", expand=True)

        cols = ("Id", "Description", "Type", "Amount", "Date")
        self.current_tree = ttk.Treeview(self.current_tree_frame, columns=cols, show="headings")
        for col in cols:
            self.current_tree.heading(col, text=col)
            self.current_tree.column(col, width=120)
        self.current_tree.pack(side="left", fill="both", expand=True)

        current_scroll = ttk.Scrollbar(self.current_tree_frame, orient="vertical", command=self.current_tree.yview)
        current_scroll.pack(side="right", fill="y")
        self.current_tree.configure(yscrollcommand=current_scroll.set)

        # Filters and Buttons
        self.current_btn_frame = ctk.CTkFrame(self.current_frame, fg_color="transparent")
        self.current_btn_frame.pack(pady=10, fill="x", padx=10)

        # Search box
        self.search_var = tk.StringVar()
        self.search_entry = ctk.CTkEntry(self.current_btn_frame, placeholder_text="Search description...", textvariable=self.search_var, width=300)
        self.search_entry.pack(side="left", padx=(0,10))
        self.search_entry.bind("<KeyRelease>", lambda e: self.refresh_current_list())

        # Category filter (populated dynamically)
        self.category_var = tk.StringVar(value="All")
        self.category_option = ctk.CTkOptionMenu(self.current_btn_frame, values=["All"], command=lambda v: self.refresh_current_list())
        self.category_option.pack(side="left", padx=(0,10))

        self.current_refresh_btn = ctk.CTkButton(self.current_btn_frame, text="Refresh", command=self.refresh_current_list)
        self.current_refresh_btn.pack(side="left", padx=10)

        self.current_delete_btn = ctk.CTkButton(self.current_btn_frame, text="Delete Selected", fg_color="red", hover_color="darkred", command=self.delete_current_selected_action)
        self.current_delete_btn.pack(side="left", padx=10)

        # Export current view to CSV
        self.export_btn = ctk.CTkButton(self.current_btn_frame, text="Export Current Month", command=self.export_current_month_action)
        self.export_btn.pack(side="right", padx=10)

    def refresh_current_list(self):
        # Clear tree
        for item in self.current_tree.get_children():
            self.current_tree.delete(item)

        # Load and apply filters
        expenses = self.logic.load_expenses()
        search = self.search_var.get().strip().lower() if hasattr(self, 'search_var') else ''
        selected_cat = self.category_var.get() if hasattr(self, 'category_var') else 'All'

        # Gather categories for the filter dropdown
        categories = set()
        for exp in expenses:
            categories.add(exp.get("Expense_Type", "").strip())

        # Update category option values (keep 'All' at front)
        vals = ["All"] + sorted([c for c in categories if c])
        try:
            # Avoid resetting selection if already set
            current_val = self.category_var.get()
        except Exception:
            current_val = "All"
        self.category_option.configure(values=vals)
        if current_val in vals:
            self.category_var.set(current_val)
        else:
            self.category_var.set("All")

        for exp in expenses:
            desc = exp.get("Description", "").lower()
            cat = exp.get("Expense_Type", "")
            if search and search not in desc:
                continue
            if selected_cat != "All" and cat != selected_cat:
                continue
            self.current_tree.insert("", "end", values=(exp["Id"], exp["Description"], exp["Expense_Type"], f"${exp['Amount']}", exp["Date"]))

    def delete_current_selected_action(self):
        selected = self.current_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No expense selected")
            return
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this expense?")
        if confirm:
            item = self.current_tree.item(selected[0])
            exp_id = item['values'][0]
            self.logic.delete_expense(exp_id)
            self.refresh_current_list()

    def export_current_month_action(self):
        # Export the currently displayed rows to CSV
        rows = []
        for item in self.current_tree.get_children():
            vals = self.current_tree.item(item)['values']
            # Id, Description, Type, Amount(with $), Date
            amt = str(vals[3]).lstrip('$')
            rows.append({"Id": vals[0], "Description": vals[1], "Expense_Type": vals[2], "Amount": amt, "Date": vals[4]})

        if not rows:
            messagebox.showinfo("Export", "No rows to export.")
            return

        fpath = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files', '*.csv')], title='Save current month export as')
        if not fpath:
            return

        try:
            with open(fpath, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=["Id", "Description", "Expense_Type", "Amount", "Date"])
                writer.writeheader()
                writer.writerows(rows)
            messagebox.showinfo("Export", f"Exported {len(rows)} rows to {fpath}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export: {e}")

    # --- Monthly Comparison UI ---
    def setup_monthly_ui(self):
        self.monthly_label = ctk.CTkLabel(self.monthly_frame, text="Monthly Comparison", font=ctk.CTkFont(size=24))
        self.monthly_label.pack(pady=10)

        self.monthly_stats_frame = ctk.CTkFrame(self.monthly_frame, fg_color="transparent")
        self.monthly_stats_frame.pack(fill="x", pady=10, padx=10)

        self.monthly_total_lbl = ctk.CTkLabel(self.monthly_stats_frame, text="", font=ctk.CTkFont(size=18, weight="bold"))
        self.monthly_total_lbl.pack(side="left", padx=20)

        self.monthly_prev_lbl = ctk.CTkLabel(self.monthly_stats_frame, text="", font=ctk.CTkFont(size=16))
        self.monthly_prev_lbl.pack(side="left", padx=20)

        self.monthly_change_lbl = ctk.CTkLabel(self.monthly_stats_frame, text="", font=ctk.CTkFont(size=16))
        self.monthly_change_lbl.pack(side="left", padx=20)

        # Selection and preview area
        self.months_selection_frame = ctk.CTkFrame(self.monthly_frame, fg_color="transparent")
        self.months_selection_frame.pack(fill="x", pady=(0,10), padx=10)

        self.months_label = ctk.CTkLabel(self.months_selection_frame, text="Select months to sync:")
        self.months_label.pack(anchor='w', padx=10)

        self.months_check_frame = ctk.CTkFrame(self.months_selection_frame, fg_color="transparent")
        self.months_check_frame.pack(fill="x", padx=10, pady=5)

        # will populate checkboxes dynamically in update_monthly_view
        self.month_check_vars = {}

        btns_frame = ctk.CTkFrame(self.months_selection_frame, fg_color="transparent")
        btns_frame.pack(fill="x", padx=10)

        self.preview_btn = ctk.CTkButton(btns_frame, text="Preview Imports", command=self.preview_imports_action)
        self.preview_btn.pack(side="left", padx=(0,10))

        self.perform_sync_btn = ctk.CTkButton(btns_frame, text="Sync Selected", command=self.perform_sync_action)
        self.perform_sync_btn.pack(side="left")

        # Preview Tree
        self.preview_frame = ctk.CTkFrame(self.monthly_frame, fg_color="transparent")
        self.preview_frame.pack(fill="both", expand=False, padx=10, pady=(5,10))

        cols = ("From File", "Description", "Type", "Amount", "Date")
        self.import_preview_tree = ttk.Treeview(self.preview_frame, columns=cols, show='headings', height=6)
        for c in cols:
            self.import_preview_tree.heading(c, text=c)
            self.import_preview_tree.column(c, width=140)
        self.import_preview_tree.pack(side="left", fill="both", expand=True)

        preview_scroll = ttk.Scrollbar(self.preview_frame, orient="vertical", command=self.import_preview_tree.yview)
        preview_scroll.pack(side="right", fill="y")
        self.import_preview_tree.configure(yscrollcommand=preview_scroll.set)

        self.monthly_chart_frame = ctk.CTkFrame(self.monthly_frame, fg_color="transparent")
        self.monthly_chart_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def get_available_months(self):
        # Return list of month names that have CSV files (excluding current month)
        files = self.logic.get_all_monthly_totals()
        current_month = calendar.month_name[datetime.date.today().month]
        months = [m for m in calendar.month_name[1:] if (m in files and m != current_month)]
        return months

    def preview_imports_action(self):
        # gather selected months
        selected = [m for m, var in self.month_check_vars.items() if var.get()]
        if not selected:
            messagebox.showwarning("No Months Selected", "Please select at least one month to preview.")
            return

        # preview via logic
        preview_rows = self.logic.preview_missing_from_previous_months(months=selected)

        # clear tree
        for item in self.import_preview_tree.get_children():
            self.import_preview_tree.delete(item)

        if not preview_rows:
            messagebox.showinfo("Preview", "No missing entries found for the selected months.")
            self.perform_sync_btn.configure(state="disabled")
            return

        for r in preview_rows:
            self.import_preview_tree.insert("", "end", values=(r.get("from_file"), r.get("Description"), r.get("Expense_Type"), f"${r.get('Amount')}", r.get("Date")))

        self.perform_sync_btn.configure(state="normal")

    def perform_sync_action(self):
        selected = [m for m, var in self.month_check_vars.items() if var.get()]
        if not selected:
            messagebox.showwarning("No Months Selected", "Please select at least one month to sync.")
            return

        preview_rows = self.logic.preview_missing_from_previous_months(months=selected)
        if not preview_rows:
            messagebox.showinfo("Sync", "No missing entries to import for selected months.")
            return

        confirm = messagebox.askyesno("Confirm Sync", f"This will import {len(preview_rows)} entries into the current month's file. Continue?")
        if not confirm:
            return

        result = self.logic.perform_sync(selected)
        cnt = result.get("imported_count", 0)
        messagebox.showinfo("Sync Complete", f"Imported {cnt} missing expenses into current month.")

        # Clear preview and disable sync
        for item in self.import_preview_tree.get_children():
            self.import_preview_tree.delete(item)
        self.perform_sync_btn.configure(state="disabled")

        # Refresh UI
        if self.monthly_frame.winfo_ismapped():
            self.update_monthly_view()
        if self.view_expenses_frame.winfo_ismapped():
            self.refresh_expense_list()

    def update_monthly_view(self):
        # Clear chart area
        for widget in self.monthly_chart_frame.winfo_children():
            widget.destroy()

        comp = self.logic.compare_with_previous_month()
        self.monthly_total_lbl.configure(text=f"Current Total: ${comp['current_total']:.2f}")
        if comp['prev_exists']:
            self.monthly_prev_lbl.configure(text=f"Prev ({comp['prev_month_name']}): ${comp['previous_total']:.2f}")
            if comp['percent_change'] is None:
                self.monthly_change_lbl.configure(text="Change: N/A", text_color="gray")
            else:
                sign = "+" if comp['difference'] > 0 else ""
                pct = comp['percent_change']
                change_text = f"Change: {sign}{pct:.1f}% ({sign}${comp['difference']:.2f})"
                change_color = "green" if comp['difference'] < 0 else ("red" if comp['difference'] > 0 else "white")
                self.monthly_change_lbl.configure(text=change_text, text_color=change_color)
        else:
            self.monthly_prev_lbl.configure(text="No data for previous month")
            self.monthly_change_lbl.configure(text="")

        # populate month checkboxes
        months = self.get_available_months()
        # clear previous checkboxes
        for widget in self.months_check_frame.winfo_children():
            widget.destroy()
        self.month_check_vars = {}
        for m in months:
            var = tk.BooleanVar(value=False)
            cb = ctk.CTkCheckBox(self.months_check_frame, text=m, variable=var)
            cb.pack(side="left", padx=5)
            self.month_check_vars[m] = var

        monthly_totals = self.logic.get_all_monthly_totals()
        if monthly_totals:
            months_present = [m for m in calendar.month_name[1:] if m in monthly_totals]
            totals = [monthly_totals[m] for m in months_present]
            fig, ax = plt.subplots(figsize=(8, 3))
            fig.patch.set_facecolor('#242424')
            ax.set_facecolor('#242424')
            # Highlight current month
            current = calendar.month_name[datetime.date.today().month]
            colors = ['#ff7f0e' if m == current else '#2ca02c' for m in months_present]
            ax.bar(months_present, totals, color=colors)
            ax.tick_params(axis='x', colors='white', rotation=45)
            ax.tick_params(axis='y', colors='white')
            ax.set_title("Monthly Totals", color='white')
            fig.tight_layout()
            canvas = FigureCanvasTkAgg(fig, master=self.monthly_chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)



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

        # (Monthly comparison moved to the 'Monthly Comparison' view)

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



    def sync_previous_months_action(self):
        result = self.logic.sync_missing_from_previous_months()
        count = result.get("imported_count", 0)
        if count > 0:
            messagebox.showinfo("Sync Complete", f"Imported {count} missing expenses into current month.")
        else:
            messagebox.showinfo("Sync Complete", "No missing expenses found.")
        # Refresh the UI
        if self.dashboard_frame.winfo_ismapped():
            self.update_dashboard()
        if self.view_expenses_frame.winfo_ismapped():
            self.refresh_expense_list()

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


