import sys
import subprocess
import os
from github import Github
from pathlib import Path
from github import GithubException
from fuzzywuzzy import process

# Keywords to detect secrets (very basic check)
#SECRET_KEYWORDS = ['token', 'secret', 'key', 'password']

#def contains_secret(content: bytes) -> bool:
    #content_str = content.decode(errors='ignore').lower()
    #return any(keyword in content_str for keyword in SECRET_KEYWORDS)


# Initialize github
def init_github():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("GitHub token not found in environment variables.")
    return Github(token)


# Helper function to exclude folders/files similar to .gitignore behavior
EXCLUDE = ['.git', '__pycache__', '.DS_Store', '.vscode', '.conda', 'node_modules']

def should_exclude(path: Path) -> bool:
    return any(exclude in str(path) for exclude in EXCLUDE)


def display_all_repos():
    try:
        g = init_github()
        repos = list(g.get_user().get_repos())
        #for repo in repos:
            #print(f"Repo Name: {repo.name}")
            #print(f"Description: {repo.description or 'No description available'}")
            #print(f"URL: {repo.html_url}\n")
        return [
            {
                "name": repo.name,
                "description": repo.description or "No description available",
                "url": repo.html_url
            }
            for repo in repos
        ]

    except Exception as e:
        return{"error: strr {e}"}


def access_repo_contents(repo_name: str):
    try:
        g = init_github()  # Initialize the GitHub client
        all_repos = [repo.full_name for repo in g.get_user().get_repos()]  # Fetch all repo names
        
        # Match the user's input with the closest repo name
        matched_repo = process.extractOne(repo_name, all_repos)
        
        if matched_repo and matched_repo[1] > 70:  # If match is above the threshold (e.g., 70%)
            repo = g.get_repo(matched_repo[0])  # Get the matched repo by its full name
            
            # Get the content at the root of the repository
            contents = repo.get_contents("")  # Empty string to get the root directory

            return [content.path for content in contents]
        else:
            return{"error": "Repository not found or couldn't match the name well enough."}
    except Exception as e:
        return{"error: str{e}"}



def delete_repository(repo_name: str):
    try:
        g = init_github()
        all_repos = [repo.full_name for repo in g.get_user().get_repos()]  # Fetch all repo names
        
        # Match the user's input with the closest repo name
        matched_repo = process.extractOne(repo_name, all_repos)
        
        if matched_repo and matched_repo[1] > 70:  # If match is above the threshold (e.g., 70%)
            repo = g.get_repo(matched_repo[0])  # Get the matched repo by its full name
            repo.delete()  # Delete the repository
            print(f"Repository '{matched_repo[0]}' deleted successfully.")
        else:
            print("Repository not found or couldn't match the name well enough.")
    except Exception as e:
        print(f"Error: {e}")


def upload_project(repo_name: str, description: str, folder_path: str):
    upload_log=[]

    try:
        # 1. Check if folder exists
        project_dir = Path(folder_path.strip().replace("\\", "/")).resolve()
        if not project_dir.exists() or not project_dir.is_dir():
            return {"error": f"Folder path '{folder_path}' does not exist or is not a directory."}

            

        # 2. Init GitHub and create repo
        g = init_github()
        user = g.get_user()

        try:
            new_repo = user.create_repo(repo_name, description=description)
        except GithubException as ge:
            if ge.status == 422 and "name already exists" in str(ge.data):
                return {"error": f"A repository named '{repo_name}' already exists."}
            return {"error": ge.data.get("message", "Unknown error")}

        # 3. Walk through files in the folder
        for file_path in project_dir.rglob("*"):
            if should_exclude(file_path):
                continue

            if file_path.is_file():
                relative_path = str(file_path.relative_to(project_dir))

                with open(file_path, "rb") as f:
                    content = f.read()

                # 4. Skip files with secrets
                #if contains_secret(content):
                    #print(f"⚠️ Skipped '{relative_path}': Possible secret detected.")
                    #continue

                # 5. Check if file already exists in the repo
                try:
                    new_repo.get_contents(relative_path)
                    upload_log.append(f"Skipped '{relative_path}': Already exists.")
                    continue  # Skip this file
                except GithubException as ge:
                    if ge.status != 404:
                        return {"error": f"File check failed: {ge.data.get('message', 'Unknown error')}"}
                        

                # 6. Upload the file
                try:
                    new_repo.create_file(
                        relative_path,
                        "Initial commit",
                        content
                    )
                    upload_log.append(f"Uploaded: {relative_path}")
                except GithubException as ge:
                   return {"error": f"Upload failed: {ge.data.get('message', 'Unknown error')}"} 

        upload_log.append(f"Project '{repo_name}' uploaded successfully.")
        return {"log": upload_log}

    except Exception as e:
        return {"error": str(e)}


