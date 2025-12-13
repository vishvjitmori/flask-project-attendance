from flask import Blueprint, render_template, request
from datetime import date, timedelta
from sqlalchemy import func, case
from app import db
from app.model import Attendance, Employee, Store


payroll_bp = Blueprint('payroll', __name__)


@payroll_bp.route('/payroll')
def payroll():
    # Inputs
    month = request.args.get('month', default=date.today().month, type=int)
    year = request.args.get('year', default=date.today().year, type=int)
    store_name = request.args.get('store_name', default='', type=str)
    employee_name = request.args.get('employee_name', default='', type=str)
    page = request.args.get('page', default=1, type=int)

    # Date range for selected month
    start_date = date(year, month, 1)
    next_month = start_date.replace(day=28) + timedelta(days=4)
    end_date = next_month.replace(day=1)

    # Reusable hours expression
    hours_expr = func.coalesce(
        Attendance.total_hours,
        case(
            (Attendance.check_out.isnot(None),
             (func.extract('epoch', Attendance.check_out) - func.extract('epoch', Attendance.check_in)) / 3600.0),
            else_=0
        )
    )

    # Base query
    query = db.session.query(
        Employee.id.label('employee_id'),
        Employee.employee_name,
        Store.store_name,
        func.min(Attendance.date).label('from_date'),
        func.max(Attendance.date).label('to_date'),
        func.sum(hours_expr).label('hours')
    ).join(Employee, Employee.id == Attendance.employee_id)\
     .join(Store, Store.id == Attendance.store_id)\
     .filter(Attendance.date >= start_date, Attendance.date < end_date)

    if store_name:
        query = query.filter(Store.store_name.ilike(f"%{store_name}%"))
    if employee_name:
        query = query.filter(Employee.employee_name.ilike(f"%{employee_name}%"))

    grouped = query.group_by(Employee.id, Store.store_name, Employee.employee_name)

    rows = grouped.order_by(Employee.employee_name.asc())\
                  .paginate(page=page, per_page=15, error_out=False)

    # Total hours across the filtered month (not just the page)
    total_hours = db.session.query(func.sum(hours_expr))\
        .join(Employee, Employee.id == Attendance.employee_id)\
        .join(Store, Store.id == Attendance.store_id)\
        .filter(Attendance.date >= start_date, Attendance.date < end_date)

    if store_name:
        total_hours = total_hours.filter(Store.store_name.ilike(f"%{store_name}%"))
    if employee_name:
        total_hours = total_hours.filter(Employee.employee_name.ilike(f"%{employee_name}%"))

    total_hours_val = total_hours.scalar() or 0

    return render_template(
        'payroll.html',
        rows=rows,
        month=month,
        year=year,
        store_name=store_name,
        employee_name=employee_name,
        total_hours=round(total_hours_val, 2)
    )
