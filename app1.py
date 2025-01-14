from flask import Flask, render_template, request, jsonify, redirect, url_for
import csv
import pymongo
import subprocess
import os
from Main import visualize_and_save

app = Flask(__name__)

# Connect to MongoDB
myclient = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.npnpn7l.mongodb.net/?retryWrites=true&w=majority")
db = myclient["qr"]
feedback_collection = db["feedback"]

# Define the route to serve the feedback form
@app.route('/')
def feedback_form():
    return render_template('feedback.html')

# Define the route to handle form submission and store data in MongoDB and CSV
@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    if request.method == 'POST':
        # Get form data
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        email = request.form.get('email', '')  # Get email, default to empty string if not provided
        phone_number = request.form.get('phoneNumber', '')  # Get phone number, default to empty string if not provided
        police_address = request.form['policeAddress']
        district = request.form['district']
        comments = request.form['comments']
        rating = request.form['rating'] 

        # Store data in MongoDB
        result = feedback_collection.insert_one({
            "First Name": first_name,
            "Last Name": last_name,
            "Email": email,
            "Police Station Address": police_address,
            "District": district,
            "Comments": comments,
            "Rating": rating
        })

        # Store data in CSV file
      # Store data in CSV file 
        with open('Final SSIP Project/SSIP/Data Visualization/feedbackk.csv', mode='a', newline='') as file: 
            writer = csv.writer(file) 
            writer.writerow([first_name, last_name, email, police_address, district, comments, rating]) 
 
        return redirect(url_for('thank_you_page'))  # Redirect to the thank you page 
 
@app.route('/thank_you_page') 
def thank_you_page(): 
    return render_template('Tq.html') 

# Define a route to list feedback data from MongoDB
@app.route('/feedback_list')
def feedback_list():
    feedback_data = feedback_collection.find({})
    return render_template('feedback_list.html', feedback_data=feedback_data)

# Define a route to run Python code for visualization
@app.route('/run_python_code')
def run_python_code():
    # Replace 'path/to/your/visualization/script.py' with the correct path to your visualization script
    visualize_and_save()
    return 'Python code executed successfully!'  # Return a message to the user

# Define a route to serve the visualization page
@app.route('/visualization')
def visualization():
    images = []
    # Get a list of all image files in the 'static' folder
    image_dir = 'Final SSIP Project/SSIP/static/'
    for filename in os.listdir(image_dir):
        if filename.endswith("_service_distribution.png"):
            images.append(filename)
    return render_template('visualization.html', images=images)

if __name__ == '__main__':
    app.run(debug=True)
