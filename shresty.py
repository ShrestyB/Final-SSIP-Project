from flask import Flask, render_template, request, jsonify, redirect, url_for
import csv
import pymongo
import datetime

app = Flask(__name__)

# Connect to MongoDB
myclient = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.npnpn7l.mongodb.net/?retryWrites=true&w=majority")
db = myclient["qr"]
feedback_collection = db["feedback"]

# Dictionary to store IP addresses and submission timestamps
ip_timestamps = {}

# Function to reset timestamps at the beginning of each day
def reset_timestamps():
    for ip in ip_timestamps:
        ip_timestamps[ip] = None

# Schedule the reset_timestamps function to run at the beginning of each day
# You can use a scheduler library for this.


@app.route('/')
def feedback_form():
    return render_template('feedback.html')

# Route to handle form submission and store data in MongoDB
@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    if request.method == 'POST':
        # Get form data
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        email = request.form['email']
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

        print(result.inserted_id)

        return redirect(url_for('feedback_form'))  # Redirect to the feedback form

# Route to list feedback data from MongoDB
@app.route('/feedback_list')
def feedback_list():
    feedback_data = feedback_collection.find({})
    return render_template('feedback_list.html', feedback_data=feedback_data)

# Route to fetch data from a CSV file and serve it as JSON
@app.route('/fetch_csv_data')
def fetch_csv_data():
    feedback_data = []

    # Read data from the CSV file
    with open('feedbacckk.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            feedback_data.append(row)

    return jsonify(feedback_data)

# Route to capture and handle IP addresses for form submissions
@app.route('/form', methods=['GET', 'POST'])
def qr_form():
    if request.method == 'POST':
        user_ip = request.remote_addr
        now = datetime.datetime.now()

        if user_ip in ip_timestamps:
            last_submission_time = ip_timestamps[user_ip]
            if last_submission_time is None or (now - last_submission_time).days >= 1:
                ip_timestamps[user_ip] = now
                # Process the form submission
                return "Form submitted successfully."
            else:
                return "You have already submitted a form today."

    return render_template('feedback.html')

if __name__ == '__main__':
    app.run(debug=True)