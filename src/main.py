import os
import requests
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TOKEN")

def make_request(owner: str, repo: str):
   try:   
      req = requests.get(f"https://api.github.com/repos/{owner}/{repo}", headers={"Authorization": f"Bearer {token}"})  
      if req.status_code == 200:
         resp = req.json()
         print(f"Repository Name: {resp['name']}")
         print(f"Repository URL: {resp['html_url']}")
         print(f"Repository Description: {resp['description']}")
         print(f"Repository Language: {resp['language']}")
         print(f"Repository Stars: {resp['stargazers_count']}")
         print(f"Repository Forks: {resp['forks_count']}")
      else:
         print(f"Request failed with status code: {req.status_code}")
   except requests.exceptions.RequestException as e:
      print(f"An error occurred: {e}")

def get_repositories_from_user(owner: str):
   try:   
      req = requests.get(f"https://api.github.com/users/{owner}/repos", headers={"Authorization": f"Bearer {token}"})  
      if req.status_code == 200:
            repositories = []
            resp = req.json()
            for repo in resp:
               repositories.append(repo['name'])
            return repositories
               
      else:
         print(f"Request failed with status code: {req.status_code}")
   except requests.exceptions.RequestException as e:
      print(f"An error occurred: {e}")

def extract_repository_from_user(owner: str, repo: str):
   try:   
      req = requests.get(f"https://api.github.com/repos/{owner}/{repo}", headers={"Authorization": f"Bearer {token}"})  
      if req.status_code == 200:
         resp = req.json()
         print(resp)
      else:
         print(f"Request failed with status code: {req.status_code}")
   except requests.exceptions.RequestException as e:
      print(f"An error occurred: {e}")

def main():
   repositorys = get_repositories_from_user("cedricnator")
   if repositorys:
      print("List of repositories:")
      for repo in repositorys:
         make_request("cedricnator", repo)
   

   
if __name__ == "__main__":
   main()