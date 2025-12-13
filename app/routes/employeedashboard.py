from flask import Blueprint, render_template, redirect, url_for, flash, session
from app.model import Employee, Attendance, LeaveRequest
from datetime import datetime, date, timedelta
from sqlalchemy import func, case
from app import db

emp_dashboard = Blueprint('emp_dashboard', __name__)

@emp_dashboard.route('/employee_dashboard')
def dashboard():
    # if 'employee_id' not in session:
    #     return redirect(url_for('employeelogin.employee_login'))
    employee_name = session.get('employee_name', "User")
    employee_id = session.get('employee_id')

    today = datetime.utcnow().date()
    attendance = None
    last_leave = None
    if employee_id:
        attendance = Attendance.query.filter_by(
            employee_id=employee_id,
            date=today
        ).order_by(Attendance.check_in.desc()).first()
        last_leave = LeaveRequest.query.filter_by(employee_id=employee_id)\
            .order_by(LeaveRequest.created_at.desc()).first()

    checked_in = bool(attendance and attendance.check_in)
    checked_out = bool(attendance and attendance.check_out)
    disable_check_in = checked_in and not checked_out
    disable_check_out = (not checked_in) or checked_out

    # Current month stats for this employee
    month_start = date.today().replace(day=1)
    month_end = (month_start + timedelta(days=32)).replace(day=1)

    hours_expr = func.coalesce(
        Attendance.total_hours,
        case(
            (Attendance.check_out.isnot(None),
             (func.extract('epoch', Attendance.check_out) - func.extract('epoch', Attendance.check_in)) / 3600.0),
            else_=0
        )
    )

    attendance_days = 0
    total_hours_month = 0
    total_leaves = 0
    if employee_id:
        attendance_days = db.session.query(func.count(func.distinct(Attendance.date)))\
            .filter(
                Attendance.employee_id == employee_id,
                Attendance.date >= month_start,
                Attendance.date < month_end
            ).scalar() or 0

        total_hours_month = db.session.query(func.sum(hours_expr))\
            .filter(
                Attendance.employee_id == employee_id,
                Attendance.date >= month_start,
                Attendance.date < month_end
            ).scalar() or 0

        # Count approved leave days in the current month
        leaves = LeaveRequest.query.filter(
            LeaveRequest.employee_id == employee_id,
            LeaveRequest.status == "approved",
            LeaveRequest.start_date < month_end,
            LeaveRequest.end_date >= month_start
        ).all()

        for leave in leaves:
            start = max(leave.start_date, month_start)
            end = min(leave.end_date, month_end - timedelta(days=1))
            total_leaves += (end - start).days + 1

    total_hours_month = round(total_hours_month, 2)

    
    return render_template(
        'employeedashboard.html',
        employee_name=employee_name,
        checked_in=checked_in,
        checked_out=checked_out,
        disable_check_in=disable_check_in,
        disable_check_out=disable_check_out,
        attendance_days=attendance_days,
        total_leaves=total_leaves,
        total_hours_month=total_hours_month,
        last_leave=last_leave
    )


@emp_dashboard.route("/checkin", methods=["POST"])
def check_in():
    employee_id = session.get("employee_id")
    if not employee_id:
        return redirect(url_for("employeelogin.employee_login"))

    employee = Employee.query.get(employee_id)
    if not employee:
        flash("Employee not found. Please log in again.", "danger")
        session.pop("employee_id", None)
        return redirect(url_for("employeelogin.employee_login"))

    # Ensure a single attendance entry per day
    today = datetime.utcnow().date()
    attendance = Attendance.query.filter_by(
        employee_id=employee.id,
        date=today
    ).first()

    if attendance is None:
        attendance = Attendance(
            employee_id=employee.id,
            store_id=employee.store_id,
            check_in=datetime.utcnow(),
            date=today
        )
        db.session.add(attendance)
    elif attendance.check_in is None:
        attendance.check_in = datetime.utcnow()

    db.session.commit()

    return redirect(url_for("emp_dashboard.dashboard"))


@emp_dashboard.route("/checkout", methods=["POST"])
def check_out():
    employee_id = session.get("employee_id")

    # Get today's record (or the latest one) for this employee
    attendance = Attendance.query.filter_by(
        employee_id=employee_id,
        date=datetime.utcnow().date()
    ).order_by(Attendance.check_in.desc()).first()

    if attendance and attendance.check_out is None:
        attendance.check_out = datetime.utcnow()

        # Calculate total hours
        time_diff = attendance.check_out - attendance.check_in
        attendance.total_hours = round(time_diff.total_seconds() / 3600, 2)

        db.session.commit()

    return redirect(url_for("emp_dashboard.dashboard"))
