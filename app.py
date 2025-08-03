from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
from openepi_client import GeoLocation, BoundingBox
from openepi_client.soil import SoilClient
from openepi_client.weather import WeatherClient
from openepi_client.crop_health import CropHealthClient  # Added
import math
import os

app = Flask(__name__)

# --- Upload settings ---
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# --- Pages ---
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get-started")
def get_started():
    files = [f for f in os.listdir(UPLOAD_FOLDER)
             if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    
    file_health = {}
    for f in files:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], f)
        try:
            with open(file_path, "rb") as img_file:
                image_data = img_file.read()
                health_response = CropHealthClient.get_binary_prediction(image_data)
            scores = parse_health_response(health_response)
            disease_risk = assess_disease_risk(scores)
            file_health[f] = disease_risk
        except Exception as e:
            print(f"Error analyzing {f}: {e}")
            file_health[f] = {"status": "Error", "details": "Could not analyze image."}

    # --- Add dummy or real location info here ---
    lat, lon, area = 18.0, -76.8, 500  # example values; ideally come from user
    try:
        inputs = get_soil_and_weather_data(lat, lon, area)
        method = suggest_farming_method(inputs)
        method_info = get_method_info(method, inputs)
    except Exception as e:
        print(f"Failed to get method recommendation: {e}")
        method_info = None

    return render_template("get_started.html", files=files, file_health=file_health, method_info=method_info)



# --- Upload logic ---
@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    try:
        file.save(file_path)
        print(f"✅ Saved: {file_path}")
    except Exception as e:
        return jsonify({"error": "Save failed", "details": str(e)}), 500

    try:
        with open(file_path, "rb") as f:
            image_data = f.read()
        if len(image_data) == 0:
            return jsonify({"error": "Empty file"}), 400
    except Exception as e:
        return jsonify({"error": "Read failed", "details": str(e)}), 500

    try:
        # Call OpenEPI
        health_response = CropHealthClient.get_binary_prediction(image_data)

        # Parse safely
        try:
            scores = parse_health_response(health_response)
            disease_risk = assess_disease_risk(scores)
        except Exception as e:
            print(f"Parse error: {e}")
            disease_risk = {
                "status": "Error",
                "details": f"Failed to interpret results: {str(e)}"
            }

        return jsonify({
            "filename": file.filename,
            "health": disease_risk
        })

    except Exception as e:
        print(f"🚨 API call failed: {e}")
        return jsonify({
            "filename": file.filename,
            "health": {
                "status": "Error",
                "details": "Prediction failed (server error or unsupported image). Please try again later."
            }
        })


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    return redirect(url_for('get_started'))


# --- Crop Health Analysis ---
def parse_health_response(response):
    """
    Safely parse the response from CropHealthClient.get_binary_prediction().
    It may be a BinaryPredictionResponse object or an error dict.
    """
    # Case 1: It's an object with .model_dump() (Pydantic v2)
    if hasattr(response, 'model_dump'):
        data = response.model_dump()
        # Look for HLT, NOT_HLT, or other fields
        return {k: float(v) for k, v in data.items() if isinstance(v, (int, float))}

    # Case 2: It's a dictionary (e.g., error response)
    if isinstance(response, dict):
        if 'detail' in response:
            raise ValueError(f"API Error: {response['detail']}")
        return {k: float(v) for k, v in response.items() if isinstance(v, (int, float))}

    # Case 3: It's a string (fallback)
    if isinstance(response, str):
        scores = {}
        for item in response.strip().split():
            if '=' in item:
                key, value = item.split('=', 1)
                try:
                    scores[key] = float(value)
                except ValueError:
                    pass
        return scores

    raise ValueError(f"Unsupported response type: {type(response)}")


