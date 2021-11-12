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
import glob
import json
import shutil
import requests
from python_terraform import Terraform

def main(PR):

  TOKEN             = os.getenv('GITHUB_TOKEN')
  TERRAFORM_CLI_PATH  = os.getenv('TERRAFORM_CLI_PATH')
  GITHUB_REPOSITORY = os.getenv('GITHUB_REPOSITORY')
  
  print('****************************')
  print(os.getcwd()+'/*')
  print('****************************')
  print(glob.glob(os.getcwd()+'/*/*'))
  print('****************************')
  print(glob.glob(os.getcwd()+'/*/*/*'))
  print('****************************')
  print(glob.glob(os.getcwd()+'/*/*/*/*'))

  # Get Added / Modified files in PR
  modified_files, removed_files = pr_files(GITHUB_REPOSITORY, PR)

  # Get Working directories to run TF Plan on
  working_directories = get_working_directories(modified_files, removed_files)

  # Loop through all the identified working directories
  try:
    for dir in working_directories:
      comment, status = tf(TERRAFORM_CLI_PATH + '/' + dir)
      commentpr(GITHUB_REPOSITORY, PR, comment, TOKEN)
      if(status == 'fail'):
        sys.exit('Terraform Init or Terraform Plan FAILED for: '+ dir)
  except requests.exceptions.RequestException as e: 
    print('No working directory with TF configs in PR.')
    raise SystemExit(e)

def pr_files(GITHUB_REPOSITORY,pr):
    modified_files = []
    removed_files = []
    try:
        response = requests.get('https://api.github.com/repos/'+ GITHUB_REPOSITORY +'/pulls/'+ str(pr) +'/files')
        for file in response.json():
            if(file['status'] == 'removed'):
              removed_files.append(file['filename'])
            else:
              modified_files.append(file['filename'])

        print("Added/Modified Files:")
        print(modified_files)
        print("Removed Files:")
        print(removed_files)

        return modified_files, removed_files
    except requests.exceptions.RequestException as e: 
        raise SystemExit(e)  


def get_working_directories(modified_files, removed_files):
  modified_files_dir = []
  removed_files_dir = []

  for file in modified_files:
    modified_files_dir.append(os.path.dirname(file))

  for file in removed_files:
    removed_files_dir.append(os.path.dirname(file))

  working_directories = modified_files_dir + removed_files_dir
  working_directories = list(set(working_directories))

  print("Working Directories:")
  print(working_directories)

  return working_directories


def tf(dir):
  tr = Terraform(working_dir=dir)

  return_code_init, stdout_init, stderr_init = tr.init_cmd(capture_output=False)
  return_code_plan, stdout_plan, stderr_plan = tr.plan_cmd(capture_output=False,var={'parent':'organizations/1234567890', 'billing_account':'ABCD-EFGH-IJKL-MNOP'})
  
  if(return_code_init == 1):
    comment = 'Terraform Init FAILED!\nFor Module: ' + dir.replace(os.getenv('TERRAFORM_CLI_PATH')+'/', '')
    status = 'fail'
  if(return_code_plan == 1):
    comment = 'Terraform Plan FAILED!\nFor Module: ' + dir.replace(os.getenv('TERRAFORM_CLI_PATH')+'/', '')
    status = 'fail'
  else: 
    comment = 'Terraform Init & Terraform Plan SUCCESSFUL!\nFor Module: ' + dir.replace(os.getenv('TERRAFORM_CLI_PATH')+'/', '')
    status = 'pass'
  
  return comment, status


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

  if len(sys.argv) != 2:
    raise SystemExit('No PR passed.')
  main(sys.argv[1])