# 1. import Flask
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#db setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables 
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

@app.route("/")
def homepage():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"//api/v1.0/<start><br/>"
        f"//api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
   # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(measurement.date, measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_passengers = []
    for date, prcp in results:
        passenger_dict = {}
        passenger_dict["date"] = date
        passenger_dict["prcp"] = prcp
        all_passengers.append(passenger_dict)

    return jsonify(all_passengers)


@app.route("/api/v1.0/stations")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)


    # Query 
    results = session.query(station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query
    results = session.query(measurement.date, measurement.tobs).filter(measurement.date >= '2016-08-23').filter(measurement.station == 'USC00519397').all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)

@app.route("/api/v1.0/start")
def start():
   
    
    class Answer():
        def __init__(self, Start_Date):
            self.Start_Date= Start_Date 
            

    go = True
    while go:
        Start_Date = input("What is the Start Date? ")  
        answer = Answer(Start_Date)
        check = input("Would you like to put in another start date? (y/n) ")
        if(check.lower() == "y"):
            go = True
        else:
            go = False
    session = Session(engine)
    # Query
    TMIN = session.query(func.min(measurement.tobs)).filter(measurement.date >= Start_Date).all()
    TMax = session.query(func.max(measurement.tobs)).filter(measurement.date >= Start_Date).all()
    TAVG = session.query(func.avg(measurement.tobs)).filter(measurement.date >= Start_Date).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = (TMIN, TMax, TAVG)

    return jsonify(all_names)

@app.route("/api/v1.0/start/end")
def StartEnd():
    class Answer():
        def __init__(self, Start_Date, End_Date):
            self.Start_Date = Start_Date
            self.End_Date = End_Date
            
    go = True
    while go:
        Start_Date = input("What is the Start Date? ")
        End_Date = input("What is the End Date? ")
        check = input("Would you like to put in another start date? (y/n) ")
        if(check.lower() == "y"):
            go = True
        else:
            go = False
    
    session = Session(engine)
    # Query
    TMIN = session.query(func.min(measurement.tobs)).filter(measurement.date >= Start_Date).filter(measurement.date <= End_Date).all()
    TMax = session.query(func.max(measurement.tobs)).filter(measurement.date >= Start_Date).filter(measurement.date <= End_Date).all()
    TAVG = session.query(func.avg(measurement.tobs)).filter(measurement.date >= Start_Date).filter(measurement.date <= End_Date).all()
    session.close()

    # Convert list of tuples into normal list
    all_names = (TMIN, TMax, TAVG)

    return jsonify(all_names)

if __name__ == '__main__':
    app.run(debug=True)