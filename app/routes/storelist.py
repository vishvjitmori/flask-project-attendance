from flask import Blueprint, render_template,session,request, redirect, url_for,flash
from app import db
from app.model import Store
from datetime import datetime


storelist_bp = Blueprint('storelist', __name__)

@storelist_bp.route("/storelist", methods = ["GET","POST"])
def storelist():
    # Get filter parameters from request (both GET and POST)
    store_name = request.args.get('store_name') or request.form.get('store_name') or ''
    date = request.args.get('date') or request.form.get('date') or ''
    page = request.args.get('page', 1, type=int)
    
    # Start with base query
    query = Store.query
    
    # Filter by store name
    if store_name:
        query = query.filter(Store.store_name.ilike(f'%{store_name}%'))
    
    # Filter by date of creation (created_at)
    if date:
        try:
            filter_date = datetime.strptime(date, '%Y-%m-%d').date()
            query = query.filter(db.func.date(Store.created_at) == filter_date)
        except ValueError:
            pass  # Invalid date format, ignore
    
    stores = query.order_by(Store.created_at.desc()).paginate(page=page, per_page=15, error_out=False)
    
    return render_template('storelist.html', stores=stores, 
                         store_name=store_name, date=date)

@storelist_bp.route("/get_store/<int:id>")
def get_store(id):
    store = Store.query.get(id)
    return {
        "id": store.id,
        "store_name": store.store_name,
        "email": store.email,
        "address_name": store.address_name,
        "street_name": store.street_name,
        "town": store.town,
        "locality": store.locality,
        "post_code": store.post_code,
        "contact1": store.contact1,
        "contact2": store.contact2
    }

@storelist_bp.route("/update_store", methods=["POST"])
def update_store():

    id = request.form['id']
    store = Store.query.get(id)

    store.store_name = request.form['store_name']
    store.email = request.form['email']
    store.address_name = request.form['address_name']
    store.street_name = request.form['street_name']
    store.town = request.form['town']
    store.locality = request.form['locality']
    store.post_code = request.form['post_code']
    store.contact1 = request.form['contact1']
    store.contact2 = request.form['contact2']

    db.session.commit()

    flash("Store updated successfully!", "success")
    return redirect(url_for("storelist.storelist"))




@storelist_bp.route("/delete_store/<int:id>")
def delete_store(id):
    store = Store.query.get_or_404(id)

    db.session.delete(store)
    db.session.commit()
    return redirect(url_for('storelist.storelist'))


@storelist_bp.route("/filter_store", methods=["POST"])
def filter_store():
    # Get filter parameters from form
    store_name = request.form.get('store_name', '')
    date = request.form.get('date', '')
    
    # Redirect to storelist with query parameters
    return redirect(url_for('storelist.storelist', 
                           store_name=store_name, 
                           date=date))