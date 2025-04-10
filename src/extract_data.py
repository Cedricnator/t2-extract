
import requests
from constants import GITHUB_TOKEN

class GithubExtractor:
   def __init__(self):
      self.github_token = GITHUB_TOKEN

   def make_request(self, owner: str, repo: str):
      try:   
         req = requests.get(f"https://api.github.com/repos/{owner}/{repo}", headers={"Authorization": f"Bearer {self.github_token}"})  
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

   def extract_users_from_stars(self, owner: str, repo: str):
      try:
         print(f"Getting users who starred {owner}/{repo}")
      except requests.exceptions.RequestException as e:
         print(f"An error occurred: {e}")

   def get_repositories_from_user(self, owner: str):
      try:   
         req = requests.get(f"https://api.github.com/users/{owner}/repos", headers={"Authorization": f"Bearer {self.GITHUB_TOKEN}"})  
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

   def extract_repository_from_user(self, owner: str, repo: str):
      try:   
         req = requests.get(f"https://api.github.com/repos/{owner}/{repo}", headers={"Authorization": f"Bearer {self.GITHUB_TOKEN}"})  
         if req.status_code == 200:
            resp = req.json()
            print(resp)
         else:
            print(f"Request failed with status code: {req.status_code}")
      except requests.exceptions.RequestException as e:
         print(f"An error occurred: {e}")