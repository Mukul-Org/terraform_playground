#!/usr/bin/env python3

# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import requests
import datetime
import check_boilerplate
from pprint import pprint
import dateutil.parser
from pytz import timezone

IGNOREPRABOVEMINUTES = 5
# GITHUB_REPOSITORY = 'GoogleCloudPlatform/rad-lab'
# GITHUB_REPOSITORY = 'Mukul-Org/terraform_playground'

def main(GITHUB_REPOSITORY):
    # print("Current DIR: " + os.path.dirname(os.getcwd()))
    open_pr(GITHUB_REPOSITORY)

def open_pr(GITHUB_REPOSITORY):
    response = requests.get('https://api.github.com/repos/'+ GITHUB_REPOSITORY +'/pulls')
    print(type(response.json()))
    print(response.json())
    for pr in response.json():
        print(type(pr))
        print(pr)
        print(type(pr['created_at']))
        print(pr['created_at'])
        if(checkmindiff(pr['created_at'])):
            print('PR # ' + str(pr['number']) + ' : Run Licence check...')
            lisencecheck(GITHUB_REPOSITORY)
        else:
            print('PR # ' + str(pr['number']) + ' : Skip Licence check...')
            # if lisencecheck(os.path.dirname(os.getcwd())):
            if lisencecheck(GITHUB_REPOSITORY):
                print("list is not empty")
                comment = 'Apache 2.0 Lisence check failed!'
            else:
                print("list is empty")
                comment = 'Apache 2.0 Lisence check successful!'

        # comment PR
        commentpr(GITHUB_REPOSITORY, pr['number'], comment)

def checkmindiff(pr_created_at):
    now = datetime.datetime.now().astimezone(timezone('America/Los_Angeles'))
    now = now.replace(microsecond=0)
    # print(now)
    d1 = dateutil.parser.parse(pr_created_at).astimezone(timezone('America/Los_Angeles'))
    # print(d1)
    # print(now - d1)
    minutes = (now - d1).total_seconds() / 60
    # print(minutes)
    if(minutes <= IGNOREPRABOVEMINUTES):
        return True
    else:
        return False

def lisencecheck(GITHUB_REPOSITORY):
    # files = os.system("python3 check_boilerplate.py "+GITHUB_REPOSITORY)
    files = check_boilerplate.main(GITHUB_REPOSITORY)
    # for x in range(len(files)):
    #     print (files[x])
    return files

def commentpr(GITHUB_REPOSITORY, pr, comment):
    response  = requests.post('https://api.github.com/repos/'+ GITHUB_REPOSITORY +'/issues/'+ str(pr) +'/comments', data = comment)
    print(response.text)

if __name__ == '__main__':
    if len(sys.argv) != 2:
      raise SystemExit('No repository passed.')
    main(sys.argv[1])