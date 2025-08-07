from flask import Flask, request, render_template
import os
import csv
import pandas as pd
import joblib

app = Flask(__name__)

# Load trained model
model = joblib.load("LRmodel.pkl")

# Define location columns (must match training model)
location_columns = [
    'total_sqft,'bath,'price,'BHK,'1st Block Jayanagar,'1st Phase JP Nagar,'2nd Phase Judicial Layout,'	2nd Stage Nagarbhavi,'	5th Block Hbr Layout,'	5th Phase JP Nagar,'	6th Phase JP Nagar,'	7th Phase JP Nagar,'	8th Phase JP Nagar,'	9th Phase JP Nagar,'	AECS Layout,'	Abbigere,'	Akshaya Nagar,'	Ambalipura,'	Ambedkar Nagar,'	Amruthahalli,'	Anandapura,'	Ananth Nagar,'	Anekal,'	Anjanapura,'	Ardendale,'	Arekere,'	Attibele,'	BEML Layout,'	BTM 2nd Stage,'	BTM Layout,'	Babusapalaya,'	Badavala Nagar,'	Balagere,'	Banashankari,'	Banashankari Stage II,'	Banashankari Stage III,'	Banashankari Stage V,'	Banashankari Stage VI,'	Banaswadi,'	Banjara Layout,'	Bannerghatta,'	Bannerghatta Road,'	Basavangudi,'	Basaveshwara Nagar,'	Battarahalli,'	Begur,'	Begur Road,'	Bellandur,'	Benson Town,'	Bharathi Nagar,'	Bhoganhalli,'	Billekahalli,'	Binny Pete,'	Bisuvanahalli,'	Bommanahalli,'	Bommasandra,'	Bommasandra Industrial Area,'	Bommenahalli,'	Brookefield,'	Budigere,'	CV Raman Nagar,'	Chamrajpet,'	Chandapura,'	Channasandra,'	Chikka Tirupathi,'	Chikkabanavar,'	Chikkalasandra,'	Choodasandra,'	Cooke Town,'	Cox Town,'	Cunningham Road,'	Dasanapura,'	Dasarahalli,'	Devanahalli,'	Devarachikkanahalli,'	Dodda Nekkundi,'	Doddaballapur,'	Doddakallasandra,'	Doddathoguru,'	Domlur,'	Dommasandra,'	EPIP Zone,'	Electronic City,'	Electronic City Phase II,'	Electronics City Phase 1,'	Frazer Town,'	GM Palaya,'	Garudachar Palya,'	Giri Nagar,'	Gollarapalya Hosahalli,'	Gottigere,'	Green Glen Layout,'	Gubbalala,'	Gunjur,'	HAL 2nd Stage,'	HBR Layout,'	HRBR Layout,'	HSR Layout,'	Haralur Road,'	Harlur,'	Hebbal,'	Hebbal Kempapura,'	Hegde Nagar,'	Hennur,'	Hennur Road,'	Hoodi,'	Horamavu Agara,'	Horamavu Banaswadi,'	Hormavu,'	Hosa Road,'	Hosakerehalli,'	Hoskote,'	Hosur Road,'	Hulimavu,'	ISRO Layout,'	ITPL,'	Iblur Village,'	Indira Nagar,'	JP Nagar,'	Jakkur,'	Jalahalli,'	Jalahalli East,'	Jigani,'	Judicial Layout,'	KR Puram,'	Kadubeesanahalli,'	Kadugodi,'	Kaggadasapura,'	Kaggalipura,'	Kaikondrahalli,'	Kalena Agrahara,'	Kalyan nagar,'	Kambipura,'	Kammanahalli,'	Kammasandra,'	Kanakapura,'	Kanakpura Road,'	Kannamangala,'	Karuna Nagar,'	Kasavanhalli,'	Kasturi Nagar,'	Kathriguppe,'	Kaval Byrasandra,'	Kenchenahalli,'	Kengeri,'	Kengeri Satellite Town,'	Kereguddadahalli,'	Kodichikkanahalli,'	Kodigehaali,'	Kodigehalli,'	Kodihalli,'	Kogilu,'	Konanakunte,'	Koramangala,'	Kothannur,'	Kothanur,'	Kudlu,'	Kudlu Gate,'	Kumaraswami Layout,'	Kundalahalli,'	LB Shastri Nagar,'	Laggere,'	Lakshminarayana Pura,'	Lingadheeranahalli,'	Magadi Road,'	Mahadevpura,'	Mahalakshmi Layout,'	Mallasandra,'	Malleshpalya,'	Malleshwaram,'	Marathahalli,'	Margondanahalli,'	Marsur,'	Mico Layout,'	Munnekollal,'	Murugeshpalya,'	Mysore Road,'	NGR Layout,'	NRI Layout,'	Nagarbhavi,'	Nagasandra,'	Nagavara,'	Nagavarapalya,'	Narayanapura,'	Neeladri Nagar,'	Nehru Nagar,'	OMBR Layout,'	Old Airport Road,'	Old Madras Road,'	Padmanabhanagar,'	Pai Layout,'	Panathur,'	Parappana Agrahara,'	Pattandur Agrahara,'	Poorna Pragna Layout,'	Prithvi Layout,'	R.T. Nagar,'	Rachenahalli,'	Raja Rajeshwari Nagar,'	Rajaji Nagar,'	Rajiv Nagar,'	Ramagondanahalli,'	Ramamurthy Nagar,'	Rayasandra,'	Sahakara Nagar,'	Sanjay nagar,'	Sarakki Nagar,'	Sarjapur,'	Sarjapur  Road,'	Sarjapura - Attibele Road,'	Sector 2 HSR Layout,'	Sector 7 HSR Layout,'	Seegehalli,'	Shampura,'	Shivaji Nagar,'	Singasandra,'	Somasundara Palya,'	Sompura,'	Sonnenahalli,'	Subramanyapura,'	Sultan Palaya,'	TC Palaya,'	Talaghattapura,'	Thanisandra,'	Thigalarapalya,'	Thubarahalli,'	Thyagaraja Nagar,'	Tindlu,'	Tumkur Road,'	Ulsoor,'	Uttarahalli,'	Varthur,'	Varthur Road,'	Vasanthapura,'	Vidyaranyapura,'	Vijayanagar,'	Vishveshwarya Layout,'	Vishwapriya Layout,'	Vittasandra,'	Whitefield,'	Yelachenahalli,'	Yelahanka,'	Yelahanka New Town,'	Yelenahalli,'	Yeshwanthpur,'

]

