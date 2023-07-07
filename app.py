from flask import Flask, render_template, request
import csv
from reportlab.pdfgen import canvas

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['csv_file']
    file_path = f"uploads/{file.filename}"
    file.save(file_path)

    create_certificates(file_path)

    return "Certificates generated successfully!"

def create_certificates(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row['Name']
            grade = row['Grade']
            school = row['School']
            day = row['Day']
            month = row['Month']
            year = row['Year']
            rank = row['Rank']

            certificate_filename = f"certificates/{name}.pdf"

            # Create a new PDF canvas
            c = canvas.Canvas(certificate_filename)

            # Customize the certificate layout
            c.setFont("Helvetica", 24)
            c.drawString(100, 700, f"Certificate of Achievement")
            c.setFont("Helvetica", 18)
            c.drawString(100, 600, f"Name: {name}")
            c.drawString(100, 550, f"Grade: {grade}")
            c.drawString(100, 500, f"School: {school}")
            c.drawString(100, 450, f"Date: {day} {month} {year}")
            c.drawString(100, 400, f"Rank: {rank}")
            # Customize further as needed

            # Save and close the PDF canvas
            c.save()

if __name__ == '__main__':
    app.run(debug=True)
