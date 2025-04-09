import os
import requests
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TOKEN")

def make_request(owner: str, repo: str):
   req = requests.get(f"https://api.github.com/repos/{owner}/{repo}", headers={"Authorization": f"Bearer {token}"})  
   if req.status_code == 200:
       print("Request successful!")
       print(req.json())
   else:
       print(f"Request failed with status code: {req.status_code}")

def main():
   make_request("Cucharoth", "t2_eda")

   
if __name__ == "__main__":
   main()