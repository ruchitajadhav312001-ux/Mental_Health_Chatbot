from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

# ===== SUPABASE CONFIG =====
SUPABASE_URL = "https://iywprvavelmmxyxpdyea.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml5d3BydmF2ZWxtbXh5eHBkeWVhIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2ODc1MDkwNCwiZXhwIjoyMDg0MzI2OTA0fQ.yHeJ48nudifvbskIegkR3W6wLGPSDFcKH_kYKwjUoQk"   # use SERVICE key for backend

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# =========================
@app.route("/get_contacts", methods=["POST","OPTIONS"])
def get_contacts():
    data = request.json
    user_id = data["user_id"]

    res = supabase.table("emergency_contacts")\
        .select("phone")\
        .eq("user_id", user_id)\
        .execute()

    return jsonify(res.data)


@app.route("/emergency", methods=["POST","OPTIONS"])
def emergency():
    data = request.json

    user_id = data["user_id"]
    lat = data["latitude"]
    lon = data["longitude"]

    res = supabase.table("emergency_contacts")\
        .select("*")\
        .eq("user_id", user_id)\
        .execute()

    contacts = res.data

    link = f"https://maps.google.com/?q={lat},{lon}"

    sent = []

    for c in contacts:
        sent.append(c["phone"])
        print("SEND TO:", c["phone"])

    return jsonify({
        "message":"Emergency triggered",
        "numbers": sent,
        "location": link
    })


if __name__ == "__main__":
    app.run(debug=True)