from logger import Logger
import os
import csv

class CsvOutput:
   def __init__(self, file_name: str, file_path: str):
      self.file_path = file_path
      self.filename =  file_name
      self.logger  = Logger()
   
   def save_repositories_to_csv(self, repositories):
      """
      Guarda datos de repositorios en un archivo CSV.
      
      Args:
         repositories (list): Lista de datos de repositorios
         filename (str): Nombre del archivo de salida
      """
      try:         
         os.makedirs(os.path.dirname(self.filename) if os.path.dirname(self.filename) else self.file_path, exist_ok=True)
         
         with open(self.filename, 'w', newline='', encoding='utf-8') as csvfile:
            if not repositories:
               self.logger.log_warning("No hay repositorios para guardar")
               return
                  
            # Obtener encabezados del primer repositorio
            fieldnames = repositories[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for repo in repositories:
               writer.writerow(repo)
                  
         self.logger.log(f"Guardados {len(repositories)} repositorios en {self.filename}")
      except Exception as e:
         self.logger.log_error(f"Error guardando en CSV: {e}")