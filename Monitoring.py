import os
import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

##  ----  MONITORING DATA VISUALIZATION FOR SPECIFIC TARGET LOCATIONS  ---  ###

##  ----  SCRIPT DESCRIPTION  ---  ##
##  1. Takes readings from survey data in csv files at different dates.
##  2. Translates data into  readable database that can be used to return data for given points 
##  3. Plots data for specific targets and plots circles representing amber and red trigger levels.
##  Data is plotted so that you can differentiate between data before construciton starts and data that is after construction started. Black = before, red = after. Xes for general points and red circle for most recent point.  


##  ----  USER INPUT/ ACTIONS  ---  ##
##  1. Import all csv data into folder with following headings for columns: 
##  (A) Target, (B) Location description, (C) Eastings baseline coordinate, (D) Northings baseline coordinate, (E) Height baseline coordinate, (F) Eastings coordinate of measured value, (G) Northings coordinate of measured value, (H) Height coordinate of measured value
##  N.B. folders should all be labelled YYYYMMDD so that script can decipher dates of readings

##  2. input date at which construction started in "main" function. This will allow the script to show the difference between movement before works and movement since works commencing

##  3. Enter lookup target in "main" function. This should match what is in column (A) of the csv file





def has_numbers(string):
    return any (char.isdigit() for char in string)

def translate_dates(file_name):
    year=int(file_name[0:4])
    month = int(file_name[4:6])
    day = int(file_name[6:8])
    hour = int(file_name[9:11])
    minute = int(file_name[11:13])
    date = datetime.datetime(year,month,day, hour, minute)
    return date

def scan_files(date_log,Targets):
    for file in os.listdir():
        file_name,file_ext = os.path.splitext(file)
        if file_ext == '.csv':
            date = translate_dates(file_name)
            if date in date_log:
                pass
            else:
                Targets = add_data(Targets,file,date)

def add_data(Targets,file,date):
    with open(file,'r') as f:
        reader = csv.reader(f)
        next(reader)
        
        for row in reader:
            if row[0] in Targets.keys():
                if row[5] != "NULL" and has_numbers(row[5]):
                    Targets[row[0]][date] = {}
                    Targets[row[0]][date]["Co-ordinates"] = [row[2],row[3],row[4]]
                    Targets[row[0]][date]["Measurements"] = [row[5],row[6],row[7]]
                    dX = round(1000*(float(row[5])-float(row[2])),5)
                    dY  = round(1000*(float(row[6])-float(row[3])),5)
                    dZ = round(1000*(float(row[7])-float(row[4])),5)
                    Targets[row[0]][date]["Horizontal movements"] = (dX**2 + dY**2)**0.5
                    Targets[row[0]][date]["Vertical movements"] = dZ
                    Targets[row[0]][date]["Movement Vector"] = [dX, dY, dZ]
                else:
                    pass
            else:
                if row[5] != "NULL" and has_numbers(row[5]):
                    Targets[row[0]]={}
                    Targets[row[0]][date] = {}
                    Targets[row[0]][date]["Co-ordinates"] = [row[2],row[3],row[4]]
                    Targets[row[0]][date]["Measurements"] = [row[5],row[6],row[7]]
                    dX = round(1000*(float(row[5])-float(row[2])),5)
                    dY  = round(1000*(float(row[6])-float(row[3])),5)
                    dZ = round(1000*(float(row[7])-float(row[4])),5)
                    Targets[row[0]][date]["Horizontal movements"] = (dX**2 + dY**2)**0.5
                    Targets[row[0]][date]["Vertical movements"] = dZ
                    Targets[row[0]][date]["Movement Vector"] = [dX, dY, dZ]
                else:
                    pass
    return Targets

def plot_points(Targets, trial, construction_start_date, trigger_levels):
    x1, y1, x2, y2 = [], [], [], []
    dates1, dates2 = [], []
    fig = go.Figure()
    for k in Targets[trial].keys():
        if k < construction_start_date:
            dates1.append(k)
            x1.append(Targets[trial][k]["Movement Vector"][0]) 
            y1.append(Targets[trial][k]["Movement Vector"][1])
        else:
            dates2.append(k)
            x2.append(Targets[trial][k]["Movement Vector"][0])
            y2.append(Targets[trial][k]["Movement Vector"][1])
    fig.add_trace(go.Scatter(x=x1,y=y1,mode='markers',hovertext=(dates1),marker=dict(size=10,color='blue'), name = "before construction"))
    fig.add_trace(go.Scatter(x=x2,y=y2,mode='markers',hovertext=(dates2),marker=dict(size=10,color='red'), name = "after construction"))
    fig.add_shape(type = "circle", xref = "x", yref = "y", x0 = trigger_levels[0]*-1, y0 = trigger_levels[0]*-1, x1 = trigger_levels[0], y1 = trigger_levels[0], line_color = "orange")
    fig.add_shape(type = "circle", xref = "x", yref = "y", x0 = trigger_levels[1]*-1, y0 = trigger_levels[1]*-1, x1 = trigger_levels[1], y1 = trigger_levels[1], line_color = "red")
    fig.update_layout(title=go.layout.Title(text = trial +"<br><sup>Plot Subtitle<sup>"))
    fig.update_yaxes(    scaleanchor="x",    scaleratio=1 )
    
    fig.show()

def main():
    Targets = {}
    date_log = []
    construction_start_date = datetime.datetime(2023,3,12)
    trigger_levels =[8,15]
    trial = "SO5.2"
    scan_files(date_log,Targets)
    plot_points(Targets, trial, construction_start_date, trigger_levels)
    

if __name__ == '__main__':
    main() 