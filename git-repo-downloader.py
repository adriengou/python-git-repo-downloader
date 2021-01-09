import requests

def get_files_list(owner, repo):
    r = requests.get(f"https://api.github.com/repos/{owner}/{repo}/contents")
    return r.text

print(get_files_list())
