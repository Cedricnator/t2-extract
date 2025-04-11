from app.extract_data import GithubExtractor
from app.csv_output import CsvOutput
from app.constants import LANGUAGES, YEARS, STARS
from app.logger import Logger
import time

def main():
   logger = Logger()
   github_extractor = GithubExtractor()
   csv_output = CsvOutput(file_name="repositories.csv", file_path="../data/")
   all_repositories = [] 
   
   # Para evitar duplicados
   seen_repos = set() 
   
   for lang in LANGUAGES:
      for starts in STARS:
         query = f"language:{lang} stars:{starts}"
         repositories = github_extractor.search_repositories(
            query=query,
            sort="starts",
            order="desc",
            max_results=1000,
         )
         
         if repositories:
            for repo in repositories:
               # Evitar duplicados
               if repo['name'] not in seen_repos:
                  seen_repos.add(repo['name'])
                  all_repositories.append(repo)
      
      time.sleep(2)
         
      if len(all_repositories) >= 20000:
         break
   
   for year in YEARS:
      if len(all_repositories) >= 20000:
         break
         
      query = f"created:{year} stars:>10"
      print(f"\nBuscando por año: {query}")
      
      repos = github_extractor.search_repositories(
         query=query,
         sort="stars",
         order="desc",
         max_results=1000
      )
      
      for repo in repos:
         repo_id = repo["id"]
         if repo_id not in seen_repos:
            all_repositories.append(repo)
            seen_repos.add(repo_id)
      
      logger.log(f"Total acumulado: {len(all_repositories)}")
      time.sleep(2)
               
   csv_output.save_repositories_to_csv(all_repositories)
   logger.log(f"Total de repositorios guardados: {len(all_repositories)}")

   
if __name__ == "__main__":
   main()