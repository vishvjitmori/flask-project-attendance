from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'Your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app.model import User, LeaveRequest

    @app.context_processor
    def inject_user():
        user = None
        pending_leaves = 0
        if 'user_id' in session:
            user = User.query.get(session['user_id'])
            pending_leaves = LeaveRequest.query.filter_by(status="pending").count()
        return {'current_user': user, 'pending_leaves': pending_leaves}
    
    
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.addstore import addstore_bp
    from app.routes.storelist import storelist_bp
    from app.routes.employeelist import employeelist_bp
    from app.routes.addemployee import addemployee_bp
    from app.routes.employeelogin import employeelogin_bp
    from app.routes.employeedashboard import emp_dashboard
    from app.routes.attendancelogs import attendancelogs_bp
    from app.routes.payroll import payroll_bp
    from app.routes.leaves import leaves_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(addstore_bp)
    app.register_blueprint(storelist_bp)
    app.register_blueprint(employeelist_bp)
    app.register_blueprint(addemployee_bp)
    app.register_blueprint(employeelogin_bp)
    app.register_blueprint(emp_dashboard)
    app.register_blueprint(attendancelogs_bp)
    app.register_blueprint(payroll_bp)
    app.register_blueprint(leaves_bp)

    return app