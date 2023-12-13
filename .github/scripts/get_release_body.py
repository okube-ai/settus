import os
import logging
from datetime import datetime
from packaging import version

script_root = os.path.dirname(__file__)
package_name = "settus"
package_root = f"./{package_name}/"


def main():

    # Filepaths
    version_filepath = os.path.join(package_root, "_version.py")
    local_env_filepath = os.path.join(script_root, "git.env")
    git_env_filepath = os.getenv("GITHUB_OUTPUT", local_env_filepath)
    changelog_filepath = os.path.join("./", "CHANGELOG.md")

    # Read version file
    with open(version_filepath) as fp:
        v0 = fp.read().split("=")[-1].strip().replace('"', '')
    print(f"Get changes for {package_name} {v0}")

    # Read changelog
    with open(changelog_filepath, 'r') as fp:
        content = fp.read()

    # Select latest changes
    content = content.split("## ")[1]
    content = "\n".join(content.split("\n")[1:]).strip()
    print("Release Content")
    print("---------------")
    print(content)
    print("--------------")

    # Set content as git action variable
    print(f"Setting git env var body {git_env_filepath}")
    with open(git_env_filepath, 'a') as fp:
        fp.write(f"body={content}")

    # Cleanup
    if git_env_filepath == local_env_filepath and os.path.exists(local_env_filepath):
        os.remove(local_env_filepath)


if __name__ == "__main__":
    main()
