#%%
import requests
import json



headers = {
    'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
    'x-rapidapi-key': "7d340db5b7msh5cd2b4aa5f69fa5p139080jsnf055ec0e432c"
    }

#%%
def get_airports(headers, filt):
    url_locations = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/autosuggest/v1.0/UK/GBP/en-GB/"
    querystring = {"query": filt}
    response = requests.request("GET", url_locations, headers=headers, params=querystring)
    dict_places = {e['PlaceId']:e for e in json.loads(response.text)['Places']}
    return dict_places

get_airports(headers, 'España')
#%%
market_country = 'IT'
currency = 'EUR'

locale = 'en-US'
origin = 'MXP-sky'
dest = 'FCO-sky'
start_date = '2021-10-01'
url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/" + market_country + "/" + currency + "/" + locale + "/" + origin + "/" + dest + "/" + start_date 

#querystring = {"inboundpartialdate":"2021-10-05"}
response = requests.request("GET", url, headers=headers)#, params=querystring)
print(response.text)
print(json.loads(response.text)['Quotes'])
# %%
