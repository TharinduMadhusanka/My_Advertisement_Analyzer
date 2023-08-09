import os
from database import add_to_db
from flask import Flask, request, jsonify, render_template
from nlp.webScraper import extract_article_info
from nlp.imagetotext import run_ocr, ocr_image_url
from nlp.pdftotext import run_pdf
import folium
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)

# Define the upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/members")
def members():
    return jsonify({"members": ["Anthony", "Jason", "Karl"]})


@app.route('/sendurl', methods=['POST'])
def receive_url_from_frontend():
    data = request.get_json()
    url = data.get('url')
    
    results = extract_article_info(url)

    print(url)
    
    map_view(results[-1])
    locations_list = list(results[-1].items())

    results = list(results)
    del results[-1]
    results.append(locations_list)

    add_to_db(results)
    
    for _ in results:
        print(_, "\n\n")


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


if __name__ == "__main__":
    app.run(debug=True)
