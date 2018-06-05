# Copyright 2015 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#from __future__ import print_function
from watson_machine_learning_client import WatsonMachineLearningAPIClient

from flask import Flask, jsonify, render_template, json, Response, request, Markup, flash
import os
import dataset
import plotdata
import sys
from vvk17Utilities import JSONtoHTML

wml_credentials = {
        "url": "https://ibm-watson-ml.mybluemix.net",
        "username": "a3e27bf9-2b60-4844-88ec-dfff829edba5",
        "password": "25fe23d8-6a13-4523-8fe5-10dea01d97e0",
        "instance_id": "630e57b3-5e9f-4721-8251-1035c8b69563"
    }

wmc = WatsonMachineLearningAPIClient(wml_credentials)

#create flask application
app = Flask(__name__)

@app.route('/')
def Run():
    """
    Load the site page
    """
    print('run the app - stdout', file=sys.stdout)

    return render_template('index.html')


@app.route('/clientDescription')
def clientDescription():
    """
    Load clientDescription page
    """
    i_d = wmc.service_instance.get_details()
    p_d = json.dumps(i_d, indent=4) + "  "
    msg = Markup(JSONtoHTML(p_d))
    return render_template('clientDescription.html', data = msg)


@app.route('/clientDetails')
def clientDetails():
    """
    Load clientDetails page
    """
    i_d = wmc.repository.get_details()
    p_d = json.dumps(i_d, indent=4) + "  "
    msg = Markup(JSONtoHTML(p_d))
    return render_template('clientDetails.html', data=msg)

@app.route('/repositoryDefinitions')
def repositoryDefinitions():
    """
    Load repositoryDefinitions page
    """
    i_d = wmc.repository.get_definition_details()
    p_d = json.dumps(i_d, indent=4) + "  "
    msg = Markup(JSONtoHTML(p_d))
    return render_template('repositoryDefinitions.html', data=msg)

@app.route('/repositoryExperiments')
def repositoryExperiments():
    """
    Load repositoryExperiments page
    """
    i_d = wmc.repository.get_experiment_details()
    p_d = json.dumps(i_d, indent=4) + "  "
    msg = Markup(JSONtoHTML(p_d))
    return render_template('repositoryExperiments.html', data=msg)

@app.route('/repositoryModels')
def repositoryModels():
    """
    Load repositoryModels page
    """
    i_d = wmc.repository.get_model_details()
    p_d = json.dumps(i_d, indent=4) + "  "
    msg = Markup(JSONtoHTML(p_d))
    return render_template('repositoryModels.html', data=msg)


@app.route('/listAll')
def listAll():
    """
    Load listAll page
    """
    old_stdout = sys.stdout
    sys.stdout = open('file.txt', 'w')
    i_d = wmc.repository.list()
    sys.stdout.close()
    sys.stdout = old_stdout
    fl = open('file.txt','r')
    i_d = fl.read()
    fl.close()
    msg = Markup(i_d)
    return render_template('listAll.html', data=msg)

@app.route('/deviceacrossdays')
def Device_data_across_days():
    """
    Load deviceAcrossDays page
    """
    return render_template('deviceAcrossDays.html')


@app.route('/hourlyStatsTrends')
def Hourly_stats_trends():
    """
    Load hourlyStatsTrends page
    """
    return render_template('hourlyStatsTrends.html')


@app.route('/devicecorrelationanalysis')
def Device_correlation_analysis():
    """
    Load deviceCorrelationAnalysis page
    """
    return render_template('deviceCorrelationAnalysis.html')


@app.route('/deviceStatsAcrossDays')
def Device_stats_across_days():
    """
    Load deviceStatsAcrossDays page
    """
    return render_template('deviceStatsAcrossDays.html')


@app.route('/createdataset')
def Create_dataset():
    """
    Load createDataset page
    """
    return render_template('createDataset.html')


