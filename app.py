import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def homepage():
    return(
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/tobs/start<br>"
        f"/api/v1.0/tobs/start/end<br/>"
        )


@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= "2016-08-24").filter(Measurement.date <= "2017-08-23").all()
    
    precipitation_list = [results]
    return jsonify(precipitation_list)

           
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.name, Station.station, Station.elevation).all()
    
    station_list = []
    
    for name, station, elevation in results:
        row = {}
        row["name"] = name
        row["station"] = station
        row["elevation"] = elevation
        station_list.append(row)
    return jsonify(station_list)
    
@app.route("/api/v1.0/tobs")
def tobs():
    results = session.query(Station.name, Measurement.date, Measurement.tobs).filter(Measurement.date >= "2016-08-23").filter(Measurement.date <= "2017-08-23").all()
    
    tobs_list = []
    for station, date, temperature in results:
        row = {}
        row["station"] = station
        row["date"] = date
        row["temperature"] = temperature
        tobs_list.append(row)
    
    return jsonify(tobs_list)

@app.route("/api/v1.0/tobs/<start>")
@app.route("/api/v1.0/tobs/<start>/<end>")
def dates(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results= session.query(*sel).filter(Measurement.date >= start).all()
        temp= list(np.ravel(results))
        return jsonify(temp)

    results= session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temp= list(np.ravel(results))
    return jsonify(temp)


if __name__ == '__main__':
    app.run(debug=True)