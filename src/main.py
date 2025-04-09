import os
import requests
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TOKEN")

def make_request(owner: str, repo: str):
   try:   
      req = requests.get(f"https://api.github.com/repos/{owner}/{repo}", headers={"Authorization": f"Bearer {token}"})  
      if req.status_code == 200:
         owner = req.json()["owner"]["login"]
         print(f"{owner} is the owner of the repository {repo}")
         return owner
      else:
         print(f"Request failed with status code: {req.status_code}")
   except requests.exceptions.RequestException as e:
      print(f"An error occurred: {e}")

def get_user_info(owner: str):
   try:   
      req = requests.get(f"https://api.github.com/users/{owner}/repos", headers={"Authorization": f"Bearer {token}"})  
      if req.status_code == 200:
            resp = req.json()
            for repo in resp:
               print(f"Repository Name: {repo['name']}")
               print(f"Repository URL: {repo['html_url']}")
               print(f"Repository Description: {repo['description']}")
               print(f"Repository Language: {repo['language']}")
               print(f"Repository Stars: {repo['stargazers_count']}")
               print(f"Repository Forks: {repo['forks_count']}")
               print("-" * 40)
      else:
         print(f"Request failed with status code: {req.status_code}")
   except requests.exceptions.RequestException as e:
      print(f"An error occurred: {e}")

def extract_repository_from_user(owner: str, repo: str):
   print(f"Extracting repository {repo} from user {owner}", )

def main():
   get_user_info("cedricnator")

   
if __name__ == "__main__":
   main()