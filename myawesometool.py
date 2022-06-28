
import sys
import base64
import json
import re
import random
import os
from github import Github  
import pandas as pd


csv_path = str(sys.argv[1])
csv_file = pd.read_csv(csv_path)

#parse user and repo name from url using regex
def getElement(url):
    pos = re.findall(r"\/[a-zA-z-]+", url)
    return pos[1][1:], pos[2][1:]

#compare versions to check validity 
def compareVersion(v1, v2):
    if(v1 == None):
        return None
    arr1 = v1.split(".")
    arr2 = v2.split(".")
    n = len(arr1)
    m = len(arr2)
     
    arr1 = [int(i) for i in arr1]
    arr2 = [int(i) for i in arr2]
  
    if n>m:
      for i in range(m, n):
         arr2.append(0)
    elif m>n:
      for i in range(n, m):
         arr1.append(0)
     
    for i in range(len(arr1)):
      if arr1[i]>arr2[i]:
         return True
      elif arr2[i]>arr1[i]:
         return False
    return True

#function to delete temporary files
def removeFiles():
    if os.path.exists("package.json"):
        os.remove("package.json")
    if os.path.exists("package-lock.json"):
        os.remove("package-lock.json")


repo_name = []
for repos in csv_file["repo"]:
    user, repo_temp = getElement(repos) 
    repo_name.append(repo_temp)

input_dep_version = str(sys.argv[2]).split('@')
dependency = input_dep_version[0]
given_version = input_dep_version[1]
update = False
if len(sys.argv) > 3 and sys.argv[3] == "update":
    update = True
vers = []
prs = []

#store access token to github account in access.json
acc_file = open("access-tokens.json", 'r')
acc_tok = json.load(acc_file)
acc_file.close()
for i in repo_name:
    try:
        g = Github(acc_tok['token'])
        repo = g.get_user().get_repo(i)
        repo.get_branch(branch="master")
        contents = repo.get_contents("package.json")
        lock_contents = repo.get_contents("package-lock.json")
        content = base64.b64decode(contents.content)
        json_res = json.loads(content)
        if dependency in json_res['dependencies']:
            vers.append(json_res['dependencies'][dependency][1:])
            if not compareVersion(json_res['dependencies'][dependency][1:], given_version) and update:
                json_res['dependencies'][dependency] = json_res['dependencies'][dependency][0]+given_version
                out_file = open("package.json", "w")
                json.dump(json_res, out_file, indent = 6)
                out_file.close() 
                os.system('npm i --package-lock-only')
                read_file = open("package.json", "r")
                read_file_lock = open("package-lock.json", "r")
                sb = repo.get_branch('master')

                #generating new branch using random numbers
                new_branch = "dev-branch"+str(random.randint(1, 1000)) 

                #creating branch
                repo.create_git_ref(ref='refs/heads/' + new_branch, sha=sb.commit.sha) 
                
                #updating files
                repo.update_file(contents.path, "package.json", read_file.read(), contents.sha, branch=new_branch)
                repo.update_file(lock_contents.path, "package-lock.json", read_file_lock.read(), lock_contents.sha, branch=new_branch)

                #raise PR
                pr = repo.create_pull(title="updated dependencies", body="updated dependencies", head=new_branch, base="master")
                prs.append(pr)

                #remove temporary files
                read_file.close()
                read_file_lock.close()
                removeFiles()

            else:
                prs.append(None)
                
        else:
            vers.append(None)
            prs.append(None)
            
    except:
        vers.append(None)
        prs.append(None)
        print(sys.exc_info()[0])
        read_file.close()
        read_file_lock.close()
        removeFiles()
    
    

#printing results
for j in range(0, len(csv_file)):
    print("name:",repo_name[j])
    print("repo:", csv_file['repo'][j])
    print("version:", vers[j])
    print("version_satisfied:", compareVersion(vers[j], given_version))    
    if update and not compareVersion(vers[j], given_version):
        print("update_pr:", prs[j])
    print()

