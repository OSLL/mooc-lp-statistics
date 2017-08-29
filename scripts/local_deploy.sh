#!/bin/bash

CATALOG='mooc-lp-statistics'
HOSTS_STRING="127.0.0.1 mooc-lp-statistics"
CONFIG_FILE="mooc-lp-statistics.conf"
SETTINGS_JSON=false
DJANGO_USER_NAME="admin"
DJANGO_USER_EMAIL='admin@mooclpstatistics.ru'

PASSWORD="$1" # <- means take first script argument
########################################################################

if ! grep -Fxq "$HOSTS_STRING" /etc/hosts
then
	echo "$HOSTS_STRING" >> /etc/hosts
fi

if [ -f /var/www/"$CATALOG"/App/settings.json ];
then
    mv /var/www/"$CATALOG"/App/settings.json /var/tmp/
    SETTINGS_JSON=true;
fi
rm -rf /var/www/"$CATALOG"

mkdir /var/www/"$CATALOG"

if [ "$SETTINGS_JSON" == "true" ];
then
    rsync -r --exclude='App/settings.json' ./  /var/www/"$CATALOG"
    mv /var/tmp/settings.json /var/www/"$CATALOG"/App/
else
    cp -r ./  /var/www/"$CATALOG"
fi

cp config/"$CONFIG_FILE" /etc/apache2/sites-available/
./scripts/setup_pip_dependencies.sh

cd /var/www/"$CATALOG"/
python ./manage.py collectstatic -v0 --noinput

chown -R www-data:www-data /var/www/"$CATALOG"

if [ -z "$PASSWORD" ]
then
	PASSWORD=`date +%s | sha256sum | base64 | head -c 32`
        echo "Generated PASSWORD ${PASSWORD}"
fi

/usr/bin/python /var/www/mooc-lp-statistics/manage.py migrate
/usr/bin/python /var/www/mooc-lp-statistics/manage.py createadminuser --login=${DJANGO_USER_NAME} --email=${DJANGO_USER_EMAIL} --password=${PASSWORD}

a2ensite $CONFIG_FILE

service apache2 restart
