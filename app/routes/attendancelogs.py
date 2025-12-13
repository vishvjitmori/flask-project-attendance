from flask import Blueprint, render_template, request
from app.model import Attendance, Employee, Store
from datetime import datetime


attendancelogs_bp = Blueprint('attendancelogs', __name__)

@attendancelogs_bp.route('/attendance_logs')
def attendance_logs():
    page = request.args.get('page', 1, type=int)
    store_name = request.args.get('store_name', '', type=str)
    employee_name = request.args.get('employee_name', '', type=str)
    date_str = request.args.get('date', '', type=str)

    query = Attendance.query.join(Employee).join(Store)

    if store_name:
        query = query.filter(Store.store_name.ilike(f"%{store_name}%"))
    if employee_name:
        query = query.filter(Employee.employee_name.ilike(f"%{employee_name}%"))
    if date_str:
        try:
            filter_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            query = query.filter(Attendance.date == filter_date)
        except ValueError:
            pass

    logs = query.order_by(Attendance.date.desc(), Attendance.check_in.desc())\
        .paginate(page=page, per_page=15, error_out=False)

    return render_template(
        'attendancelogs.html',
        logs=logs,
        store_name=store_name,
        employee_name=employee_name,
        date=date_str
    )