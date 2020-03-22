import streamlit as st
import pandas as pd
import numpy as np
import gpxpy
from glob import glob
import random
from gpxreader import pandas_data_frame_for_gpx as gpx2df
import secrets

st.title('Coronavirus transmissions contact tracing (team Virus Tracking)')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
                    'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text('Loading data... done!')

st.subheader('Number of people in contamination hotspot by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Map of all possible hosts at %s:00' % hour_to_filter)
st.map(filtered_data)

activities = glob("activities/*.gpx")
a = activities[3] 
g = gpx2df(gpxpy.parse(open(a,"r"))) 
gs = [] #pd.concat([gpx2df(gpxpy.parse(open(a,"r")))[0][0] for a in activities]) 
for i,a in enumerate(activities):
    gpx = gpx2df(gpxpy.parse(open(a,"r")))[0][0]
    gpx['device'] = secrets.token_hex(nbytes=16)
    gpx['colorR'] = random.randint(0,255)
    gpx['colorG'] = random.randint(0,255)
    gpx['colorB'] = random.randint(0,255)
    gpx.index = gpx.index.map(lambda x: x.replace(year=2020, month=3, hour=12, day=20))
    gs.append(gpx) 

gs = pd.concat(gs) 
st.write("Data gathered by multiple gnss enabled devices")
st.write(gs[['latitude', 'longitude', 'altitude', 'device']]) 
g0 = gs
midpoint=(np.average(g0['latitude']), np.average(g0['longitude'])) 

st.write('Location tracks of possible contamination, different color per device') 

st.deck_gl_chart(
        viewport={ 
            'latitude': midpoint[0], 
            'longitude':  midpoint[1], 
            'zoom': 18,
            #'pitch': 50,
            }, 
        layers=[{ 
            'type': 'ScatterplotLayer',
            'data': gs, 
            'radiusScale': 0.01, 
            'radiusMinPixels': 1, 
            #'getFillColor': [248, 24, 148], 
            }]
        )
