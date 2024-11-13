Odoo 17.0 Development Environment using Devcontainer
=====================================================

This guide provides instructions for setting up and using a development environment for Odoo 17.0 using Devcontainer.

Prerequisites
-------------

Ensure you have the following installed on your system:

1. Docker
2. Visual Studio Code
3. Remote - Containers extension for Visual Studio Code

Setup
-----

1. Clone this repository to your local machine.

    ```bash
    git clone https://github.com/renzo1974/odoo-devcontainer.git
    ```

2. Open the cloned repository in Visual Studio Code.

3. When prompted by Visual Studio Code, reopen the folder in the Devcontainer.

    This will automatically build the Docker image, start the container and runs some additional steps:
    1. Fetch OCA repositories.
    2. Clone necessary repositories into the workspace.
    3. Install any external Python dependencies specified in the `__manifest__.py` files.

Usage
-----

### Running Odoo

1. Use the provided launch configuration in `launch.json` to start Odoo.
   - Open the Debug panel in VS Code (Ctrl+Shift+D).
   - Select "Start Odoo" configuration.
   - Click the green play button to start debugging.


Conclusion
----------

This setup should provide a comfortable and efficient development environment for working with Odoo 17.0, leveraging Docker and Visual Studio Code's Devcontainer capabilities. Feel free to modify and expand upon this setup to fit your specific needs.