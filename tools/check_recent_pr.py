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
import json
import requests
import datetime
import check_boilerplate
from pprint import pprint
import dateutil.parser
from pytz import timezone

IGNOREPRABOVEMINUTES = 7000

def main():

    TOKEN             = os.getenv('GITHUB_TOKEN')
    GITHUB_WORKSPACE  = os.getenv('GITHUB_WORKSPACE')
    GITHUB_REPOSITORY = os.getenv('GITHUB_REPOSITORY')

    open_pr(GITHUB_REPOSITORY, TOKEN, GITHUB_WORKSPACE)

def open_pr(GITHUB_REPOSITORY, TOKEN, GITHUB_WORKSPACE):
    
    response = requests.get('https://api.github.com/repos/'+ GITHUB_REPOSITORY +'/pulls')

    for pr in response.json():
        if(checkmindiff(pr['created_at'])):
            print('PR # ' + str(pr['number']) + ' : Run Licence check...')
            files = lisencecheck(GITHUB_WORKSPACE)
            # print(files)
            if files:
                # print("list is not empty")
                comment = 'Apache 2.0 Lisence check failed!\n\nThe following files are missing the license boilerplate:\n'
                for x in range(len(files)):
                    # print (files[x])
                    comment = comment + '\n' + files[x].replace(GITHUB_WORKSPACE, ".")
            else:
                # print("list is empty")
                comment = 'Apache 2.0 Lisence check successful!'
        else:
            print('PR # ' + str(pr['number']) + ' : Skip Licence check...')

        # comment PR
        commentpr(GITHUB_REPOSITORY, pr['number'], comment, TOKEN)

def checkmindiff(pr_created_at):
    now = datetime.datetime.now().astimezone(timezone('America/Los_Angeles'))
    now = now.replace(microsecond=0)
    # print(now)
    d1 = dateutil.parser.parse(pr_created_at).astimezone(timezone('America/Los_Angeles'))
    # print(d1)
    # print(now - d1)
    minutes = (now - d1).total_seconds() / 60
    print(minutes)
    if(minutes <= IGNOREPRABOVEMINUTES):
        return True
    else:
        return False

def lisencecheck(GITHUB_WORKSPACE):
    files = check_boilerplate.main(GITHUB_WORKSPACE)
    # print(files)
    return files

def commentpr(GITHUB_REPOSITORY, pr, comment, TOKEN):
    headers = {'Authorization': f'token {TOKEN}', 'Accept': 'application/vnd.github.v3+json'}
    print(comment)
    data = {"body":comment}
    response  = requests.post('https://api.github.com/repos/'+ GITHUB_REPOSITORY +'/issues/'+ str(pr) +'/comments', data=json.dumps(data), headers=headers)
    print(response.text)

if __name__ == '__main__':
    main()