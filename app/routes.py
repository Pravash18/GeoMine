"""GeoMine REST API routes."""
from flask import Blueprint, jsonify, request

from .db import get_db
from .model import predict

api = Blueprint("api", __name__)
REQUIRED = ("latitude", "longitude", "geology", "geophysics", "remote_sensing")


def _validate_payload(payload):
    if not isinstance(payload, dict):
        return "Request body must be a JSON object."
    missing = [field for field in REQUIRED if field not in payload]
    if missing:
        return f"Missing required field(s): {', '.join(missing)}."
    try:
        for field in REQUIRED:
            value = float(payload[field])
            if field in ("latitude", "longitude"):
                limit = 90 if field == "latitude" else 180
                if not -limit <= value <= limit:
                    return f"{field} must be between {-limit} and {limit}."
            elif not 0 <= value <= 1:
                return f"{field} must be between 0 and 1."
    except (TypeError, ValueError):
        return "Coordinates and evidence signals must be numeric."
    return None


def _serialize(row):
    item = dict(row)
    item["latitude"] = float(item["latitude"])
    item["longitude"] = float(item["longitude"])
    for key in ("geology", "geophysics", "remote_sensing", "probability"):
        item[key] = float(item[key])
    return item


@api.get("/health")
def health():
    return jsonify({"status": "ok", "service": "geomine"})


@api.post("/predictions")
def create_prediction():
    payload = request.get_json(silent=True)
    error = _validate_payload(payload)
    if error:
        return jsonify({"error": {"code": "VALIDATION_ERROR", "message": error}}), 400
    fields = {key: float(payload[key]) for key in REQUIRED}
    probability, classification = predict({key: fields[key] for key in ("geology", "geophysics", "remote_sensing")})
    db = get_db()
    cursor = db.execute(
        """INSERT INTO predictions
        (latitude, longitude, geology, geophysics, remote_sensing, probability, classification)
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (*[fields[key] for key in REQUIRED], probability, classification),
    )
    db.commit()
    row = db.execute("SELECT * FROM predictions WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return jsonify({"data": _serialize(row)}), 201


@api.get("/predictions")
def list_predictions():
    rows = get_db().execute("SELECT * FROM predictions ORDER BY id DESC").fetchall()
    return jsonify({"data": [_serialize(row) for row in rows], "count": len(rows)})


@api.get("/predictions/<int:prediction_id>")
def get_prediction(prediction_id):
    row = get_db().execute("SELECT * FROM predictions WHERE id = ?", (prediction_id,)).fetchone()
    if row is None:
        return jsonify({"error": {"code": "NOT_FOUND", "message": "Prediction not found."}}), 404
    return jsonify({"data": _serialize(row)})
