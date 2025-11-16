"""
Flask Web App for Testing AI Extraction Modules
Simple local testing interface for CV and JD extraction
With 2-step JD extraction support
"""

from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
import json
import asyncio
from datetime import datetime

# Import extraction modules
from extractors.cv_extractor import CVExtractor
from extractors.jd_extractor import JDExtractorService  # Updated import
from utils.file_utils import FileTextExtractor

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'temp_uploads'

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    """Serve favicon to prevent 404 errors"""
    return '', 204  # No content response

@app.route('/api/extract-jd', methods=['POST'])
def extract_jd():
    """Extract keywords from JD text - 2-step process"""
    try:
        data = request.get_json()
        jd_text = data.get('jd_text', '')
        ai_model = data.get('ai_model', 'gemini')
        
        if not jd_text or len(jd_text.strip()) < 50:
            return jsonify({
                'success': False,
                'error': 'JD text is too short. Please provide at least 50 characters.'
            }), 400
        
        # Initialize 2-step extractor service
        extractor = JDExtractorService(ai_model=ai_model)
        
        # Run async extraction in sync context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(extractor.extract_jd_data(jd_text))
        loop.close()
        
        if result['status'] == 'success':
            return jsonify({
                'success': True,
                'data': {
                    'keywords': result.get('keywords'),
                    'snapshot': result.get('snapshot')
                },
                'word_count': len(jd_text.split()),
                'extraction_time': result.get('extraction_time'),
                'steps_completed': result.get('steps_completed', 2),
                'timestamp': datetime.now().isoformat()
            })
        elif result['status'] == 'partial':
            return jsonify({
                'success': True,
                'data': {
                    'keywords': result.get('keywords'),
                    'snapshot': None
                },
                'word_count': len(jd_text.split()),
                'extraction_time': result.get('extraction_time'),
                'steps_completed': 1,
                'warning': 'Snapshot generation failed',
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Extraction failed'),
                'step_failed': result.get('step', 0)
            }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/extract-cv', methods=['POST'])
def extract_cv():
    """Extract keywords from CV file"""
    try:
        # Check if file is present
        if 'cv_file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file uploaded'
            }), 400
        
        file = request.files['cv_file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': f'Invalid file type. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        try:
            # Extract text first
            file_extractor = FileTextExtractor()
            cv_text = file_extractor.extract_text(filepath)
            
            if not cv_text:
                return jsonify({
                    'success': False,
                    'error': 'Failed to extract text from file'
                }), 400
            
            # Initialize CV extractor
            extractor = CVExtractor()
            
            # Extract keywords
            result = extractor.extract_from_text(cv_text)
            
            return jsonify({
                'success': True,
                'data': result,
                'extracted_text': cv_text,
                'word_count': len(cv_text.split()),
                'filename': filename,
                'timestamp': datetime.now().isoformat()
            })
            
        finally:
            # Clean up uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Check if Gemini client can be initialized
        from clients.gemini_client import get_gemini_client
        client = get_gemini_client()
        
        return jsonify({
            'status': 'healthy',
            'gemini_available': True,
            'model_info': client.get_model_info()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'gemini_available': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🚀 AI EXTRACTION TESTING SERVER")
    print("="*70)
    print("\n📍 Server starting at: http://localhost:5000")
    print("\n✅ Available endpoints:")
    print("   - GET  /              → Main testing interface")
    print("   - POST /api/extract-jd → JD extraction")
    print("   - POST /api/extract-cv → CV extraction")
    print("   - GET  /api/health     → Health check")
    print("\n💡 Open http://localhost:5000 in your browser")
    print("="*70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
