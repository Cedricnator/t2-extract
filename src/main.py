from extract_data import GithubExtractor

def main():
   github_extractor = GithubExtractor()
   github_extractor.make_request("nodejs", "node")
   
   
if __name__ == "__main__":
   main()