# 🏢 Green Saver Application

Green Saver Application is a system that helps users manage their energy consumption and track their carbon footprint. This platform supports individual and corporate subscriptions and offers features such as billing, consumption analysis, and carbon emission calculations.

---

## 🎨 Key Features

- 🟢 **Individual and Corporate Subscription**: Users can register as individual or corporate subscribers.
- 💰 **Invoice Management**: Users can add, view, delete, or update their invoices.
- 🌱 **Carbon Emission Calculation**: Calculates users' carbon footprint based on their energy consumption.
- 📊 **Invoice Comparison**: Users can compare past invoices and analyze their consumption trends.
- 📈 **Admin Panel**: Admins can list all subscribers and view the top spenders.

---

## 🌐 Modularity and Project Structure

This project was developed using a **modular architecture**. Keeping each class and function in separate files provides the following key advantages:

### 📝 Easy Maintenance and Scalability
- Each function or component has a specific role, making the code easier to understand and develop.
- New features can be added by updating only the relevant files without affecting other modules.

### 🔄 Code Reusability
- Allows writing **reusable code**. For example, functions in `operations.py` can be easily called by different GUI windows.
- Similarly, `database/queries.py` centralizes SQL queries, making them **secure** and **more manageable**.

### 🌍 Suitable for Team Collaboration
- Enables multiple developers to work on different files simultaneously.
- Team members can focus on **admin panel**, **subscription system**, or **database operations** independently.

### 🎨 Cleaner and More Readable Code
- A well-structured file organization helps new developers understand the project more easily.
- Improves code readability and simplifies debugging.

This approach makes the application **flexible**, **easy to maintain**, and **sustainable in the long term**.

## 📂 Project Directory Structure

```
/database
  ├── config.py          # Database configuration settings
  ├── connection.py      # Database connection functions
  ├── operations.py      # Database operations (CRUD functions)
  └── queries.py         # SQL queries

/gui
  ├── /admin
  │   ├── admin_panel_window.py         # Admin panel interface
  │   ├── all_subscribers_dialog.py     # Window listing all subscribers
  │   └── top_spenders_dialog.py        # Window displaying top spenders
  │   
  ├── /auth
  │   ├── admin_login_window.py          # Admin login screen
  │   ├── password_update_dialog.py      # Password update screen
  │   └── user_login_window.py          # User login screen
  │   
  ├── /main_app
  │   ├── add_invoice_dialog.py                 # Invoice addition screen
  │   ├── carbon_emission_dialog.py            # Carbon emission calculation screen
  │   ├── compare_all_time_invoices_dialog.py  # Compare past invoices
  │   ├── compare_invoices_dialog.py           # Compare selected invoices
  │   ├── delete_invoice_dialog.py             # Delete invoice screen
  │   ├── main_app_window.py                   # Main application interface
  │   ├── show_all_invoices_dialog.py          # Display all invoices
  │   ├── show_invoice_dialog.py               # Display selected invoice
  │   └── update_invoice_dialog.py             # Update invoice screen
  │   
  ├── /subscriptions
  │   ├── corporate_window.py      # Corporate subscription screen
  │   └── individual_window.py     # Individual subscription screen
  │   
  └── main_window.py  # Application startup screen

.gitignore
app_icon.png
greensaverdb-insert.sql  # Sample data insertion SQL file
greensaverdb-schema.sql  # Database schema file
main.py  # Entry point of the application
README.md
```

---

## 💪 Installation and Usage

1. **Clone the Repository:**

   ```
   git clone https://github.com/yusufyilmaz00/Green-Saver-Application.git
   cd Green-Saver-Application
   ```

2. **Requirements:**
   - Python 3.x
   - PostgreSQL
   - PyQt5
   - psycopg2

3. **Installing Dependencies:**

   ```
   pip install -r requirements.txt
   ```

4. **Setting Up the Database:** Run `greensaverdb-schema.sql` in PostgreSQL to create the necessary tables:

   ```
   psql -U postgres -d greensaverdb -f greensaverdb-schema.sql
   ```

   Then, insert sample data using:

   ```
   psql -U postgres -d greensaverdb -f greensaverdb-insert.sql
   ```

5. **Running the Application:**

   ```
   python main.py
   ```

1. **Requirements:**

   - Python 3.x
   - PostgreSQL
   - PyQt5
   - psycopg2

2. **Installing Dependencies:**

   ```
   pip install -r requirements.txt
   ```

3. **Setting Up the Database:** Run `greensaverdb-schema.sql` in PostgreSQL to create the necessary tables:

   ```
   psql -U postgres -d greensaverdb -f greensaverdb-schema.sql
   ```

   Then, insert sample data using:

   ```
   psql -U postgres -d greensaverdb -f greensaverdb-insert.sql
   ```

4. **Running the Application:**

   ```
   python main.py
   ```

## 👥 Contributions

The **first version** of the project was developed by Alihan Uludağ, Burakhan Saruhan, and Yusuf Yılmaz. The **second version** was updated by Yusuf Yılmaz.

Developers interested in contributing can submit **pull requests (PR)** or create an **issue** for bug reports. We welcome all feedback and contributions!