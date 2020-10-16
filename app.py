
import numpy as np
import os

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime, timedelta, date

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to the tables
measurement= Base.classes.measurement
station= Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Welcome to Honolulu, Hawaii's Climate Home Page:<br/>"
        f"Available Routes:<br/>"
        f"<br/>"
        f"List of Precipitation Data with Corresponding Dates:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"List of Stations:<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"List of Temperature Observations with Corresponding Dates:<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"List of Minimum/Average/Maximum Temperatures for a Given Start Date ('yyyy-mm-dd'):<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"<br/>"
        f"List of Minimum/Average/Maximum Temperatures for a Given Start-End Range ('yyyy-mm-dd'/'yyyy-mm-dd'):<br/>"
        f"/api/v1.0/&lt;start&gt/&lt;end&gt"
    )

#################################################
# Precipitation (prcp) Route
#################################################

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return dates and corresponding precipitation data"""

    # Open a communication session with the database
    session = Session(engine)

    # Query all precipitation data
    results = session.query(measurement.date, measurement.prcp).all()

    # Close the session
    session.close()

    # Convert list of tuples into normal list
    precipitation = list(np.ravel(results))
    print(precipitation)
    return jsonify(precipitation)

#################################################
# Stations Route
#################################################

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all the stations"""

    # Open a communication session with the database
    session = Session(engine)

    # Query all stations
    results = session.query(station.station, station.name).all()

    # close the session
    session.close()

    # Convert list of tuples into normal list
    stations = list(np.ravel(results))
    print(stations)
    return jsonify(stations)

#################################################
# Date & Temp Obs (tobs) for Most Active Station Route
#################################################

@app.route("/api/v1.0/tobs")
def tobs():
    """Return dates and corresponding temperature observation data for most active station (USC00519281) for the last year"""

    # Open a communication session with the database
    session = Session(engine)

    # Query all temperature observations for USC00519281 for the last year
    results = session.query(measurement.tobs).filter(measurement.station=='USC00519281').filter(measurement.date >= '2016-08-23').all()

    # Close the session
    session.close()

    # Convert list of tuples into normal list
    tobs = list(np.ravel(results))
    print(tobs)
    return jsonify(tobs)

#################################################
# Min/Max/Avg Temp Obs for Given Start Date Route
#################################################

@app.route("/api/v1.0/<start>")
def start(start):
    """Return Min/Avg/Max temps for a given start date"""

    # Open a communication session with the database
    session = Session(engine)

    # Date conversion
    start_date = start

    # Query min/avg/max temperature observations for start date on
    results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= start_date).all()

    # Close the session
    session.close()

    # Create a list of the results
    minavgmax_list = []
    for result in results:
        r = {}
        r["Start Date"] = start_date
        r["TMIN"] = result[0]
        r["TAVG"] = result[1]
        r["TMAX"] = result[2]
        minavgmax_list.append(r)
    return jsonify(minavgmax_list)

#################################################
# Min/Max/Avg Temp Obs for Given Start-End Date Range Route
#################################################

@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):
    """Return Min/Avg/Max temps for a given start-end date range"""

    # Open a communication session with the database
    session = Session(engine)

    # Date conversion
    start_date = start
    end_date = end

    # Query min/avg/max temperature observations for start date on
    results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= start_date).filter(measurement.date <= end_date)

    # Close the session
    session.close()

    # Create a list of the results
    minavgmax_startend_list = []
    for result in results:
        r = {}
        r["Start Date"] = start_date
        r["End Date"] = end_date
        r["TMIN"] = result[0]
        r["TAVG"] = result[1]
        r["TMAX"] = result[2]
        minavgmax_startend_list.append(r)
    return jsonify(minavgmax_startend_list)


if __name__ == '__main__':
    app.run(debug=True)
