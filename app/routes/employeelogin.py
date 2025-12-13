from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.model import GenerateID



employeelogin_bp = Blueprint ('employeelogin', __name__)


@employeelogin_bp.route('/employee_login', methods=['GET', 'POST'])
def employee_login():
    if request.method == 'POST':
        employee_ID = request.form.get('employee_ID')
        password = request.form.get('password')

        emp_id_entry = GenerateID.query.filter_by(employee_ID=employee_ID).first()

        if emp_id_entry is None:
            flash('Invalid employee ID or password', "danger")
            return redirect(url_for('employeelogin.employee_login'))

        # Compare plain text password
        if emp_id_entry.password != password:
            flash('Invalid employee ID or password', "danger")
            return redirect(url_for('employeelogin.employee_login'))
        
        session['employee_id'] = emp_id_entry.count
        session['employee_name'] = emp_id_entry.name 
        flash('Logged in successfully!', "success")
        return redirect(url_for('emp_dashboard.dashboard'))
    
    return render_template('employeelogin.html')