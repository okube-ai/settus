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
    changelog_filepath = os.path.join("./", "CHANGELOG.md")
    body_filepath = os.path.join(script_root, "release_body.md")

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

    # Write body
    print(f"Writing body {body_filepath}")
    with open(body_filepath, 'w') as fp:
        fp.write(content)

    if os.getenv("GITHUB_OUTPUT") is None:
        os.remove(body_filepath)


if __name__ == "__main__":
    main()
