from urllib.request import urlretrieve
import pandas as pd
import matplotlib.pyplot as plt

url = 'https://s3.amazonaws.com/assets.datacamp.com/production/course_1606/datasets/winequality-red.csv'


urlretrieve(url, '2017.csv')

df = pd.read_csv('2017.csv', sep=';')

print(df.head())

pd.DataFrame.hist(df.iloc[:, 0:1])
plt.xlabel('fixed acidity (g(tartaric acid)/dm$^3$)')
plt.ylabel('count')
plt.show()