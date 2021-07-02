import requests
import json


def get_list_repos(username):

    url = f"https://api.github.com/users/{username}/repos"
    user_repo = requests.get(url).json()

    number_list = []
    repos_list = []
    for repo in range(0, len(user_repo)):
        number_list.append(repo + 1)
        repos_list.append(user_repo[repo]['name'])

    repos_dictionary = dict(zip(number_list, repos_list))

    with open("repo_list.json", "w") as write_f:
        json.dump(repos_dictionary, write_f)


get_list_repos('OlegFedotkin')
