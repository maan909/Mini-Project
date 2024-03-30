from flask import Flask, flash,redirect,url_for,render_template,request
import pickle
import numpy as np
from counting import countvehicle
import datetime


from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)
app.secret_key='your_secret_key'
filename=''
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST','GET'])
def image():
    global filename
    if 'image' not in request.files:
        flash('No file part', 'error')
        return redirect(request.url)

    file = request.files['image']

    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(request.url)

    upload_path = 'F:\\Mini-Project'
    filename = file.filename
    file.save(upload_path + file.filename)
    flash('File uploaded successfully!', 'success')
    print("file saved successfully !")
    return redirect(request.url)

@app.route('/predict')
def predict():
        day = datetime.datetime.today().weekday() 
        date = datetime.datetime.now().day
        currenttime = datetime.datetime.now().strftime('%H:%M:%S')
        le = LabelEncoder()
        time = le.fit_transform([currenttime])
        time = float(time)
        #day = 7
        count = countvehicle(filename)
        CarCount = count[0]
        BikeCount = count[1]
        BusCount = count[2]
        TruckCount = count[3]
        TotalCount = CarCount+BikeCount+BusCount+TruckCount
        input = np.array([[time, date, day, CarCount, BikeCount, BusCount, TruckCount, TotalCount]])
        picklemodel = pickle.load(open('TrafficDensityModelSVM.pkl','rb'))
        result = picklemodel.predict(input)
        print(day)
        print(date)
        print(time)
        result = str(result[0])
        prediction = 'prediction'

        return redirect(url_for(prediction,trafficsituation=result))

    



@app.route('/prediction/<int:trafficsituation>')
def prediction(trafficsituation):
    if trafficsituation == 1:
        pre = "Low"
    elif trafficsituation == 2:
        pre = "normal"
    elif trafficsituation == 3:
        pre = "High"
    elif trafficsituation == 4:
        pre = "Heavy"
   
    return render_template('prediction.html', answer=pre)

if __name__=='__main__':
    app.run(debug=True)