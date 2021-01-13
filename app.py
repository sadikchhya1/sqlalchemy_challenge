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

session=Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
    ' <h1>List all available api routes:</h1>\
        <ul><li><a href="/api/v1.0/precipitation">Precipitation</a></li>\
        <li><a href="/api/v1.0/stations">Stations</a></li>\
        <li><a href="/api/v1.0/tobs">Temperature</a></li>\
        <li>"/api/v1.0/start-date" and "/api/v1.0/start-date/end-date"</li></ul>'
    )

@app.route('/api/v1.0/precipitation')
def prcp():
    return {key:prcp for key, prcp in session.query(Measurement.date, Measurement.prcp).all()}

@app.route('/api/v1.0/stations')
def stations():
    return {station:name for station,name in session.query(Station.station,Station.name).all()}

@app.route('/api/v1.0/tobs')
def tobs():
    return {date:tobs for date,tobs in session.query(Measurement.date,Measurement.tobs).all()}

@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
def datedTemp(start,end="2017-08-23"):
    return {date:tobs for date,tobs in session.query(Measurement.date,Measurement.tobs).filter((Measurement.date>=start) & (Measurement.date<=end)).all()}
        
if __name__ == '__main__':
    app.run(debug=True)