from flask import Flask, render_template, request
import csv
import os
from weasyprint import HTML

os.environ['QT_QPA_PLATFORM'] = 'xcb'
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

# ...

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

            # Custom HTML template for the certificate
            certificate_html = render_template('certificate_template.html',
                                               name=name,
                                               grade=grade,
                                               school=school,
                                               date=f"{day} {month} {year}",
                                               rank=rank)

            certificate_filename = f"certificates/{name}.pdf"

            # Generate PDF from HTML
            HTML(string=certificate_html).write_pdf(certificate_filename)

# ...

if __name__ == '__main__':
    app.run(debug=True)
