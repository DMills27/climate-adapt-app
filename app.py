from flask import Flask, render_template, request, jsonify
from openepi_client import GeoLocation, BoundingBox
from openepi_client.soil import SoilClient
from openepi_client.weather import WeatherClient
import math

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get-started")
def get_started():
    return render_template("get_started.html")

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
        print("soil summary: ", soil_summary)

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

# print("get_soil_and_weather_data: ", get_soil_and_weather_data(59.0929, 28.9029, 200))

def suggest_farming_method(inputs):
    soil = inputs["soil_type"]
    area = inputs["land_area_m2"]
    temp = inputs["temperature"]
    rainfall = inputs["rainfall"]
    humidity = inputs["humidity"]

    if soil == "No information":
        # Fallback to general methods not soil-dependent
        if area < 50:
            return "Vertical Farming"
        elif area < 200:
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
    if soil == 'No information':
        return 'Greenhouses (CEA)'
    if soil in ['Phaeozems', 'Cambisols', 'Luvisols'] and land > 3000:
        return 'Silvopasture'
    return 'Aeroponics'

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
