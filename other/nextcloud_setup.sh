apt install vim
apt install nginx
apt install php-fpm php-pgsql php-gd php-mbstring php-zip php-soap php-dom php-curl
apt install php-bcmath php-gmp # (performance only)
apt install postgresql
apt install certbot

# configure postgres (via su postgres/psql)
create user nextcloud with password 'PASSWORD';
create database nextcloud  with owner nextcloud;

# configure nginx

# configure ssl
# include acme block in enabled/default
location /.well-known/acme-challenge/ {
    alias /var/www/.well-known/acme-challenge/;
}
systemctl reload nginx

mkdir -p /var/www/.well-known/acme-challenge/;
chown -R www-data /var/www/.well-known/
certbot certonly --webroot -w /var/www -d cloudtest.atlantishq.de --rsa-key-size 2048 --expand
# enable ssl in nginx now (in default server)
listen 443 ssl http2;
ssl_certificate     /etc/letsencrypt/live/cloudtest.atlantishq.de/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/cloudtest.atlantishq.de/privkey.pem;
# delete everything but server name and the stuff you added
systemctl restart nginx

# download nextcloud https://nextcloud.com/install/#instructions-server
cd /var/www/
wget https://download.nextcloud.com/server/releases/nextcloud-19.0.0.zip
unzip nextcloud-19.0.0.zip
chown -R www-data nextcloud
# head to https://docs.nextcloud.com/server/15/admin_manual/installation/nginx.html and add the relevant nginx config, dont foget to fix 301->302 and servernames etc
# correctly set the php handler (i.e. unix:/run/php/php7.3-fpm.sock;)
# increase memory_limit in /etc/php... php.ini to 512MB
systemctl restart nginx

# head to browser and complete setup, ignore the gateway timeout and give it some ~5in or so