@app.route('/api/retrieve', methods =['GET','POST'])
def Retrieve_per_day():
    """
    Post call to retrieve data for a day for a device per user input
    """
    #retrieve the json from the ajax call
    jsonFile = ''
    if request.method == 'POST':
        jsonFile = request.json
        print ("post request", file=sys.stderr)

    #if jsonFile successfully posted..
    if jsonFile != '':
        # check all required arguments are present:
        if not all(arg in jsonFile for arg in ["deviceId","date"]):
            print("Missing arguments in post request", file=sys.stderr)
            return json.dumps({"status":"Error", "messages":"Missing arguments"}), 422
        inputDeviceId = jsonFile["deviceId"]
        inputDate = jsonFile["date"]
        print("retreived data: " + str(inputDeviceId) + " | " + str(inputDate), file=sys.stderr)

    #get data for device fields per day
    dataArray = plotdata.Device_data_per_day(inputDeviceId, inputDate)
    print("after func call", file=sys.stderr)
    #create and return the output json
    output = {"dataArray": dataArray, "deviceId": inputDeviceId, "date" : inputDate}
    return json.dumps(output)


@app.route('/api/retrieveAcrossDays', methods =['GET','POST'])
def Retrieve_across_days():
    """
    Post call to retrieve data across days for a device per user input
    """
    #retrieve the json from the ajax call
    jsonFile = ''
    if request.method == 'POST':
        jsonFile = request.json
        print ("post request")

    #if jsonFile successfully posted..
    if jsonFile != '':
        # check all required arguments are present:
        if not all(arg in jsonFile for arg in ["deviceId","startDate","endDate"]):
            print("Missing arguments in post request")
            return json.dumps({"status":"Error", "messages":"Missing arguments"}), 422
        inputDeviceId = jsonFile["deviceId"]
        inputStartDate = jsonFile["startDate"]
        inputEndDate = jsonFile["endDate"]
        print("retreived data: " + str(inputDeviceId) + " | " + str(inputStartDate) + " | " + str(inputEndDate))

    #get data for device fields across days
    dataArray = plotdata.Device_data_across_days(inputDeviceId, inputStartDate, inputEndDate)

    #create and return the output json
    output = {"dataArray": dataArray, "deviceId": inputDeviceId, "startdate" : inputStartDate, "enddate" : inputEndDate}
    return json.dumps(output)


@app.route('/api/hourlyStatsTrends', methods =['GET','POST'])
def Retrieve_hourly_stats_trends():
    """
    Post call to retrieve data across days for a device per user input with hourly stats and trends
    """
    #retrieve the json from the ajax call
    jsonFile = ''
    if request.method == 'POST':
        jsonFile = request.json
        print ("post request")

    #if jsonFile successfully posted..
    if jsonFile != '':
        # check all required arguments are present:
        if not all(arg in jsonFile for arg in ["deviceId","field","startDate","endDate"]):
            print("Missing arguments in post request")
            return json.dumps({"status":"Error", "messages":"Missing arguments"}), 422
        inputDeviceId = jsonFile["deviceId"]
        inputStartDate = jsonFile["startDate"]
        inputEndDate = jsonFile["endDate"]
        inputField = jsonFile["field"]
        print("retreived data: " + str(inputDeviceId) + " | " + str(inputField) + " | " + str(inputStartDate) + " | " + str(inputEndDate))

    #get data for device fields across days
    dataArray = plotdata.Device_data_across_days(inputDeviceId, inputStartDate, inputEndDate)

    #get hourly stats and trends for dataArray
    hourlyData = plotdata.Hourly_stats_trends(dataArray, inputField)

    #create and return the output json
    output = {"dataArray": dataArray, "hourlyData": hourlyData, "deviceId": inputDeviceId, "startdate" : inputStartDate, "enddate" : inputEndDate, "field": inputField}
    return json.dumps(output)


@app.route('/api/deviceStats', methods =['GET','POST'])
def Retrieve_device_stats():
    """
    Post call to retrieve device stats for devices
    """

    #retrieve the json from the ajax call
    json_file = ''
    if request.method == 'POST':
        json_file = request.json
        print ("post request")

    #if json_file successfully posted..
    if json_file != '':
        # check all required arguments are present:
        if not all(arg in json_file for arg in ["deviceIds","field","startDate","endDate"]):
            print("Missing arguments in post request")
            return json.dumps({"status":"Error", "messages":"Missing arguments"}), 422
        inputDeviceIds = json_file["deviceIds"]
        inputStartDate = json_file["startDate"]
        inputEndDate = json_file["endDate"]
        inputField = json_file["field"]
        print("retreived data: " + str(inputDeviceIds) + " | " + str(inputStartDate) + " | " + str(inputEndDate) + " | " + str(inputField))

    #split deviceIds from input
    deviceIds = inputDeviceIds.split(",")

    #get data for devices across days
    dataArray = plotdata.Devices_data_across_days(deviceIds, inputStartDate, inputEndDate)

    #get plot data to compare devices
    plotdataArray = plotdata.Devices_field_data(dataArray, deviceIds, inputField)

    #create and return the output json
    output = {"dataArray": dataArray, "deviceIds": deviceIds, "plotdata": plotdataArray, "startdate": inputStartDate, "enddate" : inputEndDate, "field": inputField}
    return json.dumps(output)


