import os
# from database import add_to_db
from flask import Flask, request, jsonify, render_template
from nlp.webScraper import extract_article_info
from nlp.imagetotext import run_ocr, ocr_image_url
from nlp.pdftotext import run_pdf
import folium
from flask_pymongo import PyMongo


from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from pymongo import MongoClient


from sendmail import sendMail
from datetime import datetime, timedelta
import random

verification_codes = {}

app = Flask(__name__)

# app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
# mongo = PyMongo(app)

# # Define the upload folder
# UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp")
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# -----------------------------------------------------------------------
# original code
# Configurations
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
app.config["UPLOAD_FOLDER"] = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "tmp")

# Extensions
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True)

# User Authentication
mongo = MongoClient(app.config["MONGO_URI"])
db_mongo = mongo.myDatabase

# ----------------------------------------------------------------


@app.route("/members")
def members():
    return jsonify({"members": ["Anthony", "Jason", "Karl"]})


@app.route('/sendurl', methods=['POST'])
def receive_url_from_frontend():
    data = request.get_json()
    url = data.get('url')

    results = extract_article_info(url)

    print(url)

    # map_view(results[-1])
    # locations_list = list(results[-1].items())

    # results = list(results)
    # del results[-1]
    # results.append(locations_list)

    # add_to_db(results)

    # for _ in results:
    #     print(_, "\n\n")

    return jsonify({'results': results})


@app.route("/map")
def map_view(geocoded_addresses):
    print("this func is called==============================================")
    # Create a folium map centered at the first location found
    if geocoded_addresses:
        map_center = (list(geocoded_addresses.values())[
                      0][0], list(geocoded_addresses.values())[0][1])
        map_obj = folium.Map(location=map_center, zoom_start=12)

        # Add markers for each geocoded address
        for address, (latitude, longitude) in geocoded_addresses.items():
            folium.Marker([latitude, longitude], popup=address).add_to(map_obj)

        map_path = "templates/geocoded_map.html"
        map_obj.save(map_path)
        return render_template("geocoded_map.html")  # Updated this line
    else:
        return "No addresses found."


@app.route('/sendIMGurl', methods=['POST'])
def receive_IMG_url_from_frontend():
    data = request.get_json()
    url = data.get('imageUrl')
    results = ocr_image_url(url, 3)
    print(url)
    print(results)

    # Return the results as a JSON response
    return jsonify({'results': results})


@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    results = run_ocr(file)
    return jsonify({'results': results})


@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    save_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(save_path)

    try:
        results = run_pdf(save_path)
        return jsonify({'results': results}), 200
    except Exception as e:
        print("Error processing PDF:", str(e))
        return jsonify({"error": "Error processing PDF"}), 500


# User Authentication_______________________________________________________________________________________


@app.route("/signup", methods=["POST"])
def signup():
    email = request.json["email"]
    password = request.json["password"]

    print("------------------signup code is called------------------")
    print(email, password)

    user_exists = db_mongo.users.find_one({"email": email})
    # print(user_exists)
    if user_exists:
        return jsonify({"error": "Email already exists"}), 409

    verification_code = random.randint(100000, 999999)  # generate_random_code()  # Generate a verification code
    expiration_time = datetime.now() + timedelta(minutes=1)
    verification_codes[email] = {
        "code": verification_code, "expiration_time": expiration_time}

    print("verification code: ", verification_code)
    # sendMail(email, verification_code)

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = {"email": email, "password": hashed_password}
    db_mongo.users.insert_one(new_user)

    return jsonify({
        "email": new_user["email"]
    })


@app.route("/verify", methods=["POST"])
def verify():
    email = request.json["email"]
    user_code = request.json["verificationCode"]

    if email in verification_codes:
        stored_code = verification_codes[email]["code"]
        expiration_time = verification_codes[email]["expiration_time"]


        print(datetime.now() , expiration_time)

        if datetime.now() < expiration_time and int(user_code.strip()) == stored_code:
            del verification_codes[email]  # Remove the used verification code

            return jsonify({"success": True})
        else:
            # detete the user from the database
            del verification_codes[email]
            db_mongo.users.delete_one({"email": email})
            return jsonify({"success": False})
    else:
        del verification_codes[email]
        # detete the user from the database
        db_mongo.users.delete_one({"email": email})
        return jsonify({"success": False})


@app.route("/login", methods=["POST"])
def login_user():
    email = request.json["email"]
    password = request.json["password"]

    print("------------------login code is called------------------")
    print("email: ", email, "\n", "Pasword: ", password, "\n")

    user = db_mongo.users.find_one({"email": email})

    if user is None:
        return jsonify({"error": "Invalid User Name"}), 401

    if not bcrypt.check_password_hash(user["password"], password):
        return jsonify({"error": "Incorrect Password"}), 401

    return jsonify({
        "email": user["email"]
    })


if __name__ == "__main__":
    app.run(debug=True)
