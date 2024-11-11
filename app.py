import numpy as np

import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask,jsonify
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
Base.prepare(autoload_with=engine)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(bind=engine)
# create Flask app
app = Flask(__name__)
#Start at the homepage.

@app.route("/")
def home():
    print( " redirecting to the list of available route!")
    #List all the available routes.
    return (
         'here is the available route <br>'
            '/api/v1.0/precipitation<br>'
            '/api/v1.0/stations <br>'
            '/api/v1.0/tobs<br>'
            'Please input you start date after slash 2017-08-18<br> '
             '/api/v1.0/<start><br>'

             'please input your end date bellow after slash 2016-08-18<br>'
            '/api/v1.0/<end><br>'

            'please input your start and end date between and after slash <br>'
            '/api/v1.0/<start>/<end><br>'
            )
session.close()
@app.route("/api/v1.0/precipitation")
def preciptation():
    last12_month=dt.date(2017,8,23) - dt.timedelta(days=365)
    most_recent_date ="2017-08-23"
    session=Session(engine)
    #Convert the query results from your precipitation
    #analysis (i.e. retrieve only the last 12 months of
    #data) to a dictionary using date as the key and prcp as the value.
    prcp_data = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date < most_recent_date).\
                                filter(Measurement.date >=last12_month).all()

# Save the query results as a Pandas DataFrame. Explicitly set the column names
    date_preciptation = []
  
    for date,prcp in prcp_data:
        date_prep = {}
        date_prep["Date"] = date
        date_prep["Preciptation"] = prcp
        date_preciptation.append(date_prep)
    
    
     #Return the JSON representation of your dictionar
    return jsonify( date_preciptation)
session.close()  

@app.route("/api/v1.0/stations")
def stations():
    session=Session(bind=engine)
    #Return the JSON representation of your dictionar
    station_list=session.query(Measurement.station,func.count(Measurement.station)).\
                                group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    my_dict_list = []
    for station,count in station_list:
         my_list = {}
         my_list["Station"] = station
         my_list["Count"] = count
         my_dict_list.append(my_list)

    #Return the JSON representation of your dictionar
    return jsonify(my_dict_list)
session.close()

@app.route("/api/v1.0/tobs")
def tobs():
    session=Session(bind=engine)
    #Query the dates and temperature observations of the
    #most-active station for the previous year of data
    # the most active station is :'USC00519281'
    temp = session.query(Measurement.date,Measurement.tobs).filter(Measurement.station=='USC00519281').filter(Measurement.date <'2017-08-18').\
                        filter(Measurement.date >= '2016-08-18').all()
    temp_list=[]
    for date,tobs in temp:
         temp_dict = {}
         temp_dict["Date"]=date
         temp_dict["Temprature"]=tobs
         temp_dict["Station"]='USC00519281'
         temp_list.append(temp_dict)
    # converting to normal list from tuple:
    
    
    return jsonify(temp_list)
session.close()


@app.route("/api/v1.0/<start>")
def start_date(start):
    session=Session(bind=engine)
    start = "2017-08-18"
    start_temp=(session.query(Measurement.station,func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
                                filter(Measurement.date < start).group_by(Measurement.station).all())
    tobs_all_station = []
    for station,min,max,avg in start_temp:
        station_dict = {}
        station_dict["Station"]=station
        station_dict['Min_temp']=min
        station_dict['max_temp'] = max
        station_dict['avg_temp'] = avg
        tobs_all_station.append(station_dict)
    
    return jsonify(tobs_all_station)
session.close()

@app.route("/api/v1.0/<end>")
def end_date():
    session=Session(bind=engine)
    end =  "2016-08-18"
    end_temp=session.query(Measurement.station,func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
                        filter(Measurement.date > end).group_by(Measurement.station).all()
    end_all_station = []
    for station,min,max,avg in end_temp:
        station_dict = {}
        station_dict["Station"]=station
        station_dict['Min_temp']=min
        station_dict['max_temp'] = max
        station_dict['avg_temp'] = avg
        end_all_station.append(station_dict)
    return jsonify(end_all_station)
   
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    session=Session(engine)
    start = "2017-08-18"
    end =  "2016-08-18"
    start_end_temp=session.query(Measurement.station,func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
                                    filter(Measurement.date < start).filter(Measurement.date >= end).group_by(Measurement.station).all()
    end_start_all_station = []
    for station,min,max,avg in start_end_temp:
        end_start_dict = {}
        end_start_dict["Station"]=station
        end_start_dict['Min_temp']=min
        end_start_dict['max_temp'] = max
        end_start_dict['avg_temp'] = avg
        end_start_all_station.append( end_start_dict)
    return jsonify(end_start_all_station)
session.close()
if __name__ == '__main__':
            app.run(debug=True)