@app.route('/api/setDataset', methods =['GET','POST'])
def Set_dataset():
    """
    Post call to set active dataset in dataset.json
    """
    output = {}

    #retrieve the json from the ajax call
    jsonFile = ''
    if request.method == 'POST':
        jsonFile = request.json
        print ("post request")

    #if jsonFile successfully posted..
    if jsonFile != '':
        # check all required arguments are present:
        if not all(arg in jsonFile for arg in ["dataset"]):
            print("Missing arguments in post request")
            return json.dumps({"status":"Error", "messages":"Missing arguments"}), 422
        inputDataset = jsonFile["dataset"]
        print("retreived data: " + str(inputDataset)  )

    #call update datasets.json file
    return json.dumps(dataset.Set_dataset(inputDataset))


@app.route('/api/appendDataset', methods =['GET','POST'])
def Append_dataset():
    """
    Post call to append dataset.json file with user inputs
    """

    #retrieve the json from the ajax call
    jsonFile = ''
    if request.method == 'POST':
        jsonFile = request.json
        print ("post request")

    #if jsonFile successfully posted..
    if jsonFile != '':
        # check all required arguments are present:
        if not all(arg in jsonFile for arg in ["deviceIds","dates","datasetName","dbName"]):
            print("Missing arguments in post request")
            return json.dumps({"status":"Error", "messages":"Missing arguments"}), 422
        inputDeviceIds = jsonFile["deviceIds"]
        inputDates = jsonFile["dates"]
        inputDatasetName = jsonFile["datasetName"]
        inputDbName = jsonFile["dbName"]
        print("retreived data: " + str(inputDeviceIds) + " | " + str(inputDates) + " | " + str(inputDatasetName) + " | " + str(inputDbName))

    return json.dumps(dataset.Append_dataset(inputDeviceIds, inputDates, inputDatasetName, inputDbName))


@app.route('/api/getfields',methods=['GET'])
def Get_fields():
    """
    Get and return fields
    """
    #return fields array
    fields = ['connections','deviceCount','activeClients']
    return json.dumps(fields)


@app.route('/api/getdatasets',methods=['GET'])
def Get_datasets():
    """
    Get datasets name from dataset.json file
    """
    #return datasets array
    return json.dumps(dataset.Get_datasets())


@app.route('/api/getdataset',methods=['GET'])
def Get_dataset():
    """
    Get dataset name from dataset.json file
    """
    #return active dataset
    return json.dumps(dataset.Get_dataset())


@app.route('/api/getdates',methods=['GET'])
def Get_dates():
    """
    Get and return the dates from dataset
    """
    #return dates
    return json.dumps(dataset.Get_dates())

@app.route('/api/getdeviceids',methods=['GET'])
def Get_devices():
    """
    Get and return deviceIds from dataset
    """
    #return deviceIds
    return json.dumps(dataset.Get_devices())


@app.route('/api/getdbnames',methods=['GET'])
def Get_db_names():
    """
    Get and return database name initials from the Cloudant storage for dataset initialization
    """
    #return uniqueDbnames
    return json.dumps(dataset.Get_db_names())


@app.route('/api/getdbdates',methods=['GET'])
def Get_db_dates():
    """
    Get and returns dates from the Cloudant storage for dataset initialization
    """
    #return uniqueDates
    return json.dumps(dataset.Get_db_dates())


@app.route('/api/getdbdeviceids',methods=['GET'])
def Get_db_deviceids():
    """
    Get and returns dates from the Cloudant storage for dataset initialization
    """
    #retrun uniqueDeviceIds
    return json.dumps(dataset.Get_db_deviceids())


port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))
