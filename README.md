# friday-project-5
# Simple Customer Data Manager (Python + SQLite)

This is a lightweight system built in Python using the `tkinter` GUI library and the built-in `sqlite3` database module. It provides a simple interface for collecting customer information and a separate utility for viewing the stored data.

## 📁 Project Files

| File Name | Purpose | Description |
| :--- | :--- | :--- |
| **`fp5.py`** | **Data Entry GUI** | This is the main application file. It opens the GUI form where customers enter their personal data. When the "Submit" button is pressed, the data is saved to the database. |
| **`customer_data.db`** | **Database File** | This is the SQLite database file where **all collected customer information is permanently stored**. This file is automatically created by `fp5.py` the first time data is submitted. |
| **`readDatabase.py`** | **Data Viewer GUI** | This utility opens a separate GUI window to **display all the records** found within the `customer_data.db` file in a clear, tabular format. |

---

## 🚀 Getting Started

### Prerequisites

* **Python 3**
* The project relies on standard Python libraries: `tkinter` (for the GUI) and `sqlite3` (for the database), which are included with most Python installations.

### Setup

1.  Clone or download the project files.
2.  Ensure that all files (`fp5.py`, `readDatabase.py`, etc.) are located in the same directory.

---

## 💻 How to Use

### 1. Collecting Data (`fp5.py`)

This is the file you run to accept new customer information.

```bash
python fp5.py
