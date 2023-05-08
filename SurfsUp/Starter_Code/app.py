# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine('sqlite:///Resources/hawaii.sqlite')

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with = engine)

# Save references to each table
measurements = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route('/')
def welcome():

    '''List of all available routes.'''
    return(
        f'Available Routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/temp/start/end<br/>'
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    year_ago = dt.datetime(2016, 8, 22)
    sel = [measurements.date,
           measurements.prcp]
    year_prcp = session.query(*sel).filter(measurements.date > year_ago).order_by(measurements.date.asc()).all()
    session.close()
    prcp_dict = {}
    for date, prcp in year_prcp:
        prcp_dict.update({date: prcp}) 
    return  jsonify(prcp_dict)

@app.route('/api/v1.0/stations')
def stations():
    results = session.query(station.station).all()
    session.close()
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

@app.route('/api/v1.0/tobs')
def tobs():
    year_ago = dt.datetime(2016, 8, 22)
    year_temps = session.query(measurements.tobs).filter(measurements.date >= year_ago).\
        filter(measurements.station == 'USC00519281').all()
    session.close()
    tobs = list(np.ravel(year_temps))
    return jsonify(tobs)

@app.route("/api/v1.0/temp/<start>")
def start(start=None,end=None):
    values = [func.min(measurements.tobs), 
              func.avg(measurements.tobs),
              func.max(measurements.tobs)
              ] 
    result = session.query(*values).filter(measurements.date >= start).all()
    session.close()
    output = list(np.ravel(result))
    return jsonify(output)

@app.route("/api/v1.0/temp/<start>/<end>")
def start_end(start=None,end=None):
    values = [func.min(measurements.tobs), 
              func.avg(measurements.tobs),
              func.max(measurements.tobs)
              ] 
    result = session.query(*values).filter(measurements.date >= start).filter(measurements.date <= end).all()
    session.close()
    output = list(np.ravel(result))
    return jsonify(output)


if __name__ == '__main__':
    app.run(debug=True)