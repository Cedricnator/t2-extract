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
         print(f"{req.json()}")
      else:
         print(f"Request failed with status code: {req.status_code}")
   except requests.exceptions.RequestException as e:
      print(f"An error occurred: {e}")

def extract_repository_from_user(owner: str, repo: str):
   print(f"Extracting repository {repo} from user {owner}", )

def main():
   owner = make_request("Cucharoth", "t2_eda")
   get_user_info(owner)

   
if __name__ == "__main__":
   main()