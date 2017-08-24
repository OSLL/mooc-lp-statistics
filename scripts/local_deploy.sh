#!/bin/bash

CATALOG='mooc-lp-statistics'
HOSTS_STRING="127.0.0.1 mooc-lp-statistics"
CONFIG_FILE="mooc-lp-statistics.conf"
SETTINGS_JSON=false
DJANGO_USER_NAME = 'admin'

echo "Enter username for django superuser"
read django_user_name

python manage.py migrate
python manage.py createsuperuser --username ${django_user_name}

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

a2ensite $CONFIG_FILE

service apache2 restart