from flask import Flask, render_template, request, send_file
import os
from werkzeug.utils import secure_filename
from model import process_inventory_data
import pandas as pd
import traceback

app = Flask(__name__)
app.secret_key = 'your-secret-key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def validate_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        if 'Date' not in df.columns:
            return False, "CSV file must contain a 'Date' column"
        if 'Quantity' not in df.columns and 'Sales' not in df.columns:
            return False, "CSV file must contain either 'Quantity' or 'Sales' column"
        if len(df) < 7:
            return False, "CSV file must contain at least 7 data points"
        return True, "Valid CSV file"
    except Exception as e:
        return False, f"Error reading CSV file: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    result_html = None
    error_message = None
    
    if request.method == 'POST':
        try:
            if 'file' not in request.files:
                return render_template('index.html', error="No file uploaded")
            
            file = request.files['file']
            if file.filename == '':
                return render_template('index.html', error="No file selected")
            
            if file and file.filename.endswith('.csv'):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                is_valid, message = validate_csv(filepath)
                if not is_valid:
                    return render_template('index.html', error=message)
                
                result_html = process_inventory_data(filepath)
                
                os.remove(filepath)
                
                return render_template('index.html', result=result_html)
            else:
                error_message = "Please upload a CSV file"
        
        except Exception as e:
            app.logger.error(f"Error processing file: {str(e)}\n{traceback.format_exc()}")
            error_message = f"Error processing file: {str(e)}"
    
    return render_template('index.html', error=error_message)

if __name__ == '__main__':
    app.run(debug=True)
