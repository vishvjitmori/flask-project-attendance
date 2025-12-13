from flask import Blueprint, render_template,redirect, url_for,request, jsonify
from app import db
from app.model import Employee,Store,GenerateID
from datetime import datetime



employeelist_bp = Blueprint ('employeelist', __name__)

@employeelist_bp.route("/employeelist", methods = ["GET","POST"])
def employeelist():
    stores = Store.query.all()
    
    # Get filter parameters from request (both GET and POST)
    store_name = request.args.get('store_name') or request.form.get('store_name') or ''
    employee_name = request.args.get('employee_name') or request.form.get('employee_name') or ''
    date = request.args.get('date') or request.form.get('date') or ''
    page = request.args.get('page', 1, type=int)
    
    # Start with base query
    query = Employee.query
    
    # Filter by store name
    if store_name:
        query = query.join(Store).filter(Store.store_name.ilike(f'%{store_name}%'))
    
    # Filter by employee name
    if employee_name:
        query = query.filter(Employee.employee_name.ilike(f'%{employee_name}%'))
    
    # Filter by date of join (created_at)
    if date:
        try:
            filter_date = datetime.strptime(date, '%Y-%m-%d').date()
            query = query.filter(db.func.date(Employee.created_at) == filter_date)
        except ValueError:
            pass  # Invalid date format, ignore
    
    employees = query.order_by(Employee.created_at.desc()).paginate(page=page, per_page=15, error_out=False)
    
    return render_template('employeelist.html', employees=employees, stores=stores, 
                         store_name=store_name, employee_name=employee_name, date=date)


@employeelist_bp.route("/delete_employee/<int:id>")
def delete_employee(id):
    employee = Employee.query.get_or_404(id)

    db.session.delete(employee)
    db.session.commit()

    return redirect(url_for('employeelist.employeelist'))

@employeelist_bp.route("/update_employee", methods=["POST"])
def update_employee():
    emp_id = request.form.get("id")
    employee = Employee.query.get(emp_id)

    employee.store_id = request.form.get("store_id")
    employee.employee_name = request.form.get("employee_name")
    employee.email = request.form.get("email")
    employee.designation = request.form.get("designation")
    employee.status = request.form.get("status")
    employee.address_name = request.form.get("address_name")
    employee.street_name = request.form.get("street_name")
    employee.town = request.form.get("town")
    employee.locality = request.form.get("locality_name")
    employee.post_code = request.form.get("post_code")
    employee.contact1 = request.form.get("contact1")
    employee.contact2 = request.form.get("contact2")

    db.session.commit()

    return redirect(url_for("employeelist.employeelist"))


@employeelist_bp.route("/filter_employee", methods=["POST"])
def filter_employee():
    # Get filter parameters from form
    store_name = request.form.get('store_name', '')
    employee_name = request.form.get('employee_name', '')
    date = request.form.get('date', '')
    
    # Redirect to employeelist with query parameters
    return redirect(url_for('employeelist.employeelist', 
                           store_name=store_name, 
                           employee_name=employee_name, 
                           date=date))


@employeelist_bp.route("/get_employee/<int:id>")
def get_employee(id):
    employee = Employee.query.get_or_404(id)
    return jsonify({
        "id": employee.id,
        "store_id": employee.store_id,
        "employee_name": employee.employee_name,
        "email": employee.email,
        "designation": employee.designation,
        "status": employee.status,
        "address_name": employee.address_name,
        "street_name": employee.street_name,
        "town": employee.town,
        "locality": employee.locality,
        "post_code": employee.post_code,
        "contact1": employee.contact1,
        "contact2": employee.contact2 or ""
    })



@employeelist_bp.route("/generate_id", methods=['GET','POST'])
def generate_id():
    if request.method == 'POST':
        employee_ID = request.form.get('employee_ID')
        name = request.form.get('name')
        password = request.form.get('password')

        new_id = GenerateID(
            employee_ID=employee_ID,
            name=name,
            password=password
        )
        db.session.add(new_id)
        db.session.commit()

        return redirect(url_for('employeelist.generate_id'))

    return render_template('generate_id.html')
