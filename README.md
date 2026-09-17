# GeoMine — Mineral Hotspot Prediction API

GeoMine is a Flask REST API for scoring mineral exploration areas and persisting prediction results in SQLite. It exposes a replaceable, dependency-free inference layer that combines geology, geophysics, and remote-sensing evidence into a hotspot probability and `low`/`medium`/`high` classification.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

The API listens on `http://localhost:5000`.

## Endpoints

| Method | Endpoint | Description | Success |
| --- | --- | --- | --- |
| GET | `/api/v1/health` | Service health check | 200 |
| POST | `/api/v1/predictions` | Validate, infer, and persist a prediction | 201 |
| GET | `/api/v1/predictions` | List stored predictions | 200 |
| GET | `/api/v1/predictions/<id>` | Retrieve one prediction | 200 |

### Create a prediction

```bash
curl -X POST http://localhost:5000/api/v1/predictions \
  -H 'Content-Type: application/json' \
  -d '{
    "latitude": 23.5,
    "longitude": 87.2,
    "geology": 0.9,
    "geophysics": 0.8,
    "remote_sensing": 0.7
  }'
```

Coordinates must be within latitude `[-90, 90]` and longitude `[-180, 180]`. Evidence fields must be normalized to `[0, 1]`. Invalid input returns a structured `400`; an unknown prediction returns a structured `404`.

## Inference

The current baseline uses weighted evidence: geology `45%`, geophysics `35%`, and remote sensing `20%`. The inference function is isolated in `app/model.py`, so a trained model can replace it without changing the API or persistence contract.

## Testing

```bash
python -m unittest discover -s tests -v
```

The test suite covers health, 201 creation, inference output, persistence retrieval, 400 validation errors, and 404 not-found behavior.
