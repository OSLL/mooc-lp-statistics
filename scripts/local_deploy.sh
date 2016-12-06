#!/bin/bash

CATALOG='mooc-lp-statistics'
HOSTS_STRING="127.0.0.1 mooc-lp-statistics"
DEBUG_FILE="/var/www/geomongo/DEBUG"
CONFIG_FILE="mooc-lp-statistics.conf"

if ! grep -Fxq "$HOSTS_STRING" /etc/hosts
then
	echo "$HOSTS_STRING" >> /etc/hosts
fi


rm -rf /var/www/"$CATALOG"

mkdir /var/www/"$CATALOG"

cp -r ./  /var/www/"$CATALOG"
cp config/"$CONFIG_FILE" /etc/apache2/sites-available/
./scripts/setup_pip_dependencies.sh




chown -R www-data:www-data /var/www/"$CATALOG"

a2ensite $CONFIG_FILE

service apache2 restart