def assess_disease_risk(scores: dict):
    """
    Determine if the crop is healthy based on thresholds.
    High scores indicate disease presence.
    We'll flag if any disease score exceeds a threshold (e.g., > 1.0).
    """
    # Threshold for "likely diseased"
    THRESHOLD = 1.0

    # Extract crop type from keys (e.g., cassava, maize, etc.)
    crops = set()
    for key in scores:
        parts = key.split('_')
        if len(parts) >= 2:
            crop = parts[-1].lower()
            crops.add(crop.capitalize())

    high_risk = {k: v for k, v in scores.items() if v > THRESHOLD}

    if high_risk:
        top_issue = max(high_risk, key=high_risk.get)
        return {
            "status": "Unhealthy",
            "crop": ", ".join(crops),
            "details": f"Possible issue: {top_issue.replace('_', ' ').title()} (Score: {high_risk[top_issue]:.2f}). Consider taking action.",
            "score": high_risk[top_issue]
        }
    else:
        crop_list = ", ".join(crops) if crops else "Unknown"
        return {
            "status": "Healthy",
            "crop": crop_list,
            "details": "No major diseases detected. Crop appears healthy.",
            "score": 0.0
        }


# --- Farming logic ---
def area_to_bounding_box(lat, lon, area_m2):
    lat_deg_per_m = 1 / 111_320
    lon_deg_per_m = 1 / (40075000 * math.cos(math.radians(lat)) / 360)
    side_m = math.sqrt(area_m2)
    delta_lat = (side_m * lat_deg_per_m) / 2
    delta_lon = (side_m * lon_deg_per_m) / 2
    return BoundingBox(
        min_lat=lat - delta_lat,
        max_lat=lat + delta_lat,
        min_lon=lon - delta_lon,
        max_lon=lon + delta_lon
    )


def get_soil_and_weather_data(lat, lon, land_area_m2):
    bbox = area_to_bounding_box(lat, lon, land_area_m2)
    try:
        soil_summary = SoilClient.get_soil_type_summary(bounding_box=bbox)
        summaries = getattr(soil_summary.properties, 'summaries', [])
        if summaries:
            dominant_soil = summaries[0].soil_type.root
        else:
            dominant_soil = "No information"
    except Exception as e:
        print(f"Error retrieving soil data: {e}")
        dominant_soil = "No information"

    try:
        weather = WeatherClient.get_location_forecast(
            geolocation=GeoLocation(lat=lat, lon=lon)
        )
        forecast_day = weather.properties.timeseries[0].data.instant.details
        temperature = forecast_day.air_temperature
        precipitation = getattr(forecast_day, 'precipitation_amount', 10)
        humidity = getattr(forecast_day, 'relative_humidity', 50)
    except Exception as e:
        print(f"Error retrieving weather data: {e}")
        temperature = 25
        precipitation = 10
        humidity = 50

    return {
        "soil_type": dominant_soil,
        "temperature": temperature,
        "rainfall": precipitation,
        "humidity": humidity,
        "land_area_m2": land_area_m2
    }


def suggest_farming_method(inputs):
    soil = inputs["soil_type"]
    land = inputs["land_area_m2"]
    temp = inputs["temperature"]
    rain = inputs["rainfall"]
    humidity = inputs["humidity"]

    if soil == "No information":
        if land < 50:
            return "Vertical Farming"
        elif land < 200:
            return "Greenhouses (CEA)"
        else:
            return "Regenerative Ag"
    if soil in ['Chernozems', 'Luvisols', 'Phaeozems'] and land > 5000 and rain > 30:
        return 'Agroforestry'
    if soil in ['Gleysols', 'Histosols', 'Stagnosols'] and rain > 50:
        return 'Aquaponics'
    if soil in ['Solonchaks', 'Leptosols', 'Gypsisols'] and rain < 10:
        return 'Dryland Farming'
    if land < 100 and temp > 25:
        return 'Vertical Farming'
    if soil in ['Andosols', 'Ferralsols'] and rain > 40 and land > 1000:
        return 'Regenerative agriculture'
    if soil in ['Phaeozems', 'Cambisols', 'Luvisols'] and land > 3000:
        return 'Silvopasture'
    return 'Aeroponics'

