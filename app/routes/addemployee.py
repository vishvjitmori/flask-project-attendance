from flask import Blueprint, render_template, request,flash,redirect,url_for, session
from app import db
from app.model import Employee,Store



addemployee_bp = Blueprint ('addemployee', __name__)

@addemployee_bp.route("/addemployee", methods = ["GET","POST"])
def addemployee():
    stores = Store.query.all()

    designations = ["Manager", "Cashier", "Stock Handler", "Accountant", "Delivery Boy"]
    statuses = ["Active", "Inactive"] 

    if request.method == "POST":
        store_id = request.form.get('store_id')
        employee_name = request.form.get('name')
        email = request.form.get('email')
        designation = request.form.get('designation')
        status = request.form.get('status')
        address_name = request.form.get('address_name')
        street_name = request.form.get('street_name')
        town = request.form.get('town')
        locality = request.form.get('locality_name')
        post_code = request.form.get('post_code')
        contact1 = request.form.get('contact1')
        contact2 = request.form.get('contact2')

        new_employee = Employee(
            employee_name=employee_name,
            email=email,
            store_id=store_id,
            designation=designation,
            status=status,
            address_name=address_name,
            street_name=street_name,
            town=town,
            locality=locality,
            post_code=post_code,
            contact1=contact1,
            contact2=contact2
         )
        db.session.add(new_employee)
        db.session.commit()

        flash('Employee added succesfully', "successfully")
        return redirect(url_for('employeelist.employeelist'))

    return render_template('addemployee.html',stores=stores,designations=designations,statuses=statuses)