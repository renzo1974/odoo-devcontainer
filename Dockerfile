FROM odoo:17

USER root

RUN sed -i 's|; admin_passwd = admin|admin_passwd = $pbkdf2-sha512$600000$OCdkDAHAWKsVojRGCGFMaQ$4xenDT3kygh/YXGS8Ba8QdR3vwawcgqoO6iKzW.zMNZbLYj.1QWi38Ry3nikz9zM.qBgVJ3dcIfGA8uHTwn58Q|g' /etc/odoo/odoo.conf

RUN mkdir -p /workspace/core/odoo && \
    ln -s /usr/lib/python3/dist-packages/odoo /workspace/core/odoo && \
    mkdir -p /workspace/core/data && \
    ln -s /var/lib/odoo /workspace/core/data && \
    mkdir -p /workspace/conf && \
    ln -s /etc/odoo /workspace/conf && \
    mkdir -p /workspace/addons && \
    ln -s /mnt/extra-addons /workspace/addons && \
    mkdir -p /workspace/.vscode

COPY launch.json /workspace/.vscode/launch.json
COPY clone_oca_repos.py /workspace/scripts/clone_oca_repos.py

# Install additional tools or dependencies if needed
