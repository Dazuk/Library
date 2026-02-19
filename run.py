import os
import pathlib
import urllib.parse
from os import listdir
from os.path import isfile, join

directory = os.getcwd()

if not os.path.exists(os.path.join(directory, ".git")):
    os.system("git init")
    os.system("git remote add origin https://github.com/Dazuk/Library.git")
    os.system("git branch -M main")

with open(os.path.join(directory, "README.md"), 'w', encoding='utf-8') as readme:
    readme.write("# Library\n\n")

    for folder, _, files in os.walk(directory):
        if any(excluded in folder for excluded in ['.git', '.idea']):
            continue

        # Determine relative folder structure
        sub_folders = folder.replace(directory, '').strip(os.sep).split(os.sep)

        if sub_folders and sub_folders[0] != '':
            heading_level = min(len(sub_folders) + 1, 6)  # Ensure max level is ######
            readme.write(f"{'#' * heading_level} {sub_folders[-1]}\n\n")

        for file in sorted(files):
            if file.lower().endswith('.pdf'):  # Adjust file filtering if needed
                relative_path = os.path.join(*(sub_folders + [file]))
                encoded_path = urllib.parse.quote(relative_path).replace('%5C', '/')  # Normalize path for GitHub
                readme.write(f"- [{file.replace('.pdf', '')}]({encoded_path})\n")

        readme.write("\n")

for path in list(pathlib.Path(directory).rglob("*")):
    if path.is_file():
        relative_path = path.relative_to(directory)  # Get relative path
        if ".git" in relative_path.parts or ".idea" in relative_path.parts:
            continue
        os.system(f'git add "{path}"')
        os.system(f'git commit -m "Add {path.name[0:path.name.rfind('.')]}"')
        os.system("git push -u origin main")
