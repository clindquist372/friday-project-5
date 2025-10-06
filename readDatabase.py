import tkinter as tk
from tkinter import ttk
import sqlite3

# --- Database Configuration ---
DATABASE_FILE = "customer_data.db"
TABLE_NAME = "customers"

def connect_db():
    """Establishes a connection to the SQLite database file."""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        # Optional: Set row_factory to sqlite3.Row for dictionary-like access
        # conn.row_factory = sqlite3.Row 
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def fetch_data():
    """Fetches all customer records and column names from the database."""
    conn = connect_db()
    if conn is None:
        return [], []
        
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {TABLE_NAME};")
        
        # Get column names from the cursor description
        column_names = [description[0] for description in cursor.description]
        
        # Get all records
        records = cursor.fetchall()
        
        return column_names, records
        
    except sqlite3.OperationalError as e:
        print(f"Error fetching data (table missing?): {e}")
        # Assuming the structure from the previous request (5 columns)
        default_cols = ["id", "name", "email", "phone", "address"]
        return default_cols, [("N/A", "N/A", "N/A", "N/A", "N/A")] 
        
    except sqlite3.Error as e:
        print(f"An unexpected SQLite error occurred: {e}")
        return [], []

    finally:
        if conn:
            conn.close()


def setup_gui():
    """Sets up the main Tkinter window and Treeview widget."""
    root = tk.Tk()
    root.title("Customer Data Viewer")
    
    # Fetch data and column names
    columns, data = fetch_data()

    if not columns:
        tk.Label(root, text="Error: Could not retrieve column structure or data.", fg="red").pack(pady=20)
        return root

    # --- Setup Treeview (the data table) ---
    
    # 1. Prepare columns for the Treeview
    # Tkinter needs the columns as a list of names/identifiers
    tree_columns = tuple(columns)
    
    tree = ttk.Treeview(root, columns=tree_columns, show='headings')
    
    # 2. Configure Column Headings and Widths
    # The first column is the implicit internal column, which we hide with show='headings'
    # The 'id' column is the first heading
    for col_name in columns:
        tree.heading(col_name, text=col_name.title()) # Set column header text
        # Set a reasonable width for each column
        if col_name == 'id':
            tree.column(col_name, width=50, anchor='center')
        elif col_name == 'name':
            tree.column(col_name, width=150)
        elif col_name == 'email':
            tree.column(col_name, width=200)
        else: # phone, address
            tree.column(col_name, width=100)

    # 3. Insert Data
    for row in data:
        # Insert each row of data into the treeview
        tree.insert('', tk.END, values=row)

    # 4. Add a Scrollbar (makes it usable with many records)
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    # 5. Grid/Pack the Treeview and Scrollbar
    scrollbar.pack(side='right', fill='y')
    tree.pack(padx=10, pady=10, fill='both', expand=True)
    
    # Add a refresh button
    def refresh_data():
        # Clear existing data
        for item in tree.get_children():
            tree.delete(item)
        
        # Fetch and insert new data
        _, new_data = fetch_data()
        for row in new_data:
            tree.insert('', tk.END, values=row)
            
    refresh_btn = ttk.Button(root, text="Refresh Data", command=refresh_data)
    refresh_btn.pack(pady=5)
    
    return root

if __name__ == "__main__":
    app = setup_gui()
    if app:
        app.mainloop()