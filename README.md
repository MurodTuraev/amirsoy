# Amirsoy e-polis

# SQLite Jadvaldan malumotlarni o`chirish va schotchikni reset qilish
``` 
delete from api_report;    
delete from sqlite_sequence where name='api_report';
```

# PDF qilish uchun zarur
```
sudo apt install default-jre libreoffice-java-common
sudo apt install libreoffice-gnome libreoffice
```


----------------------------------------------
# Loyihani Ubuntu server 20.04 ga o'rnatish
## 1-qadam. Ubuntu omborlaridan barcha bog'liqlik paketlarni o'rnatish
``` 
sudo apt update
sudo apt install python3-venv libpq-dev postgresql postgresql-contrib nginx curl
```
## 2-qadam. PostgreSQL maʼlumotlar bazasini o'rnatish va foydalanuvchi yaratish
``` 
sudo -u postgres psql
CREATE DATABASE amirsoydb;
CREATE USER ulugbek WITH PASSWORD 'nc778119';

ALTER ROLE ulugbek SET client_encoding TO 'utf8';
ALTER ROLE ulugbek SET default_transaction_isolation TO 'read committed';
ALTER ROLE ulugbek SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE amirsoydb TO ulugbek;
```

## 3-qadam. Github dan loyihani ko'chirib olish va virtualmuhit yaratish
``` 
git clone https://github.com/dohcgle/amirsoy.git
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
```

## 4-qadam. requirements.txt o'rnatish va loyihani sozlash
``` 
pip install -r requirements.txt
sudo nano amirsoy/settings.py
```
### Postgresql bazasini sozlash
``` 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'amirsoydb',
        'USER': 'ulugbek',
        'PASSWORD': 'nc778119',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```

``` 
./manage.py makemigrations
./manage.py migrate
./manage.py createsuperuser
./manage.py collectstatic
```

### 8000 port uchun istisno yaratish:
``` 
sudo ufw allow 8000
```
``` 
./manage.py runserver 0.0.0.0:8000
```
## Gunicorn ning loyihaga xizmat qilish qobiliyatini sinab ko'rish
``` 
gunicorn --bind 0.0.0.0:8000 amirsoy.asgi -w 4 -k uvicorn.workers.UvicornWorker
```

## 5-qadam. Gunicorn uchun tizimli socket va xizmat fayllarini yaratish
``` 
sudo nano /etc/systemd/system/gunicorn.socket
```
### Socket fayli ichiga quyidagini yozamiz:
``` 
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

``` 
sudo nano /etc/systemd/system/gunicorn.service
```
### Xizmat fayli ichiga quyidagini yozamiz:

``` 
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=ulugbek
Group=www-data
WorkingDirectory=/home/ulugbek/amirsoy
ExecStart=/home/ulugbek/asakabank/venv/bin/gunicorn \
          --access-logfile - \
          -k uvicorn.workers.UvicornWorker \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          asakabank.asgi:application
[Install]
WantedBy=multi-user.target       
```

``` 
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
```

## 6-qadam. Gunicorn soket faylini tekshirish
``` 
sudo systemctl status gunicorn.socket
file /run/gunicorn.sock
```

## 7-qadam. Socketni faollashtirishni sinab ko'rish
``` 
sudo systemctl status gunicorn

sudo systemctl daemon-reload
sudo systemctl restart gunicorn

```

## 8-qadam. Nginx ni Gunicorn ga proksi-server sifatida sozlash:

``` 
sudo nano /etc/nginx/sites-available/amirsoy
```
### fayl ichiga quyidagi buyruqlarni yozamiz:
``` 
server {
    listen 80;
    server_name 192.168.122.91; # IP address sozlanadi

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/ulugbek/amirsoy;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

``` 
sudo ln -s /etc/nginx/sites-available/amirsoy /etc/nginx/sites-enabled
```

``` 
sudo nginx -t
sudo systemctl restart nginx
```


# pgAdmin4 o'rnatish
```
sudo curl https://www.pgadmin.org/static/packages_pgadmin_org.pub | sudo apt-key add
sudo sh -c 'echo "deb https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/$(lsb_release -cs) pgadmin4 main" > /etc/apt/sources.list.d/pgadmin4.list && apt update'
sudo apt install pgadmin4-web
```

### Apache server portni o'zgartirish
``` 
sudo nano /etc/apache2/ports.conf
listen 80 > 8081
sudo systemctl restart apache2
sudo service apache2 restart
```

## pgAdmin4 web serverni sozlash
``` 
sudo /usr/pgadmin4/bin/setup-web.sh
email: utn1002@gmail.com
pass: nc778119
```

# Postgresql bazasiga dostup berish.

``` 
sudo nano /etc/postgresql/12/main/pg_hba.conf
```
### Quyidagini qo'shish kk:
``` 
host     all            all             0.0.0.0/0               md5
```
----------------------------------------------------------------------------
``` 
sudo nano /etc/postgresql/12/main/postgresql.conf  
```
### Quyidagini qo'shish kk:
``` 
listen_addresses = '*'
```


### Payme Create paycom user
```
python manage.py create_paycom_user
```