from flask import Flask, request, redirect, url_for, flash, jsonify, render_template
from features_calculation import doTheCalculation, returnSomething, get_prediction
import json
import pandas as pd
import numpy as np
import os
import tempfile
import flask_excel as excel

# This line sets the app directory as the working directory
app = Flask(__name__)


# The route to the api
@app.route('/api', methods=['POST'])
def get_result():
    """
    Function to be run at each API call
    """

    # This is how you jsonify a list
    # request_file = jsonify({"result": request.get_array(field_name='data_file')})

    if not request:
        return "No file"

    # This line creates a dataframe from a list of lists
    df = pd.DataFrame(request.get_array(field_name='data_file'))

    # The first row is the list of column names so set the column names to the first row
    df.columns = df.iloc[0, :]

    # Now remove the first row
    df = df[1:]

    # Print the dataframe to the console
    print(df)

    # These are the values given for the fields
    input_list = list(request.form.values())

    # These are the names of the fields, i.e. LotFrontage, LotArea etc...
    input_names = list(request.form)

    '''
    # This code section creates a dictionary where each key is a list of observations
    res = dict()
    i = 0
    for j in df.columns:
        res[i] = list(df[j])
        i += 1
    '''

    result = get_prediction(df, input_list)

    # This code section creates a dictionary where each key is a row in the dataframe
    res = dict()
    for i in range(len(df)):
        res[i] = list(df.iloc[i, :])

    # Return the result

    # return jsonify(res)
    return 'The predicted Sale Price of this house is: ' + str(round(result, 2))


# The home route
@app.route('/', methods=['GET'])
def home_page():
    # Show the index page
    return render_template('index.html')


# The route to the api
@app.route('/api2', methods=['POST'])
def get_result2():
    """
    Function run at each API call
    """

    # Get the request as a json
    jsonfile = request.get_json()

    # Convert the json file to dictionary and then data frame
    data = pd.read_json(json.dumps(jsonfile), orient='index', convert_dates=['dteday'])

    # Print the data frame to the console window as an intermediate step
    print(data)

    # Our response will be a dictionary
    res = dict()

    # Populate the dictionary
    for i in range(len(data['atemp'])):
        res[i] = 100*data['atemp'][i]

    # Return the result
    return jsonify(res)


@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        return jsonify({"result": request.get_array(field_name='file')})
    return '''
    <!doctype html>
    <title>Upload an excel file</title>
    <h1>Excel file upload (csv)</h1>
    <form action="" method=post enctype=multipart/form-data><p>
    <input type=file name=file><input type=submit value=Upload>
    </form>
    '''


# A route to the test page that simply returns hello
@app.route('/hello', methods=['GET'])
def hello():
    return 'Hello, World!'


if __name__ == '__main__':
    excel.init_excel(app)
    # Let the console know that the load is successful
    print("loaded OK")

    # Set to debug mode
    app.run(debug=True)
