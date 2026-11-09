import os
import tempfile
from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from app.services.eaf_parser import extract_eaf_text,parse_eaf_text


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

        with open(temp_path, "rb") as uploaded_file:
            if not uploaded_file.read(5).startswith(b"%PDF-"):
                return jsonify({
                    "success": False,
                    "message": "The uploaded file is not a valid PDF."
                }), 400
            
        extracted_text = extract_eaf_text(temp_path)

        if not extracted_text.strip():
            return jsonify({
                "success": False,
                "message": "No readable text found in the PDF."
            }), 422

        schedule_data = parse_eaf_text(extracted_text)

        return jsonify({
            "success": True,
            "message": "EAF schedule extracted successfully.",
            "schedule": schedule_data
        }), 200

    except ValueError as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 422

    except Exception as e:
        print("EAF Extraction Error:", e)

        return jsonify({
            "success": False,
            "message": "Unable to process this PDF."
        }), 500

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

@schedule.route("/schedule")
def schedule_page():

    if "user_id" not in session:
        return redirect(url_for("main.splash", destination="login"))

    return render_template("schedule/schedule.html")