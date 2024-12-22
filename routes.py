from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import db, Expense, Income, Budget
from flask_login import login_required, current_user

bp = Blueprint('main', __name__)

# Expense CRUD
@bp.route('/expenses', methods=['GET', 'POST'])
@login_required
def manage_expenses():
    if request.method == 'POST':
        # Add expense
        new_expense = Expense(
            amount=request.form['amount'],
            category=request.form['category'],
            date=request.form['date'],
            user_id=current_user.id
        )
        db.session.add(new_expense)
        db.session.commit()
        flash('Expense added successfully!')
        return redirect(url_for('manage_expenses'))
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    return render_template('expenses.html', expenses=expenses)

@bp.route('/expenses/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_expense(id):
    expense = Expense.query.get_or_404(id)
    if request.method == 'POST':
        expense.amount = request.form['amount']
        expense.category = request.form['category']
        expense.date = request.form['date']
        db.session.commit()
        flash('Expense updated successfully!')
        return redirect(url_for('manage_expenses'))
    return render_template('update_expense.html', expense=expense)

@bp.route('/expenses/delete/<int:id>', methods=['POST'])
@login_required
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted successfully!')
    return redirect(url_for('manage_expenses'))

# Income CRUD
@bp.route('/income', methods=['GET', 'POST'])
@login_required
def manage_income():
    if request.method == 'POST':
        new_income = Income(
            source=request.form['source'],
            amount=request.form['amount'],
            date=request.form['date'],
            user_id=current_user.id
        )
        db.session.add(new_income)
        db.session.commit()
        flash('Income added successfully!')
        return redirect(url_for('manage_income'))
    incomes = Income.query.filter_by(user_id=current_user.id).all()
    return render_template('income.html', incomes=incomes)

# Budgeting
@bp.route('/budget', methods=['GET', 'POST'])
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

# Visualizations (to be implemented)

@bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    incomes = Income.query.filter_by(user_id=current_user.id).all()
    budget = Budget.query.filter_by(user_id=current_user.id).first()
    return render_template('dashboard.html', expenses=expenses, incomes=incomes, budget=budget)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    # ... login logic ...
    return redirect(url_for('dashboard'))