def commit_file_to_repo(repo_name: str, file_path: str, local_file_path: str, commit_message: str):
    """
    Commit (create or update) a single file in a GitHub repo.
    :param repo_name: repository full name (e.g. username/reponame)
    :param file_path: path in the repo to upload to (e.g. 'src/main.py')
    :param local_file_path: local file to read content from
    :param commit_message: commit message
    :return: dict with success or error message
    """
    try:
        g = init_github()
        repo = g.get_repo(repo_name)

        with open(local_file_path, "rb") as f:
            content = f.read()

        # Check if file exists to update or create
        try:
            contents = repo.get_contents(file_path)
            # File exists, update it
            repo.update_file(
                path=file_path,
                message=commit_message,
                content=content,
                sha=contents.sha
            )
            return {"message": f"Updated '{file_path}' successfully."}
        except GithubException as ge:
            if ge.status == 404:
                # File does not exist, create it
                repo.create_file(
                    path=file_path,
                    message=commit_message,
                    content=content
                )
                return {"message": f"Created '{file_path}' successfully."}
            else:
                return {"error": f"GitHub error: {ge.data.get('message', 'Unknown error')}"}

    except Exception as e:
        return {"error": str(e)}

def merge_branches(repo_name: str, base_branch: str, head_branch: str, commit_message: str = None):
    """
    Merge a branch into another branch.
    :param repo_name: repository full name (e.g. username/reponame)
    :param base_branch: branch to merge into (e.g. 'main')
    :param head_branch: branch to merge from (e.g. 'feature-branch')
    :param commit_message: optional commit message for merge commit
    :return: dict with success or error message
    """
    try:
        g = init_github()
        repo = g.get_repo(repo_name)

        merge_result = repo.merge(base=base_branch, head=head_branch, commit_message=commit_message or f"Merge {head_branch} into {base_branch}")

        return {"message": f"Branches merged successfully. Commit SHA: {merge_result.sha}"}

    except GithubException as ge:
        # Handle merge conflicts or errors
        if ge.status == 409:
            return {"error": "Merge conflict detected. Please resolve conflicts manually."}
        return {"error": f"GitHub error: {ge.data.get('message', 'Unknown error')}"}

    except Exception as e:
        return {"error": str(e)}

def main():
    print("Welcome to the GitHub Project Manager!")
    print("1. Display all repositories")
    print("2. Access repository contents")
    print("3. Delete a repository")
    print("4. Upload a project to a repository")
    print("5. Commit a file to a repository")
    print("6. Merge branches in a repository")
    choice = input("Enter the number corresponding to your choice: ")

    if choice == '1':
        repos = display_all_repos()
        if isinstance(repos, dict) and "error" in repos:
            print(repos["error"])
        else:
            for repo in repos:
                print(f"Name: {repo['name']}")
                print(f"Description: {repo['description']}")
                print(f"URL: {repo['url']}\n")

    elif choice == '2':
        repo_name = input("Enter the repository name: ")
        result = access_repo_contents(repo_name)
        if isinstance(result, dict) and "error" in result:
            print(result["error"])
        else:
            print(f"Contents of '{repo_name}':")
            for item in result:
                print(f"- {item}")

    elif choice == '3':
        repo_name = input("Enter the repository name to delete: ")
        delete_repository(repo_name)  # already prints internally

    elif choice == '4':
        repo_name = input("Enter the repository name: ")
        description = input("Enter the description for the read me file: ")
        folder_path = input("Enter the folder path to upload: ")
        result = upload_project(repo_name, description, folder_path)
        if isinstance(result, dict) and "error" in result:
            print(f"Error: {result['error']}")
        else:
            print("Upload Log:")
            for line in result["log"]:
                print(line)

    elif choice == '5':
        repo_name = input("Enter the full repository name (e.g., username/reponame): ")
        file_path = input("Enter the path of the file in the repo (e.g., src/main.py): ")
        local_file_path = input("Enter the local file path to commit: ")
        commit_message = input("Enter the commit message: ")
        result = commit_file_to_repo(repo_name, file_path, local_file_path, commit_message)
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print(result["message"])

    elif choice == '6':
        repo_name = input("Enter the full repository name (e.g., username/reponame): ")
        base_branch = input("Enter the base branch (e.g., 'main'): ")
        head_branch = input("Enter the branch to merge from (e.g., 'feature-branch'): ")
        commit_message = input("Enter the merge commit message (optional): ")
        result = merge_branches(repo_name, base_branch, head_branch, commit_message)
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print(result["message"])

    else:
        print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
 


