from flask import Flask, render_template, request, redirect, url_for
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# List to store file paths
uploaded_files = []

@app.route('/files')
def files():
    return render_template('files.html', uploaded_files=uploaded_files)


@app.route('/', methods=['GET', 'POST'])
def preview():
    if request.method == 'POST':
        # Save uploaded files with specific names
        html_file = request.files['html']
        css_file = request.files['css']
        html_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'index.html')
        css_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'style.css')
        html_file.save(html_filepath)
        css_file.save(css_filepath)

        # Track file paths
        uploaded_files.append((html_filepath, css_filepath))

        # Read uploaded files
        with open(html_filepath, 'r') as html_file, \
                open(css_filepath, 'r') as css_file:
            html = html_file.read()
            css = css_file.read()
            combined_html = f'<style>{css}</style>{html}'

        return render_template('preview.html', combined_html=combined_html)

    return '''
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="html" accept=".html">
            <input type="file" name="css" accept=".css">
            <input type="submit" value="Preview">
        </form>
    '''


if __name__ == '__main__':
    app.run(debug=True)
