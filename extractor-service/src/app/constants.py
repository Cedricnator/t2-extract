import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("TOKEN")
LANGUAGES = ["javascript", "python", "java", "rust", "go",  "swift"]
STARS = ["5..100", "100..500", "500..1000", "1000..5000", ">5000"]
YEARS = ["2000..2010", "2011..2020", "2021..2025"]