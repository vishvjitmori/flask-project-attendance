from flask import Blueprint, render_template, redirect, url_for, session
from datetime import datetime, timedelta, date
from sqlalchemy import func
from app import db
from app.model import Employee, Attendance, Store

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    today = datetime.utcnow().date()
    start_30_days = today - timedelta(days=29)

    # Top cards
    total_employees = Employee.query.count()
    active_checked_in = Attendance.query.filter(
        Attendance.date == today,
        Attendance.check_in.isnot(None),
        Attendance.check_out.is_(None)
    ).count()

    # Total hours today (completed and in-progress)
    total_hours_today = db.session.query(
        func.sum(
            func.coalesce(
                func.extract('epoch', func.coalesce(Attendance.check_out, datetime.utcnow())) -
                func.extract('epoch', Attendance.check_in),
                0
            ) / 3600.0
        )
    ).filter(Attendance.date == today, Attendance.check_in.isnot(None)).scalar() or 0
    total_hours_today = round(total_hours_today, 2)

    pending_checkout = active_checked_in  # same definition as active with no checkout

    # Hours per store (today)
    store_hours_rows = db.session.query(
        Store.store_name,
        func.sum(
            (func.extract('epoch', func.coalesce(Attendance.check_out, datetime.utcnow())) -
             func.extract('epoch', Attendance.check_in)) / 3600.0
        ).label('hours')
    ).join(Attendance, Attendance.store_id == Store.id)\
     .filter(Attendance.date == today, Attendance.check_in.isnot(None))\
     .group_by(Store.id).all()

    store_hours_labels = [row[0] for row in store_hours_rows]
    store_hours_values = [round(row[1], 2) if row[1] else 0 for row in store_hours_rows]

    # Last 30 days daily hours (all employees)
    daily_hours_rows = db.session.query(
        Attendance.date,
        func.sum(
            (func.extract('epoch', func.coalesce(Attendance.check_out, Attendance.check_in)) -
             func.extract('epoch', Attendance.check_in)) / 3600.0
        ).label('hours')
    ).filter(
        Attendance.date >= start_30_days,
        Attendance.date <= today,
        Attendance.check_in.isnot(None)
    ).group_by(Attendance.date).order_by(Attendance.date).all()

    daily_hours_labels = [row[0].strftime("%b %d") for row in daily_hours_rows]
    daily_hours_values = [round(row[1], 2) if row[1] else 0 for row in daily_hours_rows]

    # Live table (today)
    live_logs = Attendance.query.filter(
        Attendance.date == today,
        Attendance.check_in.isnot(None)
    ).order_by(Attendance.check_in.desc()).all()

    return render_template(
        'dashboard.html',
        total_employees=total_employees,
        active_checked_in=active_checked_in,
        total_hours_today=total_hours_today,
        pending_checkout=pending_checkout,
        store_hours_labels=store_hours_labels,
        store_hours_values=store_hours_values,
        daily_hours_labels=daily_hours_labels,
        daily_hours_values=daily_hours_values,
        live_logs=live_logs
    )
    
    

