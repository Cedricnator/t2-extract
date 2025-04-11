from constants import GITHUB_TOKEN
from logger import Logger
from datetime import datetime
import requests
import time

class GithubExtractor:
   def __init__(self):
      self.github_token = GITHUB_TOKEN
      self.logger = Logger()
      self.logger.log("GithubExtractor initialized")
      
   def _check_rate_limit(self, headers):
      """Verifica si estamos cerca del límite de tasa y espera si es necesario"""
      if "X-RateLimit-Remaining" in headers and int(headers["X-RateLimit-Remaining"]) < 5:
         self.logger.log_warning("Cerca del límite de tasa, esperando...")
         import time
         time.sleep(30)  # Esperar 30 segundos

   def _handle_rate_limit_exceeded(self, headers):
      """Maneja el caso donde se ha excedido el límite de tasa"""
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
         
   def make_request(self, owner: str, repo: str):
      try:   
         req = requests.get(f"https://api.github.com/repos/{owner}/{repo}", headers={"Authorization": f"Bearer {self.github_token}"})  
         if req.status_code == 200:
            resp = req.json()
            self.logger.log(f"Repository {owner}/{repo} found")
            self.logger.log(f"Repository URL: {resp['html_url']}")
            self.logger.log(f"Repository Description: {resp['description']}")
            self.logger.log(f"Repository Language: {resp['language']}")
            self.logger.log(f"Repository Stars: {resp['stargazers_count']}")
            self.logger.log(f"Repository Forks: {resp['forks_count']}")
            self.logger.log(f"Repository Open Issues: {resp['open_issues_count']}")
            self.logger.log(f"Repository {owner}/{repo} found")           
            self.logger.log(f"Repository Owner: {resp['owner']['login']}") 
            return resp
         else:
            self.logger.log_error(f"Request failed with status code: {req.status_code}")
      except requests.exceptions.RequestException as e:
         self.logger.log_error(f"Error occurred: {e}")

   def get_stargazers(self, owner: str, repo: str, max_pages=5):
      """Get users who have starred a repository"""
      try:
         url = f"https://api.github.com/repos/{owner}/{repo}/stargazers"
         headers = {
            "Authorization": f"Bearer {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
         }
         
         users = []
         page = 1
         per_page = 100
         
         self.logger.log(f"Fetching stargazers for {owner}/{repo}...")

         while page <= max_pages:  # Only fetch up to 5 pages
            self.logger.log(f"Fetching page {page} of stargazers...")
            req = requests.get(
                  f"{url}?page={page}&per_page={per_page}", 
                  headers=headers
            )

            if req.status_code == 200:
               response_data = req.json()
               # Empty page means we've got all users
               if not response_data:  
                  break

               for user in response_data:
                  users.append({
                     "login": user["login"],
                     "id": user["id"],
                     "url": user["html_url"]
                  })
        
               page += 1
            else:
               self.logger.log_error(f"Request failed with status code: {req.status_code}")
               break
                  
         self.logger.log(f"Found {len(users)} users who starred {owner}/{repo}")
         return users
      except requests.exceptions.RequestException as e:
         self.logger.log_error(f"Error occurred: {e}")
         return []

   def get_repositories_from_user(self, owner: str):
      try: 
         self.logger.log(f"Fetching repositories for user {owner}...")  
         req = requests.get(f"https://api.github.com/users/{owner}/repos", headers={"Authorization": f"Bearer {self.github_token}"})  
         if req.status_code == 200:
               repositories = []
               resp = req.json()
               for repo in resp:
                  repositories.append(repo['name'])
               self.logger.log(f"Found {len(repositories)} repositories for user {owner}")
               return repositories
                  
         else:            
            self.logger.log_error(f"Request failed with status code: {req.status_code}")
      except requests.exceptions.RequestException as e:
         self.logger.log_error(f"Error occurred: {e}")

   def extract_repository_from_user(self, owner: str, repo: str):
      try:   
         req = requests.get(f"https://api.github.com/repos/{owner}/{repo}", headers={"Authorization": f"Bearer {self.github_token}"})  
         if req.status_code == 200:
            resp = req.json()
            self.logger.log(f"{resp}]")
         else:
            self.logger.log_error(f"Request failed with status code: {req.status_code}")
      except requests.exceptions.RequestException as e:
         self.logger.log_error(f"Error occurred: {e}")
         
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
                     "watchers": repo["watchers"]
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
         
   def analyze_creation_years(self, repositories):
      """
      Analiza en qué años se crearon más repositorios.
      
      Args:
         repositories (list): Lista de datos de repositorios
         
      Returns:
         dict: Conteo de repositorios por año
      """
      try:         
         year_counts = {}
         
         for repo in repositories:
            created_at = repo.get("created_at")
            if created_at:
                  year = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ").year
                  year_counts[year] = year_counts.get(year, 0) + 1
         
         # Ordenar por año
         sorted_years = dict(sorted(year_counts.items()))
         self.logger.log(f"Distribución de repositorios por año de creación: {sorted_years}")
         return sorted_years
      except Exception as e:
         self.logger.log_error(f"Error analizando años de creación: {e}")
         return {}
      
   def get_stars_evolution(self, owner, repo, time_points=5):
      """
      Obtiene la evolución de estrellas de un repositorio a lo largo del tiempo.
      Utiliza el método get_stargazers existente y lo procesa para obtener la evolución.
      
      Args:
         owner (str): Propietario del repositorio
         repo (str): Nombre del repositorio
         time_points (int): Número de puntos de tiempo para analizar
         
      Returns:
         list: Conteo de estrellas en diferentes momentos
      """
      try:
         # Primero obtenemos la información del repositorio
         repo_info = self.make_request(owner, repo)
         if not repo_info:
            return []
            
         # Obtenemos las estrellas con el método existente
         stars = self.get_stargazers(owner, repo, max_pages=20)
         
         if not stars:
            return []
            
         # Parsear fechas de creación y actualización
         created_at = datetime.strptime(repo_info["created_at"], "%Y-%m-%dT%H:%M:%SZ")
         updated_at = datetime.strptime(repo_info["updated_at"], "%Y-%m-%dT%H:%M:%SZ")
         
         # Calcular intervalos de tiempo
         time_range = (updated_at - created_at).total_seconds()
         interval = time_range / (time_points - 1) if time_points > 1 else time_range
         
         # Crear puntos de tiempo
         evolution = []
         stars_count = repo_info["stargazers_count"]
         
         # Al no tener fechas exactas de cada estrella en el método original,
         # hacemos una estimación lineal
         for i in range(time_points):
            point_time = created_at.timestamp() + (interval * i)
            point_date = datetime.fromtimestamp(point_time).strftime("%Y-%m-%d")
            
            # Estimación simple: asumimos crecimiento lineal de estrellas
            estimated_stars = int((i / (time_points - 1)) * stars_count) if time_points > 1 else stars_count
            
            evolution.append({
               "date": point_date,
               "stars": estimated_stars
            })
         
         self.logger.log(f"Evolución de estrellas para {owner}/{repo}: {evolution}")
         return evolution
         
      except Exception as e:
         self.logger.log_error(f"Error obteniendo evolución de estrellas: {e}")
         return []
      
         
   def analyze_open_issues(self, repositories):
      """
      Analiza la distribución de problemas abiertos entre repositorios.
      
      Args:
         repositories (list): Lista de datos de repositorios
         
      Returns:
         dict: Estadísticas de problemas abiertos
      """
      try:
         total_repos = len(repositories)
         if total_repos == 0:
            return {"error": "No hay repositorios para analizar"}
            
         issues_counts = [repo.get("open_issues_count", 0) for repo in repositories if "open_issues_count" in repo]
         
         if not issues_counts:
            return {"error": "No hay datos de problemas abiertos disponibles"}
            
         # Calcular estadísticas básicas
         total_issues = sum(issues_counts)
         avg_issues = total_issues / total_repos
         max_issues = max(issues_counts)
         min_issues = min(issues_counts)
         
         # Distribuir por rangos
         ranges = {
            "0": 0,
            "1-10": 0,
            "11-50": 0,
            "51-100": 0,
            "101-500": 0,
            "501+": 0
         }
         
         for count in issues_counts:
            if count == 0:
                  ranges["0"] += 1
            elif count <= 10:
                  ranges["1-10"] += 1
            elif count <= 50:
                  ranges["11-50"] += 1
            elif count <= 100:
                  ranges["51-100"] += 1
            elif count <= 500:
                  ranges["101-500"] += 1
            else:
                  ranges["501+"] += 1
         
         # Convertir a porcentajes
         for key in ranges:
            ranges[key] = (ranges[key] / total_repos) * 100
            
         stats = {
            "total_issues": total_issues,
            "avg_issues_per_repo": avg_issues,
            "max_issues": max_issues,
            "min_issues": min_issues,
            "distribution_percentages": ranges
         }
         
         self.logger.log(f"Análisis de problemas abiertos: {stats}")
         return stats
         
      except Exception as e:
         self.logger.log_error(f"Error analizando problemas abiertos: {e}")
         return {"error": str(e)}
            
