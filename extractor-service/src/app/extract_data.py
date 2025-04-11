from app.constants import GITHUB_TOKEN
from app.logger import Logger
import requests
import time

class GithubExtractor:
   def __init__(self):
      self.github_token = GITHUB_TOKEN
      self.logger = Logger()
      self.logger.log("GithubExtractor initialized")
      
   def _check_rate_limit(self, headers):
      """
         Verifica si estamos cerca del límite de tasa y espera si es necesario
         
         Args:
            headers (dict): Encabezados de la respuesta de la API
         
         Returns:
            None
      """
      if "X-RateLimit-Remaining" in headers and int(headers["X-RateLimit-Remaining"]) < 5:
         self.logger.log_warning("Cerca del límite de tasa, esperando...")
         import time
         time.sleep(30)  

   def _handle_rate_limit_exceeded(self, headers):
      """
         Maneja el caso donde se ha excedido el límite de tasa

         Args:
            headers (dict): Encabezados de la respuesta de la API
            
         Returns:
            None
      """
      if "X-RateLimit-Reset" in headers:
         reset_time = int(headers["X-RateLimit-Reset"])
         current_time = time.time()
         wait_time = max(reset_time - current_time, 0) + 10  # 10 segundos extra
         self.logger.log_warning(f"Límite excedido. Esperando {wait_time:.0f} segundos...")
         time.sleep(wait_time)
      else:
         # Si no hay información de reset, esperar un minuto por defecto
         self.logger.log_warning("Límite excedido. Esperando 60 segundos...")
         time.sleep(60)
         
   def extract_commit_count(self, owner: str, repo_name: str):
      try:
         url = f"https://api.github.com/repos/{owner}/{repo_name}/commits"
         headers = { "Authorization": f"Bearer {self.github_token}" }
         
         req = requests.head(f"{url}?per_page=1", headers=headers)
         
         if req.status_code == 200 and 'Link' in req.headers:
            # Extraer el número total de commits del encabezado Link
            link = req.headers['Link']
            if 'rel="last"' in link:
               last_page = int(link.split('page=')[1].split('&')[0].split('>')[0])
               return last_page  
            
         req = requests.get(f"{url}?per_page=1", headers=headers)
         if req.status_code == 200:
               return req.json()[0]['commit']['committer']['date']
         
         return -1
      except Exception as e:
         self.logger.log_error(f"Error occurred: {e}")
         return -1 
         
   def search_repositories(self, query="stars:>1000", sort="stars", order="desc", max_results=10000):
      """
      Busca repositorios en GitHub según criterios y retorna información básica.
      
      Args:
         query (str): Consulta de búsqueda (ej: "stars:>1000 language:python")
         sort (str): Campo para ordenar (stars, forks, updated)
         order (str): Orden (asc, desc)
         max_results (int): Máximo de resultados
         
      Returns:
         list: Datos de repositorios encontrados
      """
      try:
         repositories = []
         page = 1
         per_page = 100 
         max_pages = (max_results + per_page - 1) // per_page
         
         self.logger.log(f"Buscando repositorios con query: {query}")
         
         while len(repositories) < max_results and page <= max_pages:
            self.logger.log(f"Obteniendo página {page} de resultados...")
            url = f"https://api.github.com/search/repositories?q={query}&sort={sort}&order={order}&page={page}&per_page={per_page}"
            
            headers = {
               "Authorization": f"Bearer {self.github_token}",
               "Accept": "application/vnd.github.v3+json"
            }
            
            req = requests.get(url, headers=headers)
            
            if req.status_code == 200:
               response_data = req.json()
               items = response_data.get("items", [])
               
               if not items:
                  break  # No hay más resultados
               
               for repo in items:
                  owner = repo["owner"]["login"]
                  repo_name = repo["name"]
                  
                  commit_count = self.extract_commit_count(owner, repo_name)
                  
                  repositories.append({
                     "id": repo["id"],
                     "name": repo["name"],
                     "full_name": repo["full_name"],
                     "owner": repo["owner"]["login"],
                     "html_url": repo["html_url"],
                     "description": repo["description"],
                     "created_at": repo["created_at"],
                     "updated_at": repo["updated_at"],
                     "language": repo["language"],
                     "stargazers_count": repo["stargazers_count"],
                     "forks_count": repo["forks_count"],
                     "open_issues_count": repo["open_issues_count"],
                     "watchers": repo["watchers"],
                     "commit_count": commit_count,
                  })
               
               page += 1
               
               # Control de límite de tasa de GitHub
               self._check_rate_limit(req.headers)
            else:
               self.logger.log_error(f"Solicitud falló con código: {req.status_code}")
               if req.status_code == 403 and "X-RateLimit-Remaining" in req.headers:
                  self._handle_rate_limit_exceeded(req.headers)
                  continue
               break
               
         self.logger.log(f"Encontrados {len(repositories)} repositorios que coinciden con los criterios")
         return repositories[:max_results]
      
      except requests.exceptions.RequestException as e:
         self.logger.log_error(f"Error durante la búsqueda de repositorios: {e}")
         return []
