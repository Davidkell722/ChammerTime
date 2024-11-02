print("Starting Flask app...")  # Add this line
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
