# import pandas to read in CSV files
import pandas as pd

# import matplotlib + seaborn for exploratory data analysis
import plotly.graph_objects as go
import plotly


# read in accident data CSVs for 2015 - 2017
acc15 = pd.read_csv('/Users/ianforrest/Desktop/coding/repos/DS_Safe-Routes/modeling/accident15.csv')
acc16 = pd.read_csv('/Users/ianforrest/Desktop/coding/repos/DS_Safe-Routes/modeling/accident16.csv')
acc17 = pd.read_csv('/Users/ianforrest/Desktop/coding/repos/DS_Safe-Routes/modeling/accident17.csv')

# combine acc15, acc16, acc17 into one dataframe
acc = acc15.append(acc16, sort=False, ignore_index = True)
acc = acc.append(acc17, sort=False, ignore_index = True)


# create city/state/latitude/longitude dataframe
acc_city_state = acc[['CITY', 'STATE', 'LATITUDE', 'LONGITUD']]

# remove unknown cities
acc_city_state = acc_city_state[acc_city_state['CITY'] > 0]
acc_city_state = acc_city_state[acc_city_state['CITY'] < 9997]

# remove unknown latitude/longitude
acc_city_state = acc_city_state[acc_city_state['LATITUDE'] < 700]
acc_city_state = acc_city_state[acc_city_state['LONGITUD'] < 700]

# add 'COUNT' column to dataframe, counts number of CITY/STATE combinations
acc_city_state['COUNT'] = acc_city_state.groupby(['CITY', 'STATE'])['STATE'].transform('count')
acc_city_state = acc_city_state.sort_values(by=['COUNT'], ascending=False)
acc_city_state = acc_city_state.groupby('COUNT').first().sort_values(by=['COUNT'], ascending=False)
acc_city_state = acc_city_state.reset_index()

# limit dataframe to top 100 cities with most crashes
top_100 = acc_city_state.head(100)
top_100 = top_100.replace(4120, 3382)


# City/State dictionary to interpret city/state geocodes
df = pd.read_csv('/Users/ianforrest/Desktop/coding/repos/DS_Safe-Routes/visualizations/FRPP GLC United States (1).xlsx - GeoLocation_UnitedStates.csv')
df.columns = ['ST_NAME', 'STATE', 'CITY', 'CT_NAME']

# merge city/state name dataframe with top_100 datafrate
top_100 = top_100.merge(df, how='left').drop_duplicates(['CITY', 'STATE'])

# format text of city/state columns
top_100['ST_NAME'] = top_100['ST_NAME'].str.title()
top_100['CT_NAME'] = top_100['CT_NAME'].str.title()

# combine city name, state name, and number of accidents into 'DESC' column
top_100['DESC'] = top_100['CT_NAME'] + ', ' + top_100['ST_NAME'] + ' - ' + top_100['COUNT'].map(str) + ' Accidents'


# create Plotly Scattergeo plot for top 100 accident cities from 2015 - 2017
fig = go.Figure(data=go.Scattergeo(
        lon = top_100['LONGITUD'],
        lat = top_100['LATITUDE'],
        text = top_100['DESC'],
        mode = 'markers',
        marker = dict(
            size = 8,
            opacity = 0.75,
            reversescale = True,
            autocolorscale = False,
            symbol = 'circle'),
        marker_color = '#13F1FC',
        hoverinfo = 'text',
        ))

fig.update_layout(
        geo_scope='usa',
    )
fig.show()
#plotly.offline.plot(fig, filename='top100.html')
# plotly.offline.plot(fig, include_plotlyjs='cdn', filename='top100tt.html')
