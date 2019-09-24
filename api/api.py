"""Practice using API to pull data"""



import requests

url = 'https://www.wikipedia.org/'

r = requests.get(url)

text = r.text

print(text)

# Assign URL to variable: url
url = 'http://www.omdbapi.com/?apikey=72bc447a&t=the+social+network'

# Package the request, send the request and catch the response: r
r = requests.get(url)

# Print the text of the response
print(r.text)