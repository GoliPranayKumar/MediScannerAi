import os
import base64
import logging
from flask import Flask, render_template, request, Response, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
try:
    from groq import Groq
except Exception:
    Groq = None
import markdown
from markupsafe import Markup

# Try to use full model, fallback to lite model
try:
    from ml_model import get_analyzer
except Exception:
    from ml_model_lite import get_analyzer

# Load environment variables from .env file
load_dotenv()

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "dicom"}

# Get absolute paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REACT_BUILD_DIR = os.path.join(BASE_DIR, "frontend", "build")

app = Flask(__name__, static_folder=os.path.join(REACT_BUILD_DIR, "static"), static_url_path="/static")
CORS(app)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Configure basic logging
logging.basicConfig(level=logging.INFO)

# Allow a GROQ API key to be provided via environment variable to avoid
# having to type it into the UI every time. This is useful for local testing.
ENV_GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Your medical analysis prompt
MEDICAL_QUERY = """
You are a medical imaging expert. Analyze this medical image and provide a brief, concise summary in 2-3 paragraphs:

1. What type of image is this and what body part does it show?
2. What are the main findings and any abnormalities detected?
3. What are the likely diseases or conditions based on these findings?

IMPORTANT: Format disease names in **bold** (e.g., **Pneumonia**, **Fracture**) to make them stand out.

Keep the explanation simple and direct. Avoid lengthy details and technical jargon. Focus only on the key observations and most likely diagnoses.
"""

def encode_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

@app.route("/api/analyze", methods=["POST"])
def analyze_image():
    """Analyze image using Groq API"""
    try:
        groq_api_key = ENV_GROQ_API_KEY
        if not groq_api_key:
            return jsonify({"error": "Groq API Key not configured"}), 400

        if "image" not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        file = request.files["image"]
        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({"error": "Allowed image types are png, jpg, jpeg, dicom"}), 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        base64_image = encode_image(filepath)
        if Groq is None:
            raise RuntimeError("Groq SDK is not available. Install the 'groq' package before using analysis.")

        client = Groq(api_key=groq_api_key)
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": MEDICAL_QUERY},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            model="meta-llama/llama-4-scout-17b-16e-instruct",
        )
        markdown_result = chat_completion.choices[0].message.content

        # Convert markdown to HTML
        result_html = markdown.markdown(markdown_result, extensions=["fenced_code", "tables"])
        
        return jsonify({"result": result_html}), 200
    
    except Exception as e:
        logging.exception("Error while performing analysis")
        return jsonify({"error": f"Error during analysis: {str(e)}"}), 500


@app.route("/api/ml-analyze", methods=["POST"])
def ml_analyze_image():
    """Analyze image using Deep Learning models (DenseNet + ResNet)"""
    try:
        if "image" not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        file = request.files["image"]
        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({"error": "Allowed image types are png, jpg, jpeg, dicom"}), 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        # Get analyzer instance
        analyzer = get_analyzer()
        
        # Perform ensemble analysis
        analysis_result = analyzer.ensemble_analysis(filepath)
        
        # Format results as HTML
        html_result = format_ml_analysis(analysis_result)
        
        return jsonify({"result": html_result, "analysis": analysis_result}), 200
    
    except Exception as e:
        logging.exception("Error during ML analysis")
        return jsonify({"error": f"Error during analysis: {str(e)}"}), 500


def format_ml_analysis(analysis_result):
    """Format ML analysis results as HTML"""
    try:
        if "error" in analysis_result:
            return f"<p style='color: red;'><strong>Error:</strong> {analysis_result['error']}</p>"
        
        html = "<div style='font-family: Arial, sans-serif;'>"
        
        # Ensemble Results
        if "ensemble_confidence" in analysis_result:
            html += f"""
            <h3>🤖 Ensemble Analysis Results</h3>
            <p><strong>Combined Confidence Score:</strong> {analysis_result['ensemble_confidence']:.2f}%</p>
            <p><strong>Recommendation:</strong> {analysis_result['recommendation']}</p>
            """
        
        # DenseNet Results
        if "densenet_result" in analysis_result and "error" not in analysis_result["densenet_result"]:
            dn = analysis_result["densenet_result"]
            html += f"""
            <h4>📊 DenseNet121 Analysis</h4>
            <p><strong>Top Prediction:</strong> {dn['top_prediction']}</p>
            <p><strong>Confidence:</strong> {dn['confidence']:.2f}%</p>
            <ul>
            """
            for pred in dn["predictions"][:3]:
                html += f"<li>{pred['class']}: {pred['confidence']:.2f}%</li>"
            html += "</ul>"
        
        # ResNet Results
        if "resnet_result" in analysis_result and "error" not in analysis_result["resnet_result"]:
            rn = analysis_result["resnet_result"]
            html += f"""
            <h4>📊 ResNet50 Analysis</h4>
            <p><strong>Top Prediction:</strong> {rn['top_prediction']}</p>
            <p><strong>Confidence:</strong> {rn['confidence']:.2f}%</p>
            <ul>
            """
            for pred in rn["predictions"][:3]:
                html += f"<li>{pred['class']}: {pred['confidence']:.2f}%</li>"
            html += "</ul>"
        
        html += "</div>"
        return html
    except Exception as e:
        return f"<p style='color: red;'>Error formatting results: {str(e)}</p>"


@app.route("/")
def serve_react():
    index_path = os.path.join(REACT_BUILD_DIR, "index.html")
    if os.path.exists(index_path):
        return send_from_directory(REACT_BUILD_DIR, "index.html")
    return "React app not built. Run 'npm run build' in the frontend directory.", 404


@app.route('/<path:path>')
def serve_static(path):
    if path != "" and os.path.exists(os.path.join(REACT_BUILD_DIR, path)):
        return send_from_directory(REACT_BUILD_DIR, path)
    return send_from_directory(REACT_BUILD_DIR, "index.html")


@app.route('/favicon.ico')
def favicon():
    return Response(status=204)

if __name__ == "__main__":
    app.run(debug=True)