def get_method_info(method, inputs=None):
    info = {
        "title": method,
        "description": "",
        "how_to_start": "",
        "tools": []
    }

    if method == "Vertical Farming":
        info["description"] = "A space-efficient method using stacked layers to grow crops indoors under controlled conditions."
        info["how_to_start"] = "Start with a small indoor setup using shelves, LED grow lights, and hydroponic trays. Choose fast-growing greens like lettuce or herbs."
        info["tools"] = ["LED grow lights", "Hydroponic system", "Growing trays", "Nutrient solution", "Climate control (fan/humidifier)"]

    elif method == "Greenhouses (CEA)":
        info["description"] = "Controlled Environment Agriculture using greenhouses to regulate temperature, humidity, and light."
        info["how_to_start"] = "Build or buy a small greenhouse. Install sensors and automated watering. Start with tomatoes or peppers."
        info["tools"] = ["Greenhouse frame", "Polycarbonate panels", "Irrigation system", "Thermostat", "Sensors (temp/humidity)"]

    elif method == "Regenerative Ag":
        info["description"] = "A holistic approach to farming that restores soil health, increases biodiversity, and captures carbon."
        info["how_to_start"] = "Stop tilling, introduce cover crops, rotate livestock, and avoid synthetic fertilizers. Begin with a soil test."
        info["tools"] = ["Soil testing kit", "Cover crop seeds", "No-till drill", "Livestock (optional)", "Compost spreader"]

    elif method == "Agroforestry":
        info["description"] = "Integrating trees and shrubs into crop and livestock systems to create more diverse, productive, and sustainable land use."
        info["how_to_start"] = "Plant tree rows between crop fields or integrate fruit trees with understory crops. Plan spacing carefully."
        info["tools"] = ["Tree saplings", "Shovels", "Mulch", "Drip irrigation", "Pruning shears"]

    elif method == "Aquaponics":
        info["description"] = "A symbiotic system combining aquaculture (fish) and hydroponics (soilless plants). Fish waste feeds plants."
        info["how_to_start"] = "Set up a fish tank connected to a grow bed. Cycle the system before adding fish and plants. Start with tilapia and leafy greens."
        info["tools"] = ["Fish tank", "Grow bed", "Pump", "Biofilter", "Fish food", "pH/Ammonia test kit"]

    elif method == "Dryland Farming":
        info["description"] = "Cultivating crops without irrigation in low-rainfall areas by maximizing soil moisture retention."
        info["how_to_start"] = "Use deep tillage, wide spacing, and drought-resistant crops like millet or sorghum. Mulch heavily."
        info["tools"] = ["Drought-resistant seeds", "Mulch", "Chisel plow", "Soil moisture meter", "Windbreaks"]

    elif method == "Silvopasture":
        info["description"] = "Combining trees, forage, and livestock grazing in a mutually beneficial system."
        info["how_to_start"] = "Introduce trees into pastureland. Use rotational grazing. Suitable for cattle, sheep, or goats."
        info["tools"] = ["Tree seedlings", "Fencing (rotational)", "Water troughs", "Grazing plan", "Shelter for animals"]

    elif method == "Aeroponics":
        info["description"] = "Growing plants in air with roots misted by nutrient-rich water. Highly efficient and water-saving."
        info["how_to_start"] = "Build or buy an aeroponic tower. Use a pump and misting nozzles. Monitor pH and nutrients daily."
        info["tools"] = ["Aeroponic tower", "High-pressure pump", "Misting nozzles", "Nutrient solution", "pH meter", "Timer"]

    else:
        # Default fallback
        info["description"] = "An innovative sustainable farming method suited to your land and climate."
        info["how_to_start"] = "Consult local agricultural experts and start with a small pilot plot."
        info["tools"] = ["Soil test kit", "Basic hand tools", "Research resources", "Local extension agent"]

    return info

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    lat = data.get("lat")
    lon = data.get("lon")
    area = data.get("area")

    if None in (lat, lon, area):
        return jsonify({"error": "Missing input parameters."}), 400

    try:
        features = get_soil_and_weather_data(lat, lon, area)
        recommendation = suggest_farming_method(features)
        return jsonify({"recommendation": recommendation})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000, threaded=True)