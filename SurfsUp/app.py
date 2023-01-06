import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station



#################################################
# Flask Setup
#################################################
app = Flask(__name__)




#################################################
# Flask Routes
#################################################

## Start at the homepage.
@app.route("/")
# List all the available routes.
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]<br/>"
        )




##/api/v1.0/precipitation
@app.route("/api/v1.0/precipitation")
# Create our session (link) from Python to the DB

def precipitation():
    session = Session(engine)

#Convert the query results from your precipitation analysis 
# (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
    results = session.query(Measurement.prcp, Measurement.date).\
    filter(Measurement.date >= "2016-08-23").all()

    session.close()
    
#Return the JSON representation of your dictionary.
    all_prcp = []
    for prcp, date in results:
            prcp_dict = {}
            prcp_dict["prcp"] = prcp
            prcp_dict["date"] = date
            all_prcp.append(prcp_dict)

    return jsonify(all_prcp)




#/api/v1.0/stations
@app.route("/api/v1.0/stations")

# Create our session (link) from Python to the DB
def stations():
    session = Session(engine)


    results = session.query(Station.id, Station.station, Station.name).all()

    session.close()

#Return a JSON list of stations from the dataset.
    all_station = []
    for id, station, name in results:
            station_dict = {}
            station_dict["id"] = id
            station_dict["station"] = station
            station_dict["name"] = name
            all_station.append(station_dict)

    return jsonify(all_station)




##/api/v1.0/tobs
@app.route("/api/v1.0/tobs")
def tobs():
# Create our session (link) from Python to the DB
    session = Session(engine)

#Query the dates and temperature observations of the most-active station 
# for the previous year of data.
    results = session.query(Measurement.date, Measurement.tobs, Measurement.prcp).\
    filter(Measurement.station == "USC00519281").\
        filter(Measurement.date >= "2016-08-23").all()

    session.close()

#Return a JSON list of temperature observations for the previous year.
    all_tobs = []
    for date, tobs, prcp in results:
            tobs_dict = {}
            tobs_dict["id"] = id
            tobs_dict["tobs"] = tobs
            tobs_dict["prcp"] = tobs
            all_tobs.append(tobs_dict)

    return jsonify(all_tobs)




#/api/v1.0/<start> and /api/v1.0/<start>/<end>
@app.route("/api/v1.0/<start_date>")
def Start_date(start_date):
    session = Session(engine)
   
    results = session.query(func.tmin(Measurement.tobs), \
        func.tmax(Measurement.tobs),\
            func.tavg(Measurement.prcp)).\
    filter(Measurement.date >= start_date).all()

    session.close()

#Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
#For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
    start_date_tobs = []
    for min, max, avg in results:
            start_date_tobs_dict = {}
            start_date_tobs_dict["min_temp"] = min
            start_date_tobs_dict["max_temp"] = max
            start_date_tobs_dict["avg_temp"] = avg
            start_date_tobs.append(start_date_tobs_dict)

    return jsonify(start_date_tobs_dict)

#For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.

@app.route("/api/v1.0/<start_date>/<end_date>")
def Start_end_date(start_date, end_date):
    session = Session(engine)
   
    results = session.query(func.tmin(Measurement.tobs), \
        func.tmax(Measurement.tobs),\
            func.tavg(Measurement.prcp)).\
    filter(Measurement.date >= start_date).filter(Measurement.date >= end_date).all()

    session.close()

    start_end_date_tobs = []
    for min, max, avg in results:
            start_end_date_tobs_dict = {}
            start_end_date_tobs_dict["min_temp"] = min
            start_end_date_tobs_dict["max_temp"] = max
            start_end_date_tobs_dict["avg_temp"] = avg
            start_end_date_tobs.append(start_end_date_tobs_dict)

    return jsonify(start_end_date_tobs_dict)