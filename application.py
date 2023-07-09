import numpy as np
import datetime as dt
import pandas as pd

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import desc
from sqlalchemy import inspect

from flask import Flask, jsonify

engine=create_engine(f"sqlite:///Resources/hawaii.sqlite")

Base=automap_base()
Base.prepare(autoload_with=engine)
Measurement=Base.classes.measurement
Station=Base.classes.station
app=Flask(__name__)

@app.route("/")
def welcome():
    return(
        f"Avaialble Routes:<br/>"
        f"/api/v1.0/precipitationc<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitationc")
def precipitationc():
    session=Session(engine)
    data=session.query(Measurement.date,Measurement.prcp).filter(Measurement.date<='2017-08-23',Measurement.date>='2016-08-23').order_by(Measurement.date)
    session.close()

    precp = []
    for date,prcp in data:
        precp_dict={}
        precp_dict[date]=prcp
        # precp_dict["date"]=date
        # precp_dict["prcp"]=prcp
        precp.append(precp_dict)

    return jsonify(precp)

@app.route("/api/v1.0/stations")
def station():
    session=Session(engine)
    stations=session.query(Station.station).all()
    session.close()
    all_station = list(np.ravel(stations))

    return jsonify(all_station)
    
@app.route("/api/v1.0/tobs")
def tobs():
    session=Session(engine)
    tobs=session.query(Measurement.date,Measurement.tobs).filter(Measurement.date>='2016-08-23').filter(Measurement.station=='USC00519281')
    session.close()
    tob_list=[]
    for date,tob in tobs:
        tob_dict={}
        tob_dict["date"]=date
        tob_dict["tob"]=tob
        tob_list.append(tob_dict)
    return jsonify(tob_list)


@app.route("/api/v1.0/<start>")
def trip1(start):
    session=Session(engine)

 # go back one year from start date and go to end of data for Min/Avg/Max temp   
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end =  dt.date(2017, 8, 23)
    trip_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    trip = list(np.ravel(trip_data))
    session.close()
    return jsonify(trip)
    
    # trip = list(np.ravel(trip_data))
    


@app.route("/api/v1.0/<start>/<end>")
def trip2(start,end):

  # go back one year from start/end date and get Min/Avg/Max temp     
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    end_date= dt.datetime.strptime(end,'%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end = end_date-last_year
    session=Session(engine)
    trip_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    trip = list(np.ravel(trip_data))
    return jsonify(trip)


if __name__ == '__main__':
    app.run(debug=True)

