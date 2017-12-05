#!flask/bin/python

# Install dependencies, preferably in a virtualenv:
#
#     pip install flask flask-wtf matplotlib
#
# Run the development server:
#
#     python run.py
#
# Go to http://localhost:5000 to see plot.

from app import app
app.run(debug=True)
