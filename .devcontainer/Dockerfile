FROM odoo:17

ARG ODOO_VERSION=17.0
ARG OCA_ADDONS_PATH=/mnt/extra-addons/oca
ARG ODOO_CONF_PATH=/etc/odoo/odoo.conf

ENV ODOO_VERSION=${ODOO_VERSION}
ENV OCA_ADDONS_PATH=${OCA_ADDONS_PATH}
ENV ODOO_CONF_PATH=${ODOO_CONF_PATH}

USER root

RUN apt-get update && apt-get install -y \
    git \
    vim \
    curl \
    wget \
    gcc \
    && apt-get clean

#RUN mkdir -p /workspace/core/odoo && \
#    ln -s /usr/lib/python3/dist-packages/odoo /workspace/core/odoo && \
#    mkdir -p /workspace/core/data && \
#    ln -s /var/lib/odoo /workspace/core/data && \
#    mkdir -p /workspace/conf && \
#    ln -s /etc/odoo /workspace/conf && \
#    mkdir -p /workspace/addons && \
#    ln -s /mnt/extra-addons /workspace/addons && \
RUN mkdir -p /workspace/.vscode

COPY launch.json /workspace/.vscode/launch.json
COPY prepare_dev.py /usr/local/bin/prepare_dev.py

RUN /usr/local/bin/prepare_dev.py

