#! /usr/bin/env python3

import requests
import subprocess
import os
import ast

# GitHub API URL für OCA Repositories
api_url = "https://api.github.com/orgs/OCA/repos?per_page=100"

class OcaRepoGather:

    # Funktion, um alle Repos der OCA zu holen
    def get_oca_repos(self):
        repos = []
        page = 1

        while True:
            response = requests.get(f"{api_url}&page={page}")
            if response.status_code != 200:
                print("Fehler beim Abrufen der Repos")
                break

            data = response.json()
            if not data:
                break

            repos.extend(data)
            page += 1

        return repos

    # Funktion, um die Repositories zu klonen
    def clone_repos(self, repos, target_dir):
        blacklist = [
            '.github',
            'ansible-odoo',
            'apps-store',
            'community-data-files',
            'contribute-md-template',
            'dotnet',
            'l10n-',
            'maintainer-quality-tools',
            'maintainer-tools',
            'mirrors-flake8'
            'oca-addons-repo-template',
            'oca-ci',
            'oca-custom',
            'oca-decorators',
            'oca-github-bot',
            'oca-weblate-deployment',
            'oca-recipe.odoo',
            'OCB', 
            'odoo-community.org',
            'odoo-module-migrator',
            'odoo-pre-commit-hooks',
            'odoo-test-helper',
            'OpenUpgrade', 
            'openupgradelib',
            'pylint-odoo', 
            'repo-maintainer'
            'repo-maintainer-conf'
            'runbot-addons'
            'shift-planning',
            'vertical-',
            'wallet',
            'webhook',
            'webkit-tools',
            ]
        whitelist = [
            'l10n-switzerland',
            ]
        
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        for repo in repos:
            repo_name = repo['name']
            if repo_name not in whitelist and any(repo_name.startswith(black) for black in blacklist):
                continue

            clone_url = repo['clone_url']
            print(f"Klone Repository: {repo_name}")
            subprocess.run(["git", "clone", "-b", "17.0", "--depth", "1", clone_url], cwd=target_dir)

    def install_external_dependencies(self, target_dir):
        for repo_name in os.listdir(target_dir):
            repo_path = os.path.join(target_dir, repo_name)
            manifest_path = os.path.join(repo_path, '__manifest__.py')

            if os.path.isfile(manifest_path):
                with open(manifest_path) as manifest_file:
                    manifest_data = manifest_file.read()
                    manifest = ast.literal_eval(manifest_data)
                    external_dependencies = manifest.get('external_dependencies', {}).get('python', [])

                    for dependency in external_dependencies:
                        print(f"Installiere Abhängigkeit: {dependency}")
                        subprocess.run(["pip", "install", dependency])


if __name__ == "__main__":
    # Zielverzeichnis für die Repositories
    target_directory = "/workspace/addons/oca"
    conf_file_path = "/workspace/conf/odoo/odoo.conf"

    # Repositories abrufen und klonen
    oca = OcaRepoGather()
    oca_repos = oca.get_oca_repos()
    oca.clone_repos(oca_repos, target_directory)
    oca.install_external_dependencies(target_directory)

    # Konfigurationsdatei für Odoo anpassen
    with open(conf_file_path, 'r') as conf_file:
        lines = conf_file.readlines()

    addons_paths = ",".join([f"{target_directory}/{repo['name']}" for repo in oca_repos])
    found = False

    for i, line in enumerate(lines):
        if line.startswith('addons_path'):
            existing_paths = line.strip().split('=')[1].strip()
            combined_paths = f"{existing_paths},{addons_paths}"
            lines[i] = f"addons_path = {combined_paths}\n"
            found = True
            break

    if not found:
        lines.append(f"\naddons_path = {addons_paths}\n")

    with open(conf_file_path, 'w') as conf_file:
        conf_file.writelines(lines)
