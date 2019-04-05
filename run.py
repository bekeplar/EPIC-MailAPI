"""This is the application entry point"""

from api.app import create_app

# Creating an app instance 
app = create_app("Development")

if __name__ == "__main__":
    app.run()
