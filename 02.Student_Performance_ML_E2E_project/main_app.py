
import numpy as np
import pandas as pd
from flask import Flask, request, render_template
# To call the customdata here...
from src.student_performace_MLProject.pipelines.prediction_pipeline import CustomData, PredictPipeline



# To call the customdata here...
application = Flask(__name__)

app = application

# Creating the Routes.
# Lets create a folder in local templates---.index.html

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict_datapoint', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        data = CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('race_ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get("lunch"),
            test_preparation_course=request.form.get("test_preparation_course"),
            reading_score=request.form.get("reading_score"),
            writing_score=request.form.get("writing_score")
        )

        pred_df = data.get_data_as_DataFrame()
        print("prediction dataframe:", pred_df)

        predict_pipeline = PredictPipeline()
        result = predict_pipeline.predict(pred_df)

        return render_template("home.html", result=result[0])

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8000)