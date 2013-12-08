#!/bin/bash

ssh pault.ag "cd /srv/www/uwsgi/app/dicklord/; git pull"
ssh pault.ag "cd /srv/www/uwsgi/app/dicklord/; ./csv-to-hash.py /home/tag/google.csv > numbers.json"
ssh pault.ag -l www "kill-apps; start-apps"
