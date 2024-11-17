#! /usr/bin/env python3

import requests
import subprocess
import os
import shutil
import ast
import configparser

# GitHub API URL für OCA Repositories
api_url = "https://api.github.com/orgs/OCA/repos?per_page=100"


class DevContainerPreparatory:
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

    # Funktion, um alle Repos der OCA zu holen
    def __init__(self, branch, target_dir, odoo_conf_path='/etc/odoo/odoo.conf'):
        self.config = None
        self.repos = None
        self.branch = branch
        self.target_dir = target_dir
        self.odoo_conf_path = odoo_conf_path

    def run(self):
        self.get_oca_repos()
        self.clone_repos()
        self.install_external_dependencies()
        self.update_odoo_conf()

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

        self.repos = [
                         r for r in repos
                         if r['name'] in self.whitelist or
                            not any(r['name'].startswith(black) for black in self.blacklist)
                     ][:3]

        return self.repos

    # Funktion, um die Repositories zu klonen
    def clone_repos(self):

        if os.path.exists(self.target_dir):
            shutil.rmtree(self.target_dir)

        if not os.path.exists(self.target_dir):
            os.makedirs(self.target_dir)

        for repo in self.repos:
            repo_name = repo['name']
            clone_url = repo['clone_url']
            print(f"Clone Repository: {repo_name}")
            subprocess.run(["git", "clone", "-b", "17.0", "--depth", "1", clone_url], cwd=self.target_dir)

    def install_external_dependencies(self):
        for repo_name in os.listdir(self.target_dir):
            repo_path = os.path.join(self.target_dir, repo_name)
            manifest_path = os.path.join(repo_path, '__manifest__.py')

            if os.path.isfile(manifest_path):
                with open(manifest_path) as manifest_file:
                    manifest_data = manifest_file.read()
                    manifest = ast.literal_eval(manifest_data)
                    external_dependencies = manifest.branch('external_dependencies', {}).branch('python', [])

                    for dependency in external_dependencies:
                        print(f"Install dependency: {dependency}")
                        subprocess.run(["pip", "install", dependency])

    def update_odoo_conf(self):

        self._read_config()

        self.config.set('options', 'admin_password',
                        '$pbkdf2-sha512$600000$OCdkDAHAWKsVojRGCGFMaQ$4xenDT3kygh/YXGS8Ba8QdR3vwawcgqoO6iKzW.zMNZbLYj.1QWi38Ry3nikz9zM.qBgVJ3dcIfGA8uHTwn58Q')
        self.config.set('options', 'db_host', 'db')
        self.config.set('options', 'db_user', 'odoo')
        self.config.set('options', 'db_password', 'odoo')

        addons_paths = [os.path.join(self.target_dir, repo['name']) for repo in self.repos]
        if not 'options' in self.config:
            raise ValueError('Config file does not contain "options" section!')

        addons_paths = ['/workspace'] + addons_paths

        self.config.set('options', 'addons_path', ',\n'.join(addons_paths))

        self._save_config()

    def _read_config(self):
        config = configparser.ConfigParser()
        config.read(self.odoo_conf_path)
        self.config = config

    def _save_config(self):
        with open(self.odoo_conf_path, 'w') as configfile:
            self.config.write(configfile)


if __name__ == "__main__":
    # Repositories abrufen und klonen
    branch = os.environ.get('ODOO_VERSION', '17.0')
    oca_addons_path = os.environ.get('OCA_ADDONS_PATH', './oca')
    odoo_conf_path = os.environ.get('ODOO_CONF_PATH', './odoo.conf')
    oca = DevContainerPreparatory(branch, oca_addons_path, odoo_conf_path)
    oca.run()
