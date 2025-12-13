from app import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    store_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    address_name = db.Column(db.String(255), nullable=False)
    street_name = db.Column(db.String(255), nullable=False)
    town = db.Column(db.String(255), nullable=False)
    locality = db.Column(db.String(255), nullable=False)
    post_code = db.Column(db.String(255), nullable=False)
    contact1 = db.Column(db.String(50), nullable=False)
    contact2 = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    employee_info = db.relationship('Employee', back_populates='store', passive_deletes=True)


class Employee(db.Model):
    id =  db.Column(db.Integer, primary_key=True, autoincrement=True)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id', ondelete="SET NULL"), nullable=True)
    store = db.relationship('Store', back_populates='employee_info') 
    employee_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    designation = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), default="active")
    address_name = db.Column(db.String(255), nullable=False)
    street_name = db.Column(db.String(255), nullable=False)
    town = db.Column(db.String(255), nullable=False)
    locality = db.Column(db.String(255), nullable=False)
    post_code = db.Column(db.String(255), nullable=False)
    contact1 = db.Column(db.String(50), nullable=False)
    contact2 = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)



class GenerateID(db.Model):
    count = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_ID = db.Column(db.String(20), unique=True, nullable=False)  
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    employee = db.relationship('Employee')
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)
    store = db.relationship('Store')
    check_in = db.Column(db.DateTime)
    check_out = db.Column(db.DateTime)
    total_hours = db.Column(db.Float)  
    notes = db.Column(db.String(255))
    # Use a callable for default so the date is evaluated per row, not at import
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)


class LeaveRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    employee = db.relationship('Employee')
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.String(500))
    status = db.Column(db.String(20), default="pending")  # pending, approved, rejected
    response_message = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
