from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
from steganography import encode_message, decode_message

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            action = request.form.get('action')
            password = request.form.get('password', '').strip()

            # Make password mandatory
            if not password:
                return "Password is required for this action.", 400
            
            if action == 'encode':
                message = request.form.get('message', '').strip()
                if not message:
                    return "Secret message cannot be empty.", 400
                
                output_filename = f"encoded_{filename}"
                output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
                
                try:
                    encode_message(filepath, message, password, output_path)
                    return render_template('result.html', 
                                           action='encode',
                                           filename=output_filename,
                                           original_filename=filename)
                except Exception as e:
                    return f"Error encoding message: {str(e)}", 400
                    
            elif action == 'decode':
                try:
                    message = decode_message(filepath, password)
                    return render_template('result.html',
                                           action='decode',
                                           message=message,
                                           original_filename=filename)
                except Exception as e:
                    return f"Error decoding message: {str(e)}", 400
    
    return render_template('index.html')

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)