import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Target URL
target_url = ""
target_link = ""

# Storage
vuln_forms = []

def extract_forms(url):
    response = requests.get(url, verify=False)
    return BeautifulSoup(response.text, features="html.parser")

def submit_form(url, form):
    response = requests.post(url, data=form, verify=False)
    return response

forms = extract_forms(target_url)

# Testing all the forms
for form in forms:
    is_vulnerable = False

    for c in "\"'":
        if is_vulnerable:
            break

        data = {}
        
        for input_tag in form.find_all("input"):
            if input_tag.attrs.get("type") == "hidden":
                # if the page has any hidden form, set its value to "" or some random values 
                # depending on the functionality of the form
                input_tag.attrs["value"] = get_random_value()
            name = input_tag.attrs.get("name")
            value = input_tag.attrs.get("value") + c
            if name is not None:
                # setting all fields to same value of 'test'
                input_tag.attrs["value"] = value
        
        # Include all input tags of form into the dictionary
        for input_tag in form.find_all("input"):
            name = element.get("name")
            value = element.get("value")
            if name and value:
                # Submitting form with all input tags (including hidden)
                url = target_link if target_link else target_url
                response = submit_form(url,form)
                
                # Trigger behavior like 
                if "unexpected input" in response.content.decode() and "Duplicate entry" not in response.content.decode():
                    print("SQL Injection vulnerability detected, form:")
                    print(form)
                    is_vulnerable = True
                    break