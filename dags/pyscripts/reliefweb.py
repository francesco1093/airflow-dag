# %%
import requests
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import SubscriptionClient
from azure.storage.blob import BlobClient
from datetime import datetime

def extract_res(datalake, container, resource):
    url = "https://api.reliefweb.int/v1/" + resource + "?app=fra-app" 
    response = requests.request("GET", url)#, params=querystring)

    blob_service_client = BlobServiceClient(account_url=datalake, credential = DefaultAzureCredential())
    container_client = blob_service_client.get_container_client(container)
    
    fn = "reliefweb_" + resource + "_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
      
    with open(fn  + ".txt", "w") as tf:
        tf.write(response.text + "\n")

    with open(fn  + ".txt", "rb") as data:
        container_client.upload_blob(name=fn, data=data)

    return "Written to blob: " + fn