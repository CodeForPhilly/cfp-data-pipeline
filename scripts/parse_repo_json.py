import re

import requests
import yaml

PROJECTS_URL = "https://brigade.cloud/static-api/v1/organizations/Code%20for%20Philly/projects.json"


def main():
    """Read the list of projects from the PROJECTS_URL, and write out the list of repositories, excluding anything
    on the exclude list."""

    proj_response = requests.get(PROJECTS_URL)
    if proj_response.status_code != 200:
        print("Error reading projects: ", proj_response)
        return

    github_list = []
    projects = proj_response.json()
    for project in projects["data"]:
        proj_link = requests.utils.requote_uri(
            "https://brigade.cloud/static-api/v1" + project["links"]["self"]
        )
        try:
            proj_data = requests.get(proj_link).json()
            code_url = proj_data["data"]["attributes"].get("code_url", "")
            if not code_url.startswith("https://github.com/"):
                print("Skipping ", proj_data["data"]["id"], code_url)
            else:
                print(code_url)
                code_url = code_url.replace("https://github.com/", "")
                github_list.append(code_url)

        except Exception as ex:
            print(ex)
            return

    github_urls = " ".join(github_list)
    # now load the meltano.yml file
    meltano_filename = "../meltano/cfp-pipeline/meltano.yml"
    with open(meltano_filename) as f:
        doc = yaml.safe_load(f)

    github_extractor = None
    for e in doc["plugins"]["extractors"]:
        if e["name"] == "tap-github":
            github_extractor = e
            break
    if github_extractor is None:
        print("could not find tap-github in meltano.yml file")
        return

    if github_urls != github_extractor["config"]["repository"]:
        print("tap-github repositories is different, rewriting meltano.yml")
        github_extractor["config"]["repository"] = github_urls
        with open(meltano_filename, "r") as f:
            meltano_yaml = f.read()
        meltano_yaml = re.sub(
            "repository:(.*)\n?", "repository: " + github_urls + "\n", meltano_yaml
        )
        with open(meltano_filename, "w") as f:
            f.write(meltano_yaml)


if __name__ == "__main__":
    main()
