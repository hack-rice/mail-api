import requests
import json
import sys
import hashlib

API_KEY = '827fbe9ae72d2a67fc8544054b71e680-us14'
HOST = "https://us14.api.mailchimp.com/3.0/"

def get_lists_info():
    """
    Returns a list of dictionaries, each containing information about each list of subscribers.
    """
    ENDPOINT = "lists"

    url = "%s%s" % (HOST,ENDPOINT)

    response = requests.get(url, auth=('', API_KEY))
    return response.json()["lists"]

# print (get_lists_info())

def add_to_list(list_id,email,first_name,last_name):
    """
    Adds a subscriber to the specified list.
    """
    ENDPOINT = "lists/" + list_id + "/members" 

    url = "%s%s" % (HOST,ENDPOINT)

    params = {}
    params["status"] = "subscribed"
    params["email_address"] = email
    params["merge_fields"] = {"FNAME":first_name,"LNAME":last_name}

    response = requests.post(url,auth=('', API_KEY),data=json.dumps(params))
    return response.json()

# print (add_to_list("d0c0c7514d","hamzanauman@hotmail.com","Hamza","Nauman"))

def convert_email_to_md5(email):
    m = hashlib.md5()
    m.update(email.lower().encode())
    return (m.hexdigest())

def delete_from_list(list_id,email):
    subscriber_hash = convert_email_to_md5(email)
    ENDPOINT = "lists/" + list_id + "/members/" + subscriber_hash


    url = "%s%s" % (HOST,ENDPOINT)

    response = requests.delete(url,auth=('',API_KEY))
    return response

print (delete_from_list("d0c0c7514d","hamzanauman@hotmail.com"))
#Testing change
#Testing changes again
