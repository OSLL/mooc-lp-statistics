#!/bin/bash


# Usage:
#     sudo bash ./scripts/add_crontab_entry.sh           # Ubuntu


# Check crontab entry existance
IS_EXIST=`crontab -l 2>/dev/null | grep -o run_update_log_in_db.sh | wc -l`


if [ "${IS_EXIST}" -ne "0" ]
then
    echo "Crontab entry already exists"
    exit 1
fi

line="*/1 * * * * `pwd`/scripts/run_update_log_in_db.sh >> /var/www/mooc-lp-statistics/run_update_log_in_db.log 2>&1"
(crontab -l; echo "$line") | crontab -