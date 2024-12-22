# Personal Finance Tracker

#### Video Demo: 

#### Description:
Personal Finance Tracker is a Flask-based web application designed to help users manage their finances effectively by tracking income, expenses, and budgets. It provides features for adding, updating, and deleting financial records, as well as generating insights into financial health.

---

## Features
- User authentication with secure password management.
- CRUD operations for income, expenses, and budgets.
- Dashboard for tracking financial summary and generating financial advice based on deficits or surpluses.
- Responsive UI with templates for various views, including login, registration, dashboard, and record management.
- SQLite database integration for data storage.

---
TODO
## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/HefaCom/personal-finance-tracker.git
   cd personal-finance-tracker
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Initialize the database:
   ```bash
   flask shell
   >>> from app import db
   >>> db.create_all()
   >>> exit()
   ```

6. Run the application:
   ```bash
   python run.py
   ```

---

## Directory Structure

```
personal_finance_tracker/
├── app.py                   # Application entry point
├── config.py                # Configuration file
├── requirements.txt         # Dependencies
├── run.py                   # Script to run the app
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   ├── home.html            # Homepage
│   ├── login.html           # Login page
│   ├── register.html        # Registration page
│   ├── dashboard.html       # Dashboard
│   ├── expenses.html        # Expense management page
│   ├── update_expense.html  # Update expense page
│   ├── income.html          # Income management page
│   ├── update_income.html   # Update income page
│   ├── budget.html          # Budget management page
├── static/                  # Static files
│   ├── style.css            # Stylesheet
├── models.py                # Database models
└── README.md                # Project documentation
```

---

## Usage

### User Authentication
- Register a new account using the registration page.
- Login to access the dashboard and financial features.

### Dashboard
- View financial summary, including total expenses, total income, and budget.
- Receive tailored financial advice based on the deficit or surplus.

### Manage Records
- Add, update, or delete income and expense records.
- Set and update budget to track financial goals.

---

## Technologies Used
- **Python**: Backend logic.
- **Flask**: Web framework.
- **Flask-Login**: User authentication.
- **Flask-SQLAlchemy**: Database ORM.
- **SQLite**: Database.
- **HTML/CSS**: Frontend design.

---

## Future Enhancements
- Visualize financial trends with graphs and charts.
- Add reminders for bill payments or financial goals.
- Support multiple currencies.
- Integrate with external APIs for currency conversion and expense categorization.

---

## Contribution
Contributions are welcome! Please fork the repository, create a new branch for your feature or bug fix, and submit a pull request.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contact
For any inquiries or suggestions, please contact [okokohhezron254@gmail.com].
