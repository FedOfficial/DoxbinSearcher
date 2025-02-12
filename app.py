from flask import Flask, render_template, request
import csv

app = Flask(__name__)

def search_data(query):
    # Path to your CSV file
    file_path = 'data/Data.csv'
    
    # Open the CSV file and search
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        # Check for exact match for ID first
        for row in reader:
            # Search ID first, then Username, then Email
            if query.lower() == row['id'].lower():
                return row
        file.seek(0)  # Reset reader to start of file again after searching for ID
        for row in reader:
            # Search Username second
            if query.lower() == row['username'].lower():
                return row
        file.seek(0)  # Reset reader again after searching for Username
        for row in reader:
            # Search Email third
            if query.lower() == row['email'].lower():
                return row
        file.seek(0)  # Reset reader for the final keyword search
        # If no exact match, search by keyword (ID, Username, or Email)
        for row in reader:
            if query.lower() in row['id'].lower() or query.lower() in row['username'].lower() or query.lower() in row['email'].lower():
                return row
    return None

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        query = request.form['search_query']
        result = search_data(query)
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
