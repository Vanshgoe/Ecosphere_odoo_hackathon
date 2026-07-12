FROM odoo:18.0
USER root
COPY requirements.txt /tmp/requirements.txt
RUN if [ -s /tmp/requirements.txt ]; then pip3 install --break-system-packages --no-cache-dir -r /tmp/requirements.txt; fi
USER odoo
