import os
from flask import Flask, request, render_template, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
from vxp_patcher import VXPPatcher
import io

app = Flask(__name__)
app.secret_key = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'vxp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/patch', methods=['POST'])
def patch():
    if 'vxp_file' not in request.files:
        return render_template('index.html', error='No file uploaded')
    
    file = request.files['vxp_file']
    imsi = request.form.get('imsi', '').strip()
    
    if file.filename == '':
        return render_template('index.html', error='No file selected')
    
    if not imsi:
        return render_template('index.html', error='IMSI number is required')
    
    if not imsi.isdigit() or len(imsi) != 15:
        return render_template('index.html', error='IMSI must be exactly 15 digits')
    
    if not allowed_file(file.filename):
        return render_template('index.html', error='Only .vxp files are allowed')
    
    try:
        vxp_data = file.read()
        
        patcher = VXPPatcher(vxp_data)
        patcher.patch_imsi(imsi)
        patched_data = patcher.get_patched_data()
        
        original_filename = secure_filename(file.filename)
        filename_without_ext = original_filename.rsplit('.', 1)[0]
        patched_filename = f"{filename_without_ext}_patched.vxp"
        
        return send_file(
            io.BytesIO(patched_data),
            mimetype='application/octet-stream',
            as_attachment=True,
            download_name=patched_filename
        )
        
    except ValueError as e:
        return render_template('index.html', error=str(e))
    except Exception as e:
        return render_template('index.html', error=f'Error processing file: {str(e)}')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
