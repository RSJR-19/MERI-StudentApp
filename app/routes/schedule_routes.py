import os
import tempfile
from flask import Blueprint, request, jsonify, session
from app.services.eaf_parser import extract_eaf_text

schedule = Blueprint("schedule", __name__)

@schedule.route("/extract-eaf", methods=["POST"])
def extract_eaf():
    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "Unauthorized access."
        }), 401

    if "eaf" not in request.files:
        return jsonify({
            "success": False,
            "message": "No PDF was uploaded."
        }), 400

    pdf = request.files["eaf"]

    if not pdf.filename:
        return jsonify({
            "success": False,
            "message": "Please select a PDF."
        }), 400

    if not pdf.filename.lower().endswith(".pdf"):
        return jsonify({
            "success": False,
            "message": "Only PDF files are accepted."
        }), 400

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            suffix=".pdf",
            delete=False
        ) as temp_file:

            temp_path = temp_file.name
            pdf.save(temp_path)

        extracted_text = extract_eaf_text(temp_path)

        if not extracted_text.strip():
            return jsonify({
                "success": False,
                "message": "No readable text found in the PDF."
            }), 422

        return jsonify({
            "success": True,
            "message": "PDF text extracted successfully.",
            "extracted_text": extracted_text
        })

    except Exception as e:
        print("EAF Extraction Error:", e)

        return jsonify({
            "success": False,
            "message": "Unable to process this PDF."
        }), 500

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)