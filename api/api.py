"""Practice using API to pull data"""



import requests

url = 'https://en.wikipedia.org/w/api.php?action=query&prop=extracts&format=json&exintro=&titles=pizza'

# Package the request, send the request and catch the response: r
r = requests.get(url)

# Decode the JSON data into a dictionary: json_data
json_data1 = r.json()

# Print the Wikipedia page extract
pizza_extract = json_data1['query']['pages']['24768']['extract']
print(pizza_extract)
print('\n', '\n')


# pull using specific db address and api key
url = 'http://www.omdbapi.com/?apikey=72bc447a&t=the+social+network'

# Package the request, send the request and catch the response: r
r = requests.get(url)

json_data = r.json()

# Print each key-value pair in json_data
for k in json_data.keys():
    print(k + ': ', json_data[k])