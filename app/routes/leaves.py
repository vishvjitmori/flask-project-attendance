from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime
from app import db
from app.model import LeaveRequest, Employee

leaves_bp = Blueprint('leaves', __name__)


@leaves_bp.route('/employee_leave_request', methods=['POST'])
def request_leave():
    employee_id = session.get('employee_id')
    if not employee_id:
        flash("Please log in to submit leave.", "danger")
        return redirect(url_for('employeelogin.employee_login'))

    employee = Employee.query.get(employee_id)
    if not employee:
        flash("Employee not found.", "danger")
        return redirect(url_for('employeelogin.employee_login'))

    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    reason = request.form.get('reason', '').strip()

    try:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_dt = datetime.strptime(end_date, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        flash("Invalid dates provided.", "danger")
        return redirect(url_for('emp_dashboard.dashboard'))

    if end_dt < start_dt:
        flash("End date cannot be before start date.", "danger")
        return redirect(url_for('emp_dashboard.dashboard'))

    leave = LeaveRequest(
        employee_id=employee.id,
        start_date=start_dt,
        end_date=end_dt,
        reason=reason,
        status="pending"
    )
    db.session.add(leave)
    db.session.commit()

    flash("Leave request submitted.", "success")
    return redirect(url_for('emp_dashboard.dashboard'))


@leaves_bp.route('/leave_requests')
def leave_requests():
    if 'user_id' not in session:
        flash("Unauthorized.", "danger")
        return redirect(url_for('auth.login'))
    leaves = LeaveRequest.query.order_by(LeaveRequest.created_at.desc()).all()
    return render_template('leave_requests.html', leaves=leaves)


@leaves_bp.route('/leave_requests/<int:leave_id>/<action>', methods=['POST'])
def update_leave(leave_id, action):
    if 'user_id' not in session:
        flash("Unauthorized.", "danger")
        return redirect(url_for('auth.login'))
    leave = LeaveRequest.query.get_or_404(leave_id)
    if action not in ["approve", "reject"]:
        flash("Invalid action.", "danger")
        return redirect(url_for('leaves.leave_requests'))

    leave.status = "approved" if action == "approve" else "rejected"
    leave.response_message = request.form.get('response_message', '').strip()
    leave.updated_at = datetime.utcnow()
    db.session.commit()

    flash(f"Leave {action}d.", "success")
    return redirect(url_for('leaves.leave_requests'))

