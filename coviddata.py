import requests
import json

def statewisedata(state):
    url = "https://api.covid19india.org/state_district_wise.json"

    payload = ""
    headers = {
        
        }

    response = requests.request("GET", url, data=payload, headers=headers)

    alldata = response.text
    
    statewisedata = json.loads(alldata)[state]

    totalactive = 0
    totalrecovered = 0
    totaldeaths = 0

    alldistricts = statewisedata["districtData"].keys()

    for district in alldistricts:
        totalactive = totalactive + statewisedata["districtData"][district]["active"]
        totalrecovered = totalrecovered + statewisedata["districtData"][district]["recovered"]
        totaldeaths = totaldeaths + statewisedata["districtData"][district]["deceased"]
    
    if totalactive > 1000:
        totalactive = str(int(totalactive/1000)) + 'K'
    
    if totalrecovered > 1000:
        totalrecovered = str(int(totalrecovered/1000)) + 'K'
    
    if totaldeaths > 1000:
        totaldeaths = str(int(totaldeaths/1000)) + 'K'
    
    finalresponse = {"State": state, "TotalActive": totalactive, "TotalRecovered": totalrecovered, "TotalDeaths": totaldeaths}

    return finalresponse

def districtwisedata(state, district):
    url = "https://api.covid19india.org/state_district_wise.json"

    payload = ""
    headers = {
        
        }

    response = requests.request("GET", url, data=payload, headers=headers)

    alldata = response.text
    
    statewisedata = json.loads(alldata)[state]

    totalactive = statewisedata["districtData"][district]["active"]
    totalrecovered = statewisedata["districtData"][district]["recovered"]
    totaldeaths = statewisedata["districtData"][district]["deceased"]
    
    if totalactive > 1000:
        totalactive = str(int(totalactive/1000)) + 'K'
    
    if totalrecovered > 1000:
        totalrecovered = str(int(totalrecovered/1000)) + 'K'
    
    if totaldeaths > 1000:
        totaldeaths = str(int(totaldeaths/1000)) + 'K'
    
    finalresponse = {"State": state, "District": district, "TotalActive": totalactive, "TotalRecovered": totalrecovered, "TotalDeaths": totaldeaths}

    return finalresponse