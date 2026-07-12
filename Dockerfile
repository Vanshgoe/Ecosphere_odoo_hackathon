FROM odoo:18.0

USER root
RUN mkdir -p /mnt/extra-addons /var/lib/odoo /etc/odoo \
    && chown -R odoo:odoo /mnt/extra-addons /var/lib/odoo /etc/odoo

USER odoo
