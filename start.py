from waitress import serve
from app import app  # Import your Flask app

if __name__ == "__main__":
    try:
        # Run the application using waitress
        serve(app, host='0.0.0.0', port=8080, threads=4)  # Adjust the number of threads as needed
    except Exception as e:
        print(f"An error occurred while running the server: {e}")
