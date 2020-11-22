#! /bin/bash
source ~/.bash_profile
source /home/ec2-user/virtualenv/waffleBackend/bin/activate
cd /home/ec2-user/waffle-server/
git pull origin deploy
cd waffle_backend
python3 -m pip install requirements.txt
python3 manage.py migrate
python3 manage.py check --deploy
uwsgi --ini uwsgi.ini
nginx -t
sudo service nginx restart
