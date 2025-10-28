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
    from ml_model_lite import extract_features_for_ml
import joblib
from pathlib import Path

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

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "ok", "message": "Backend is running"}), 200

@app.route("/api/analyze", methods=["POST"])
def analyze_image():
    """Analyze image using Groq API or fallback to ML models"""
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

        # Try Groq first if available
        groq_api_key = ENV_GROQ_API_KEY
        if groq_api_key and Groq is not None:
            try:
                base64_image = encode_image(filepath)
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
                result_html = markdown.markdown(markdown_result, extensions=["fenced_code", "tables"])
                return jsonify({"result": result_html}), 200
            except Exception as groq_error:
                logging.warning(f"Groq analysis failed, falling back to ML models: {groq_error}")
        
        # Fallback to ML models
        return ml_analyze_image()
    
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

        # If the analyzer provides an ensemble method (full ml_model), use it
        if hasattr(analyzer, 'ensemble_analysis'):
            analysis_result = analyzer.ensemble_analysis(filepath)
            html_result = format_ml_analysis(analysis_result)
            return jsonify({"result": html_result, "analysis": analysis_result}), 200

        # Fallback for lightweight analyzer: use analyze_image and optionally a saved classifier
        findings = analyzer.analyze_image(filepath)

        # Try to load a trained sklearn model if available and run prediction using features
        model_path = Path("model.joblib")
        model_info = None
        if model_path.exists():
            try:
                clf = joblib.load(model_path)
                feats = extract_features_for_ml(filepath)
                X = [[feats['mean_intensity'], feats['std_intensity'], feats['contrast'], feats['width'], feats['height']]]
                pred = clf.predict(X)[0]
                proba = clf.predict_proba(X).max() if hasattr(clf, 'predict_proba') else None
                model_info = {"prediction": str(pred), "confidence": float(proba) if proba is not None else None}
            except Exception as e:
                logging.exception('Error loading or running ML model')
                model_info = {"error": str(e)}

        # Simple HTML representation for findings
        html_result = "<div style='font-family: Arial, sans-serif;'>"
        if 'error' in findings:
            html_result += f"<p style='color:red;'>Error: {findings['error']}</p>"
        else:
            html_result += f"<h3>Image Quality Analysis</h3><p><strong>Type:</strong> {findings.get('image_type')}<br/>"
            html_result += f"<strong>Dimensions:</strong> {findings.get('dimensions')}<br/>"
            html_result += f"<strong>Mean intensity:</strong> {findings.get('mean_intensity')}<br/>"
            html_result += f"<strong>Contrast:</strong> {findings.get('contrast_ratio')}<br/>"
            html_result += f"<strong>Quality:</strong> {findings.get('quality_assessment')}<br/></p>"
            html_result += "<h4>Recommendations</h4><ul>"
            for r in findings.get('recommendations', []):
                html_result += f"<li>{r}</li>"
            html_result += "</ul>"

        if model_info is not None:
            html_result += "<h4>Trained Model Prediction</h4>"
            if 'error' in model_info:
                html_result += f"<p style='color:red;'>Model error: {model_info['error']}</p>"
            else:
                html_result += f"<p><strong>Prediction:</strong> {model_info.get('prediction')}"
                if model_info.get('confidence') is not None:
                    html_result += f" &nbsp; (<em>confidence: {model_info['confidence']:.2f}</em>)"
                html_result += "</p>"

        html_result += "</div>"

        return jsonify({"result": html_result, "analysis": findings, "model_info": model_info}), 200
    
    except Exception as e:
        logging.exception("Error during ML analysis")
        return jsonify({"error": f"Error during analysis: {str(e)}"}), 500


