Odoo 17.0 Development Environment using Devcontainer
=====================================================

This guide provides instructions for setting up and using a development environment for Odoo 17.0 using Devcontainer.

## Prerequisites

Ensure you have the following installed on your system:

1. Docker
2. Visual Studio Code
3. Remote - Containers extension for Visual Studio Code

## Setup

1. Clone this repository to your local machine.

    ```bash
    git clone <your-repo-url>
    cd <your-repo-directory>
    ```

2. Open the cloned repository in Visual Studio Code.

    ```bash
    code .
    ```

3. When prompted by Visual Studio Code, reopen the folder in the Devcontainer.

    This will automatically build the Docker image and start the container based on the configurations provided in the `.devcontainer.json`, `Dockerfile`, and `docker-compose.yml`.

## Configuration Files

### .devcontainer.json

This file contains the configuration for the development container.

Key configurations include:

- The Docker Compose file to use: `docker-compose.yml`
- The service to run: `devcontainer`
- Post-create commands to run: `python3 /workspace/scripts/clone_oca_repos.py`
- Customizations for VS Code including extensions and settings.

### Dockerfile

The `Dockerfile` sets up the Odoo 17 environment, links necessary directories, and copies the `clone_oca_repos.py` script to the container.

### docker-compose.yml

This file defines the services, including the `devcontainer` service and the `db` service using PostgreSQL.

## Usage

### Running Odoo

1. The container will start with the command `sleep infinity` to keep it running.
2. Use the provided launch configuration in `launch.json` to start Odoo.
   - Open the Debug panel in VS Code (Ctrl+Shift+D).
   - Select "Start Odoo" configuration.
   - Click the green play button to start debugging.

### Clone and Install OCA Repositories

The script `clone_oca_repos.py` will:

1. Fetch OCA repositories.
2. Clone necessary repositories into the workspace.
3. Install any external Python dependencies specified in the `__manifest__.py` files.

This script is executed automatically after the container creation due to the `postCreateCommand` setting in `.devcontainer.json`.

If you need to rerun the script manually:

```bash
python3 /workspace/scripts/clone_oca_repos.py
```

### PostgreSQL Database

The PostgreSQL database is set up and managed inside the container. The following environment variables are set for the PostgreSQL service:

- `POSTGRES_PASSWORD=odoo`
- `POSTGRES_USER=odoo`
- `POSTGRES_DB=postgres`

### Volumes

The `docker-compose.yml` file defines a volume `postgres-data` for persisting PostgreSQL data across container restarts.

## Customizing

### Adding Extensions

You can add VS Code extensions by updating the `.devcontainer.json`:

```json
  "customizations": {
    "vscode": {
      "extensions": [
        "your-extension-id"
      ]
    }
  }
```

### Installing Additional Tools

You can install additional dependencies in the `Dockerfile`:

```dockerfile
# Install additional tools or dependencies if needed
RUN apt-get update && apt-get install -y some-package
```

## Excluding Files

The VS Code configuration within `.devcontainer.json` includes settings to exclude certain directories from file watching to enhance performance:

```json
"files.watcherExclude": {
    "**/odoo/**": true,
    "**/addons/**": true,
    "**/conf/**": true
},
"files.exclude": {
    "**/.devcontainer": true
}
```

## Conclusion

This setup should provide a comfortable and efficient development environment for working with Odoo 17.0, leveraging Docker and Visual Studio Code's Devcontainer capabilities. Feel free to modify and expand upon this setup to fit your specific needs.