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

def main(PR):

  TOKEN             = os.getenv('GITHUB_TOKEN')
  GITHUB_REPOSITORY = os.getenv('GITHUB_REPOSITORY')

  modified_files, removed_files = pr_files(GITHUB_REPOSITORY, PR)

  print("Added/Modified Files:")
  print(modified_files)
  print("Removed Files:")
  print(removed_files)

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
        return modified_files, removed_files
    except requests.exceptions.RequestException as e: 
        raise SystemExit(e)  

if __name__ == '__main__':

  if len(sys.argv) != 2:
    raise SystemExit('No PR passed.')
  main(sys.argv[1])