def format_ml_analysis(analysis_result):
    """Format ML analysis results as HTML using trained medical models"""
    try:
        if "error" in analysis_result:
            return f"<p style='color: red;'><strong>Error:</strong> {analysis_result['error']}</p>"
        
        html = "<div style='font-family: Arial, sans-serif; background: #f5f5f5; padding: 15px; border-radius: 8px;'>"
        
        # Trained Datasets Info
        if "trained_datasets" in analysis_result:
            html += "<div style='background: #e3f2fd; padding: 10px; border-radius: 5px; margin-bottom: 15px;'>"
            html += "<p style='margin: 0; font-size: 12px; color: #1976d2;'><strong>📚 Trained on Medical Datasets:</strong></p>"
            for dataset in analysis_result["trained_datasets"]:
                html += f"<p style='margin: 5px 0; font-size: 11px; color: #1565c0;'>• {dataset}</p>"
            html += "</div>"
        
        # Ensemble Results
        if "ensemble_confidence" in analysis_result:
            confidence = analysis_result['ensemble_confidence']
            color = "#d32f2f" if confidence >= 85 else "#f57c00" if confidence >= 70 else "#fbc02d" if confidence >= 50 else "#388e3c"
            html += f"""
            <div style='background: {color}20; border-left: 4px solid {color}; padding: 12px; margin-bottom: 15px; border-radius: 4px;'>
            <h3 style='margin-top: 0; color: {color};'>🤖 Ensemble Analysis (Trained Medical Models)</h3>
            <p style='margin: 8px 0;'><strong>Combined Confidence Score:</strong> <span style='font-size: 18px; color: {color};'>{confidence:.1f}%</span></p>
            <p style='margin: 8px 0;'><strong>Clinical Recommendation:</strong> {analysis_result['recommendation']}</p>
            </div>
            """
        
        # DenseNet Results (CheXpert-trained)
        if "densenet_result" in analysis_result and "error" not in analysis_result["densenet_result"]:
            dn = analysis_result["densenet_result"]
            html += f"""
            <div style='background: white; padding: 12px; margin-bottom: 12px; border-radius: 5px; border: 1px solid #ddd;'>
            <h4 style='margin-top: 0; color: #1976d2;'>🔬 DenseNet121 Analysis (CheXpert-trained)</h4>
            <p style='margin: 5px 0;'><strong>Dataset:</strong> {dn.get('dataset', 'CheXpert')}</p>
            <p style='margin: 5px 0;'><strong>Top Finding:</strong> <span style='color: #d32f2f; font-weight: bold;'>{dn['top_prediction']}</span></p>
            <p style='margin: 5px 0;'><strong>Confidence:</strong> {dn['confidence']:.1f}%</p>
            <p style='margin: 5px 0;'><strong>Top Detections:</strong></p>
            <ul style='margin: 5px 0; padding-left: 20px;'>
            """
            for pred in dn["predictions"][:3]:
                html += f"<li>{pred['class']}: {pred['confidence']:.1f}%</li>"
            html += "</ul></div>"
        
        # MobileNetV2 Results (MIMIC-CXR-trained)
        if "mobilenet_result" in analysis_result and "error" not in analysis_result["mobilenet_result"]:
            mn = analysis_result["mobilenet_result"]
            html += f"""
            <div style='background: white; padding: 12px; margin-bottom: 12px; border-radius: 5px; border: 1px solid #ddd;'>
            <h4 style='margin-top: 0; color: #388e3c;'>🔬 MobileNetV2 Analysis (MIMIC-CXR-trained)</h4>
            <p style='margin: 5px 0;'><strong>Dataset:</strong> {mn.get('dataset', 'MIMIC-CXR')}</p>
            <p style='margin: 5px 0;'><strong>Top Finding:</strong> <span style='color: #388e3c; font-weight: bold;'>{mn['top_prediction']}</span></p>
            <p style='margin: 5px 0;'><strong>Confidence:</strong> {mn['confidence']:.1f}%</p>
            <p style='margin: 5px 0;'><strong>Top Detections:</strong></p>
            <ul style='margin: 5px 0; padding-left: 20px;'>
            """
            for pred in mn["predictions"][:3]:
                html += f"<li>{pred['class']}: {pred['confidence']:.1f}%</li>"
            html += "</ul></div>"
        
        # Legacy ResNet support
        if "resnet_result" in analysis_result and "error" not in analysis_result["resnet_result"]:
            rn = analysis_result["resnet_result"]
            html += f"""
            <div style='background: white; padding: 12px; margin-bottom: 12px; border-radius: 5px; border: 1px solid #ddd;'>
            <h4 style='margin-top: 0;'>📊 ResNet50 Analysis</h4>
            <p style='margin: 5px 0;'><strong>Top Prediction:</strong> {rn['top_prediction']}</p>
            <p style='margin: 5px 0;'><strong>Confidence:</strong> {rn['confidence']:.1f}%</p>
            <ul style='margin: 5px 0; padding-left: 20px;'>
            """
            for pred in rn["predictions"][:3]:
                html += f"<li>{pred['class']}: {pred['confidence']:.1f}%</li>"
            html += "</ul></div>"
        
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
