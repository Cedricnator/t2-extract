from abc import ABC, abstractmethod

# Originator Class
class Repository:
   def __init__(self):
      self._id = 0
      self._created_at = ''
      self._description = ''
      self._fork_count = 0
      self._full_name = ''
      self._html_url = ''
      self._language = ''
      self._name = ''
      self._open_issues_count = 0
      self._owner = ''
      self._stars_count = 0
      self._updated_at = ''
      self._watchers = ''

   @property
   def id(self):
      return self._id
   
   @id.setter
   def id(self, value):
      self._id = value
      
   @property
   def created_at(self):
      return self._created_at
   
   @created_at.setter
   def created_at(self, value):
      self._created_at = value
      
   @property
   def description(self):
      return self._description

   @description.setter
   def description(self, value):
      self._description = value
      
   @property
   def fork_count(self):
      return self._fork_count
   
   @fork_count.setter
   def fork_count(self, value):
      self._fork_count = value
      
   @property
   def full_name(self):
      return self._full_name
   
   @full_name.setter
   def full_name(self, value):
      self._full_name = value
   
   @property
   def html_url(self):
      return self._html_url
   
   @html_url.setter
   def html_url(self, value):
      self._html_url = value
      
   @property
   def language(self):
      return self._language
   
   @language.setter
   def language(self, value):
      self._language = value
      
   @property
   def name(self):
      return self._name
   
   @name.setter
   def name(self, value):
      self._name = value
      
   @property
   def open_issues_count(self):
      return self._open_issues_count
   
   @open_issues_count.setter
   def open_issues_count(self, value):
      self._open_issues_count = value
      
   @property
   def owner(self):
      return self._owner
   
   @owner.setter
   def owner(self, value):
      self._owner = value
      
   @property
   def stars_count(self):
      return self._stars_count
   
   @stars_count.setter
   def stars_count(self, value):
      self._stars_count = value
      
   @property
   def updated_at(self):
      return self._updated_at
   
   @updated_at.setter
   def updated_at(self, value):
      self._updated_at = value
      
   @property
   def watchers(self):
      return self._watchers
   
   @watchers.setter
   def watchers(self, value):
      self._watchers = value
      
   def to_dict(self):
      return {
         "id": self._id,
         "name": self._name,
         "full_name": self._full_name,
         "owner": self._owner,
         "html_url": self._html_url,
         "description": self._description,
         "created_at": self._created_at,
         "updated_at": self._updated_at,
         "language": self._language,
         "stargazers_count": self._stars_count,
         "forks_count": self._fork_count,
         "open_issues_count": self._open_issues_count,
         "watchers": self._watchers
      }

# Abstract Builder
class AbstractBuilder(ABC):
   @abstractmethod
   def set_id(id: int):
      pass
   
   @abstractmethod
   def set_name(name: str):
      pass

   @abstractmethod
   def set_full_name(full_name: str):
      pass
   
   @abstractmethod
   def set_owner(owner: str):
      pass
   
   @abstractmethod
   def set_html_url(html_url: str):
      pass
   
   @abstractmethod
   def set_description(description: str):
      pass
   
   @abstractmethod
   def set_created_at(created_at: str):
      pass
   
   @abstractmethod
   def set_language(language: str):
      pass
   
   @abstractmethod
   def set_updated_at(updated_at: str):
      pass
   
   @abstractmethod
   def set_fork_count(fork_count: int):
      pass
   
   @abstractmethod
   def set_stars_count(starts_count: int):
      pass
   
   @abstractmethod
   def set_watchers(watchers: int):
      pass
   
   @abstractmethod
   def set_open_issues_count(issues_count: int):
      pass
   
   @abstractmethod
   def build(self):
      pass

# Concrete Builder
class RepositoryBuilder(AbstractBuilder):
   def __init__(self):
      self.repository = Repository()
   
   def set_id(self, id: int):
      self.repository.id = id
      return self
   
   def set_name(self, name: str):
      self.repository.name = name
      return self
   
   def set_full_name(self, full_name: str):
      self.repository.full_name = full_name
      return self
   
   def set_owner(self, owner: str):
      self.repository.owner = owner
      return self
   
   def set_html_url(self, html_url: str):
      self.repository.html_url = html_url
      return self
   
   def set_description(self, description: str):
      self.repository.description = description
      return self
   
   def set_created_at(self, created_at: str):
      self.repository.created_at = created_at
      return self
   
   def set_language(self, language: str):
      self.repository.language = language
      return self
   
   def set_updated_at(self, updated_at: str):
      self.repository.updated_at = updated_at
      return self
   
   def set_fork_count(self, fork_count: int):
      self.repository.fork_count = fork_count
      return self
   
   def set_stars_count(self, stars_count: int):
      self.repository.stars_count = stars_count
      return self
   
   def set_watchers(self, watchers: int):
      self.repository.watchers = watchers
      return self
   
   def set_open_issues_count(self, issues_count: int):
      self.repository.open_issues_count = issues_count
      return self
   
   def build(self):
      return self.repository