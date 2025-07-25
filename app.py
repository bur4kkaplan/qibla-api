from flask import Flask, request, jsonify
from flask_cors import CORS
from pyproj import Geod
from math import atan, degrees

app = Flask(__name__)
CORS(app)

kaaba_lat = 21.4225
kaaba_lon = 39.8262
geod = Geod(ellps="WGS84")

@app.route("/qibla")
def qibla():
    try:
        lat = float(request.args.get("lat"))
        lon = float(request.args.get("lon"))
        acc = float(request.args.get("acc", 5))  # GPS doğruluğu (metre), varsayılan 5m
    except:
        return jsonify({"error": "Geçersiz lat/lon/acc"}), 400

    azimuth, _, distance = geod.inv(lon, lat, kaaba_lon, kaaba_lat)
    qibla_angle = (azimuth + 360) % 360

    # Açısal hata
    angle_error_deg = degrees(atan(acc / distance))

    # Maksimum kabul edilen hata (örn: 10°'ye kadar yön tayini geçerli sayılır)
    max_error_threshold = 10.0

    # Güven oranı
    confidence = max(0.0, min(1.0, 1 - (angle_error_deg / max_error_threshold))) * 100

    return jsonify({
        "qibla": round(qibla_angle, 2),
        "error": round(angle_error_deg, 2),
        "confidence": round(confidence, 2)
    })

if __name__ == "__main__":
    app.run()
