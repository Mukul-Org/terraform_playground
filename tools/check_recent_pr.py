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

# IGNOREPRABOVEMINUTES = 5

def main():

    TOKEN             = os.getenv('GITHUB_TOKEN')
    GITHUB_WORKSPACE  = os.getenv('GITHUB_WORKSPACE')
    GITHUB_REPOSITORY = os.getenv('GITHUB_REPOSITORY')

    response = open_pr(GITHUB_REPOSITORY)

    for pr in response.json():
        
        commentcheck = prcommentcheck(GITHUB_REPOSITORY, pr['number'])

        if(commentcheck == 'false'):
        # if(checkmindiff(pr['created_at']) and commentcheck == 'false'):
            print('PR # ' + str(pr['number']) + ' : Run Licence check...')
            
            # allfiles = lisencecheck(GITHUB_WORKSPACE)
            prfiles = pr_files(GITHUB_REPOSITORY,pr['number'])
            all_no_lisence_files = lisencecheck(GITHUB_WORKSPACE)
            pr_no_lisence_files = list(set.intersection(set(prfiles), set(all_no_lisence_files)))

            # print(files)
            if pr_no_lisence_files:
                comment = '<!-- Boilerplate Check -->\nApache 2.0 Lisence check failed!\n\nThe following files are missing the license boilerplate:\n'
                for x in range(len(pr_no_lisence_files)):
                    # print (files[x])
                    comment = comment + '\n' + pr_no_lisence_files[x]
                    # status = 'fail'
            else:
                comment = '<!-- Boilerplate Check -->\nApache 2.0 Lisence check successful!'
                # status = 'pass'

            # comment PR
            commentpr(GITHUB_REPOSITORY, pr['number'], comment, TOKEN)

            # if(status == 'fail'):
            #     raise ValueError('Apache 2.0 Lisence check failed!')

        else:
            print('PR # ' + str(pr['number']) + ' : Skip Licence check...')

def open_pr(GITHUB_REPOSITORY):
    try:
        response = requests.get('https://api.github.com/repos/'+ GITHUB_REPOSITORY +'/pulls')
        return response
    except requests.exceptions.RequestException as e: 
        raise SystemExit(e)

# def checkmindiff(pr_created_at):
#     now = datetime.datetime.now().astimezone(timezone('America/Los_Angeles'))
#     now = now.replace(microsecond=0)
#     # print(now)
#     d1 = dateutil.parser.parse(pr_created_at).astimezone(timezone('America/Los_Angeles'))
#     # print(d1)
#     # print(now - d1)
#     minutes = (now - d1).total_seconds() / 60
#     # print(minutes)
#     if(minutes <= IGNOREPRABOVEMINUTES):
#         return True
#     else:
#         return False

def prcommentcheck(GITHUB_REPOSITORY, pr):
    try:
        status = 'false'
        response = requests.get('https://api.github.com/repos/'+ GITHUB_REPOSITORY +'/issues/'+ str(pr) +'/comments')
        for comment in response.json():
            body = comment['body']
            if(body.startswith('<!-- Boilerplate Check -->')):
                # print(body)
                status = 'true'
                break
        return status
    except requests.exceptions.RequestException as e: 
        raise SystemExit(e)


def lisencecheck(GITHUB_WORKSPACE):
    all_no_lisence_files = []
    allfiles = check_boilerplate.main(GITHUB_WORKSPACE)
    # print(files)
    for x in range(len(allfiles)):
        all_no_lisence_files.append(allfiles[x].replace(GITHUB_WORKSPACE+'/', ""))
    # print(all_no_lisence_files)
    return all_no_lisence_files

def pr_files(GITHUB_REPOSITORY,pr):
    pr_files = []
    try:
        response = requests.get('https://api.github.com/repos/'+ GITHUB_REPOSITORY +'/pulls/'+ str(pr) +'/files')
        for file in response.json():
            if(file['status'] != 'removed'):
                pr_files.append(file['filename'])
            else:
                continue
        print(pr_files)
        return pr_files
    except requests.exceptions.RequestException as e: 
        raise SystemExit(e)    

def commentpr(GITHUB_REPOSITORY, pr, comment, TOKEN):
    headers = {'Authorization': f'token {TOKEN}', 'Accept': 'application/vnd.github.v3+json'}
    # print(comment)
    data = {"body":comment}
    try:
        response  = requests.post('https://api.github.com/repos/'+ GITHUB_REPOSITORY +'/issues/'+ str(pr) +'/comments', data=json.dumps(data), headers=headers)
        # print(response.text)
    except requests.exceptions.RequestException as e: 
        raise SystemExit(e)


if __name__ == '__main__':
    # main()
    pr_files('Mukul-Org/terraform_playground',55)
