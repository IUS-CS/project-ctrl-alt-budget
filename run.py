# Flask app entry point 
# In the future we should be able to do python run.py or make run to bootup the app
from src.backend.app import create_app, db

# Creates the Flask app using the create_app() function in app/app__init__.py
app = create_app()

# We will import necessary local packages for run.py in future sprints.
if __name__ == "__main__":
    app.run(debug=True)