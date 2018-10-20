/etc/hosts

gunicorn -b 127.0.0.1:8000 --chdir app main:application

sudo /usr/sbin/nginx -c /home/katze/back/nginx.conf
sudo /usr/sbin/nginx -s stop

ab -c 4 -n 5000 http://somewhere.com/api/
ab -c 4 -n 5000 http://somewhere.com/
ab -c 4 -n 5000 http://127.0.0.1:8000/
ab -c 4 -n 5000 http://127.0.0.1:8000/api/

curl -v -H  'User-Agent:telnet/hands' 'http://mail.ru/robots.txt'
curl -o robots.txt http://mail.ru/robots.txt

telnet www.mail.ru 80
GET /robots.txt HTTP/1.1
Host: www.mail.ru

flake8 app/main.py
