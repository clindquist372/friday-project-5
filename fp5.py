import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

class DatabaseManager:
    """Handles all SQLite database operations."""
    def __init__(self, db_name="customer_data.db"):
        self.conn = None
        self.cursor = None
        self.db_name = db_name
        self._connect()

    def _connect(self):
        """Connects to the database and creates the table if it doesn't exist."""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            self._create_table()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Could not connect to database: {e}")

    def _create_table(self):
        """Creates the customer table with required fields."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                birthday TEXT,
                email TEXT,
                phone TEXT,
                address TEXT,
                contact_method TEXT
            )
        ''')
        self.conn.commit()

    def insert_customer(self, data):
        """Inserts a new customer record into the database."""
        try:
            sql = '''
                INSERT INTO customers (name, birthday, email, phone, address, contact_method)
                VALUES (?, ?, ?, ?, ?, ?)
            '''
            self.cursor.execute(sql, (
                data['name'], 
                data['birthday'], 
                data['email'], 
                data['phone'], 
                data['address'], 
                data['contact_method']
            ))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to insert data: {e}")
            self.conn.rollback()
            return False

    def close(self):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()

class CustomerApp(tk.Tk):
    """Main application window for the Customer Information Manager."""
    def __init__(self):
        super().__init__()
        self.title("Customer Information Submission")
        self.db_manager = DatabaseManager()
        self.protocol("WM_DELETE_WINDOW", self.on_closing) # Handle window close

        # Configure style for better appearance
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TButton', font=('Inter', 10, 'bold'), padding=6, foreground='white', background='#4a90e2')
        style.map('TButton', background=[('active', '#357ae8')])
        
        # Setup the main frame with padding and responsiveness
        main_frame = ttk.Frame(self, padding="20 20 20 20")
        main_frame.pack(fill='both', expand=True)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        main_frame.grid_columnconfigure(1, weight=1) # Make the input column expand

        self.create_widgets(main_frame)
        self.center_window()

    def center_window(self):
        """Centers the main window on the screen."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self, frame):
        """Creates and lays out all GUI components."""
        
        fields = [
            ("Name:", "name_var"),
            ("Birthday (YYYY-MM-DD):", "birthday_var"),
            ("Email:", "email_var"),
            ("Phone Number:", "phone_var"),
            ("Address:", "address_var")
        ]
        
        self.entry_vars = {}
        row = 0
        
        # Title Label
        title_label = ttk.Label(frame, text="New Customer Registration", font=('Inter', 16, 'bold'), foreground='#4a90e2')
        title_label.grid(row=row, column=0, columnspan=2, pady=(0, 15), sticky='w')
        row += 1

        # Input Fields (Labels and Entries)
        for label_text, var_name in fields:
            label = ttk.Label(frame, text=label_text, font=('Inter', 10))
            label.grid(row=row, column=0, sticky='w', pady=5, padx=(0, 10))
            
            var = tk.StringVar(self)
            entry = ttk.Entry(frame, textvariable=var, width=50, font=('Inter', 10))
            entry.grid(row=row, column=1, sticky='ew', pady=5)
            
            self.entry_vars[var_name] = var
            row += 1

        # Preferred Contact Method Dropdown
        contact_label = ttk.Label(frame, text="Preferred Contact:", font=('Inter', 10))
        contact_label.grid(row=row, column=0, sticky='w', pady=5, padx=(0, 10))
        
        self.entry_vars["contact_method_var"] = tk.StringVar(self)
        contact_options = ["Email", "Phone", "Mail"]
        
        self.contact_dropdown = ttk.Combobox(
            frame, 
            textvariable=self.entry_vars["contact_method_var"], 
            values=contact_options, 
            state='readonly', # Prevents free typing
            width=48,
            font=('Inter', 10)
        )
        self.contact_dropdown.set(contact_options[0]) # Default value
        self.contact_dropdown.grid(row=row, column=1, sticky='ew', pady=5)
        row += 1
        
        # Spacer row
        row += 1

        # Submit Button
        submit_button = ttk.Button(
            frame, 
            text="Submit Customer Data", 
            command=self.submit_data, 
            style='TButton'
        )
        submit_button.grid(row=row, column=0, columnspan=2, pady=(20, 0), sticky='ew')

    def submit_data(self):
        """Validates input, saves data to DB, and clears the form."""
        data = {
            'name': self.entry_vars['name_var'].get().strip(),
            'birthday': self.entry_vars['birthday_var'].get().strip(),
            'email': self.entry_vars['email_var'].get().strip(),
            'phone': self.entry_vars['phone_var'].get().strip(),
            'address': self.entry_vars['address_var'].get().strip(),
            'contact_method': self.entry_vars['contact_method_var'].get().strip(),
        }

        # Basic Validation (Name and Contact Method are required)
        if not data['name']:
            messagebox.showwarning("Validation Error", "Customer Name is required.")
            return

        # Simple Email Format Validation (optional but good practice)
        if data['email'] and '@' not in data['email']:
             messagebox.showwarning("Validation Error", "Please enter a valid Email address.")
             return
             
        if not data['contact_method']:
             messagebox.showwarning("Validation Error", "Preferred Contact Method must be selected.")
             return

        # Insert data into the database
        if self.db_manager.insert_customer(data):
            messagebox.showinfo("Success", f"Customer '{data['name']}' successfully saved!")
            self.clear_form()

    def clear_form(self):
        """Resets all input fields."""
        for var in self.entry_vars.values():
            if var != self.entry_vars["contact_method_var"]:
                var.set("")
        # Reset dropdown to the first option
        self.contact_dropdown.set("Email") 

    def on_closing(self):
        """Closes the DB connection before exiting the application."""
        self.db_manager.close()
        self.destroy()

if __name__ == "__main__":
    app = CustomerApp()
    app.mainloop()
