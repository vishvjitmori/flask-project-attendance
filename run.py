from app import create_app, db
from app.model import User

app = create_app()

# Create tables
with app.app_context():
    db.create_all()

# Run Flask server
if __name__ == '__main__':
    app.run(debug=True)

