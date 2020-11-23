#!/usr/bin/env python3

import os
import sys
import shutil
import requests
import json
from requests.auth import HTTPBasicAuth

# Check whther required parameter is passed
if len(sys.argv) <= 1:
    sys.exit("[USAGE]\nPython3 "+os.path.basename(__file__)+" [PROJECT_NAME]")

# Maintain the execution in current working directory
os.chdir(os.getcwd())

# Initialization
BITBUCKET_URL='http://192.168.1.138:7990/'
BITBUCKET_USERNAME='admin'
BITBUCKET_PASSWORD='admin'
API_LIST_OF_REPOS_IN_PROJECT=BITBUCKET_URL+'rest/api/1.0/projects/'+sys.argv[1]+'/repos'
LIST_OF_REPOSITORIES=[]
LIST_OF_PROJECT_USERS=[]

def main():
    res = requests.get(API_LIST_OF_REPOS_IN_PROJECT, verify=False, auth=HTTPBasicAuth(BITBUCKET_USERNAME, BITBUCKET_PASSWORD)).json()
    NO_OF_REPOSITORIES=res['size']
    for item in res['values']:
        LIST_OF_REPOSITORIES.append(item['slug'])
    
    for repo in range(len(LIST_OF_REPOSITORIES)):
        API_LIST_OF_USERS_IN_PROJECT=BITBUCKET_URL+'rest/api/1.0/projects/'+sys.argv[1]+'/repos/'+LIST_OF_REPOSITORIES[repo]+'/permissions/users'
        res = requests.get(API_LIST_OF_USERS_IN_PROJECT, verify=False, auth=HTTPBasicAuth(BITBUCKET_USERNAME, BITBUCKET_PASSWORD)).json()
        for item in res['values']:
            store_details = {"repo":None, "user":None, "permission":None}
            store_details['repo'] = LIST_OF_REPOSITORIES[repo]
            store_details['user'] = item['user']['name']
            store_details['permission'] = item['permission']
            LIST_OF_PROJECT_USERS.append(store_details)
    print(LIST_OF_PROJECT_USERS)

if __name__ == '__main__':
    main()
