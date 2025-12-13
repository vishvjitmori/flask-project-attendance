from flask import Blueprint, render_template, redirect, session,request,flash, url_for
from app import db
from app.model import Store

addstore_bp = Blueprint('addstore', __name__)


@addstore_bp.route("/addstore", methods=["GET","POST"])
def addstore():
    if request.method == "POST":
        store_name = request.form.get('store_name')
        email = request.form.get('email')
        address_name = request.form.get('address_name')
        street_name = request.form.get('street_name')
        town = request.form.get('town')
        locality = request.form.get('locality_name')
        post_code = request.form.get('post_code')
        contact1 = request.form.get('contact1')
        contact2 = request.form.get('contact2')

        new_store = Store(
            store_name=store_name,
            email=email,
            address_name=address_name,
            street_name = street_name,
            town=town,
            locality=locality,
            post_code=post_code,
            contact1=contact1,
            contact2=contact2

        )
        db.session.add(new_store)
        db.session.commit()

        flash('store added successfully', "success")
        return redirect(url_for('storelist.storelist'))
    
    return render_template('addstore.html')