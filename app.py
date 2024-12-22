from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Initialize the Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Example config
app.config['SECRET_KEY'] = 'your_secret_key'  # Set a secret key for session management

# Initialize the database and login manager
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirect to login if not authenticated

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

# Expense model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Income model
class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Budget model
class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_budget = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home route
# @app.route("/")
# def home():
#     return redirect(url_for("home"))
@app.route('/')
def home():
    return render_template('home.html')
# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password.")
    return render_template("login.html")

# Registration route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")

# Dashboard route
@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    incomes = Income.query.filter_by(user_id=current_user.id).all()
    budget = Budget.query.filter_by(user_id=current_user.id).first()
    total_expenses = sum(expense.amount for expense in expenses)  # Calculate total expenses
    total_income = sum(income.amount for income in incomes)        # Calculate total income

    total_deficits = total_income - total_expenses   # Calculate deficits
     # Generate advice based on the deficit
    if total_deficits < 0:
        advice = "You are currently in deficit. Consider reducing your expenses or increasing your income."
    elif total_deficits > 0:
        advice = "Great job! You have a surplus. Consider saving or investing the extra funds."
    else:
        advice = "You are breaking even. Keep monitoring your finances to maintain this balance."

    return render_template('dashboard.html', expenses=expenses, incomes=incomes, budget=budget, deficit=total_deficits,total_expenses=total_expenses,advice=advice)

# Logout route
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# Expense CRUD
@app.route('/expenses', methods=['GET', 'POST'])
@login_required
def manage_expenses():
    if request.method == 'POST':
        # Convert the date string to a date object
        date_object = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        
        new_expense = Expense(
            amount=request.form['amount'],
            category=request.form['category'],
            date=date_object,  # Use the date object here
            user_id=current_user.id
        )
        db.session.add(new_expense)
        db.session.commit()
        flash('Expense added successfully!')
        return redirect(url_for('manage_expenses'))
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    return render_template('expenses.html', expenses=expenses)

@app.route('/expenses/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_expense(id):
    expense = Expense.query.get_or_404(id)
    if request.method == 'POST':
        # Convert the date string to a date object
        date_object = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        
        expense.amount = request.form['amount']
        expense.category = request.form['category']
        expense.date = date_object  # Use the date object here
        db.session.commit()
        flash('Expense updated successfully!')
        return redirect(url_for('manage_expenses'))
    return render_template('update_expense.html', expense=expense)

@app.route('/expenses/delete/<int:id>', methods=['POST'])
@login_required
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted successfully!')
    return redirect(url_for('manage_expenses'))

# Income CRUD
@app.route('/income', methods=['GET', 'POST'])
@login_required
def manage_income():
    if request.method == 'POST':
        # Convert the date string to a date object
        date_object = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        
        new_income = Income(
            source=request.form['source'],
            amount=request.form['amount'],
            date=date_object,  # Use the date object here
            user_id=current_user.id
        )
        db.session.add(new_income)
        db.session.commit()
        flash('Income added successfully!')
        return redirect(url_for('manage_income'))
    incomes = Income.query.filter_by(user_id=current_user.id).all()
    return render_template('income.html', incomes=incomes)

@app.route('/income/delete/<int:id>', methods=['POST'])
@login_required
def delete_income(id):
    income = Income.query.get_or_404(id)
    db.session.delete(income)
    db.session.commit()
    flash('Income deleted successfully!')
    return redirect(url_for('manage_income'))

@app.route('/income/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_income(id):
    income = Income.query.get_or_404(id)
    if request.method == 'POST':
        # Convert the date string to a date object
        date_object = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        
        income.source = request.form['source']
        income.amount = request.form['amount']
        income.date = date_object  # Use the date object here
        db.session.commit()
        flash('Income updated successfully!')
        return redirect(url_for('manage_income'))
    return render_template('update_income.html', income=income)

# Budgeting
@app.route('/budget', methods=['GET', 'POST'])
@login_required
def manage_budget():
    if request.method == 'POST':
        budget = Budget.query.filter_by(user_id=current_user.id).first()
        if budget:
            budget.total_budget = request.form['total_budget']
        else:
            budget = Budget(total_budget=request.form['total_budget'], user_id=current_user.id)
            db.session.add(budget)
        db.session.commit()
        flash('Budget updated successfully!')
        return redirect(url_for('manage_budget'))
    budget = Budget.query.filter_by(user_id=current_user.id).first()
    return render_template('budget.html', budget=budget)

# Run the application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)
