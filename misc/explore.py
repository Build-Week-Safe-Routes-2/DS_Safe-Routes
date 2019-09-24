import pandas as pd

acc = pd.read_csv('/Users/ianforrest/Desktop/coding/repos/DS_Safe-Routes/ACCIDENT.CSV')
acc_loc = acc[['ST_CASE', 'latitude', 'longitud']]

print(acc_loc.describe())