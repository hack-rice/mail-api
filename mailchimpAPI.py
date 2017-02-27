"""
Code for the MailChimp API for the Hack-Rice App.

Author:
Hamza Nauman
"""

import requests
import json
# import sys
import hashlib

# API_KEY = '5b304c282231deed394636cca6ff15e8-us14'
API_KEY = 'b91c082742d8f1ae8006737167647517-us12' # Hack Rice's API key
HOST = "https://us12.api.mailchimp.com/3.0/"
REMINDER_LIST_ID = '785a935423';
REMINDER_ENDPOINT = "lists/" + REMINDER_LIST_ID + "/members"
REMINDER_URL = "%s%s" % (HOST, REMINDER_ENDPOINT)



def create_new_list(name, company, address1, city, state, zip, permission_reminder, from_name, from_email, subject):
    """
    Creates a new empty list.
    :param name: The name of the list.
    :param company: The company name for the list.
    :param address1: The street address for the list contact.
    :param city: The city for the list contact.
    :param state: The state for the list contact.
    :param zip: The postal or zip code for the list contact.
    :param permission_reminder: Permission reminder for the list - description of why a subscriber is receiving email
    :param from_name: The default from name for campaigns sent to this list.
    :param from_email: The default from email for campaigns sent to this list.
    :param subject: The default subject line for campaigns sent to this list.
    :return:
    """
    ENDPOINT = "lists"

    url = "%s%s" % (HOST, ENDPOINT)

    params = {
        "name": name,
        "contact": {
            "company": company,
            "address1": address1,
            "city": city,
            "state": state,
            "zip": zip,
            "country": "US"
        },
        "permission_reminder": permission_reminder,
        "campaign_defaults": {
            "from_name": from_name,
            "from_email": from_email,
            "subject": subject,
            "language": "en"
        },
        "email_type_option": False
    }

    response = requests.post(url, auth=('', API_KEY), data=json.dumps(params))
    return response


# print(create_new_list("Testing With API", "Hamza Inc", "6320 Main St", "Houston", "Texas", "77005", "Because f you!",
#                       "Hamza Nauman", "lalahamza@lala.com", "Hello Hello"))


def add_to_list(list_id, email, first_name, last_name):
    """
    Adds a subscriber to the specified list.
    """
    ENDPOINT = "lists/" + list_id + "/members"

    url = "%s%s" % (HOST, ENDPOINT)

    params = {}
    params["status"] = "subscribed"
    params["email_address"] = email
    params["merge_fields"] = {"FNAME": first_name, "LNAME": last_name}

    response = requests.post(url, auth=('', API_KEY), data=json.dumps(params))
    return response.json()

# print (add_to_list("d0c0c7514d","hamzanauman@hotmail.com","Hamza","Nauman"))

def get_list_emails(response):
    return [member['email_address'] for member in response.json()['members']]

def add_to_reminder_list(email):
    response = requests.get(REMINDER_URL, auth=('', API_KEY));
    post_response = None
    # Check if the email is not in the list already
    if email not in get_list_emails(response):
        post_response = add_to_list(REMINDER_LIST_ID, email, "Hack Rice ", "Organizer")
    return post_response


def remove_from_reminder_list(email):
    response = requests.get(REMINDER_URL, auth=('', API_KEY))
    post_response = None
    # Check if the email is in the list to be able to delete it
    if email in get_list_emails(response):
        post_reponse = delete_from_list(REMINDER_LIST_ID, email)
    return post_response


def convert_email_to_md5(email):
    """
    Converts an email address of a user to hash values using MD5 Algorithm. Used as a helper function for
    delete_from_list.
    """
    m = hashlib.md5()
    m.update(email.lower().encode())
    return m.hexdigest()


def delete_from_list(list_id, email):
    """
    Delete a given email address from the list with the given list ID.
    """
    subscriber_hash = convert_email_to_md5(email)
    ENDPOINT = "lists/" + list_id + "/members/" + subscriber_hash

    url = "%s%s" % (HOST, ENDPOINT)

    response = requests.delete(url, auth=('', API_KEY))
    return response

# print(delete_from_list("d0c0c7514d", "hamzanauman@hotmail.com"))


def get_lists_info():
    """
    Returns a list of dictionaries, each containing information about each list of subscribers. Used as a helper
    function to get specific info about a list.
    """
    ENDPOINT = "lists"

    url = "%s%s" % (HOST, ENDPOINT)

    response = requests.get(url, auth=('', API_KEY))
    return response.json()["lists"]


# print (get_lists_info())

def get_list_id(list_name):
    """
    Returns the unique ID for a list given its name (letter case does not matter).
    """
    lists_info = get_lists_info()

    for list in lists_info:
        if list["name"].lower() == list_name:
            return list["id"]

# print(get_list_id("testing with api"))


def create_new_html_campaign(list_id, subject_line, title, from_name, reply_to):
    """
    Creates a new campaign with an HTML type, i.e. the content is in HTML. Returns campaign ID.
    """
    ENDPOINT = "campaigns"

    url = "%s%s" % (HOST, ENDPOINT)

    params = {
        "type": "regular",
        "recipients": {
            "list_id": list_id
        },
        "settings": {
            "subject_line": subject_line,
            "title": title,
            "from_name": from_name,
            "reply_to": reply_to
        }
    }

    response = requests.post(url, auth=('', API_KEY), data=json.dumps(params))

    if "id" in response:
        return response.json()["id"]
    else:
        return response


# print(create_new_html_campaign("d0c0c7514d", "Hello", "Test Campaign", "Hamza", "hn9@rice.edu"))


def set_campaign_content_html(campaign_id, html):
    """
    Set the content of a campaign given the HTML it will contain.
    """
    ENDPOINT = "campaigns/" + campaign_id + "/content"

    url = "%s%s" % (HOST, ENDPOINT)

    params = {
        "html": html
    }

    response = requests.put(url, auth=('', API_KEY), data=json.dumps(params))

    return response

#hello


def get_campaign_id(name):
    ENDPOINT = "campaigns"

    url = "%s%s" % (HOST, ENDPOINT)

    response = requests.get(url, auth=('', API_KEY))

    for campaign in response.json()["campaigns"]:
        if campaign["settings"]["title"] == name:
            return campaign["id"]

print(get_campaign_id("Apply Invite"))
print(get_campaign_id("Test Campaign"))
# print(set_campaign_content_html(get_campaign_id("Test Campaign"), "<p>Message goes here <p>"))


def send_campaign(campaign_id):
    ENDPOINT = "campaigns/" + campaign_id + "/actions/send"

    url = "%s%s" % (HOST, ENDPOINT)

    response = requests.post(url, auth=('', API_KEY))

    return response

# print(send_campaign(get_campaign_id("Test Campaign")))
