import requests
import json
import os
import errno
import argparse
import sys

def get_files_paths(owner, repo):
    r = requests.get(f"https://api.github.com/repos/{owner}/{repo}/contents")
    data = json.loads(r.text)
    paths = []
    for file in data:
        paths.append(file['path'])

    return paths

def get_file_commit(owner, repo, path):
    commits = []
    
    r = requests.get(f"https://api.github.com/repos/{owner}/{repo}/commits?path={path}")
    commits = json.loads(r.text)
    return commits[0]['sha']

def get_raw_file(owner, repo, commit, path):
    r = requests.get(f"https://raw.githubusercontent.com/{owner}/{repo}/{commit}/{path}")
    return r.text

def download_repo(owner, repo, download_path):
    
    files_paths = get_files_paths(owner, repo)

    files_info = []

    for path in files_paths:
        commit = get_file_commit(owner, repo, path)
        info = {
            'path': path,
            'commit':commit
        }

        files_info.append(info)

    for info in files_info:
        raw = get_raw_file(owner, repo, info['commit'], info['path'])
        path = f"{download_path}/{repo}/{info['path']}"

        if not os.path.exists(os.path.dirname(path)):
            try:
                os.makedirs(os.path.dirname(path))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        with open(path, 'w') as file:
            file.write(raw)

    print("files downloaded")



# Create the parser
my_parser = argparse.ArgumentParser(description='Download a Github repo\ngit-rd [owner] [repo] [path]')

# Add the arguments
my_parser.add_argument('Owner',
                       metavar='owner',
                       type=str,
                       help='the owner of the Github repo')

my_parser.add_argument('Repo',
                       metavar='repo',
                       type=str,
                       help='the Github repo')

my_parser.add_argument("--path", nargs="?", default="./")

# Execute the parse_args() method
args = my_parser.parse_args()

download_repo(args.Owner, args.Repo, args.path)