@app.route('/')
def homepage():
    return render_template("homepage.html")

@app.route('/submit', methods=['POST'])
def submit():
    Location = request.form['location']
    Total_sqft = request.form['total_sqft']
    Bath = request.form['bath']
    BHK = request.form['bhk']

    # Save to CSV
    file_exists = os.path.isfile("data.csv")
    with open("data.csv", mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Location', 'Total_sqft', 'Bath', 'BHK'])
        writer.writerow([Location, Total_sqft, Bath, BHK])

    return '''
        <h2>✅ Data saved successfully!</h2>
        <form action="/predict" method="post">
            <input type="hidden" name="location" value="{0}">
            <input type="hidden" name="total_sqft" value="{1}">
            <input type="hidden" name="bath" value="{2}">
            <input type="hidden" name="bhk" value="{3}">
            <button type="submit">Predict Price</button>
        </form>
    '''.format(Location, Total_sqft, Bath, BHK)

@app.route('/predict', methods=['POST'])
def predict():
    Location = request.form['location']
    Total_sqft = float(request.form['total_sqft'])
    Bath = int(request.form['bath'])
    BHK = int(request.form['bhk'])

    # Build location one-hot encoding
    location_input = [0] * len(location_columns)
    if Location in location_columns:
        loc_index = location_columns.index(Location)
        location_input[loc_index] = 1

    # Full input vector
    input_vector = [Total_sqft, Bath, BHK] + location_input

    # Predict
    predicted_price = model.predict([input_vector])[0]

    return f"<h2>🏠 Predicted House Price: ₹ {predicted_price:,.2f}</h2>"

if __name__ == "__main__":
    app.run(debug=True)
