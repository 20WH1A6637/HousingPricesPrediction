from flask import Flask, request, render_template
import pickle
from geopy.geocoders import Nominatim

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict',methods=['POST'])
def predict():
    """Grabs the input values and uses them to make prediction"""
    MedInc = float(request.form["MedInc"])
    HouseAge = float(request.form["HouseAge"])
    AveRooms = float(request.form["AveRooms"])
    AveBedrms = float(request.form["AveBedrms"])
    Population = float(request.form["Population"])
    AveOccup = float(request.form["AveOccup"])
    Latitude = float(request.form["Latitude"])
    Longitude = float(request.form["Longitude"])
    prediction = model.predict([[MedInc, HouseAge, AveRooms, AveBedrms,	Population,	AveOccup, Latitude,	Longitude]])  # this returns a list e.g. [127.20488798], so pick first element [0]
    output = int(round(prediction[0], 2) * 100000)
    geolocator = Nominatim(user_agent="my-app")
    location = geolocator.reverse(f"{Latitude}, {Longitude}")
    return render_template('index.html', prediction_text=f'A house in this location: {location} costs upto of ${output}')

if __name__ == "__main__":
    app.run()