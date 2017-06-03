sudo apt install php5-common php5 php5-curl php5-fpm php5-gd php5-mysql

wget https://download.nextcloud.com/server/releases/nextcloud-12.0.0.zip
unzip nextcloud-12.0.0.zip
sudo cp -r nextcloud /var/www/html/
wget https://dl.eff.org/certbot-auto
chmod a+x certbot-auto

wget ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.40.tar.gz
tar -zxf pcre-8.40.tar.gz
cd pcre-8.40
./configure
make
sudo make install
cd ..
wget http://zlib.net/zlib-1.2.11.tar.gz
tar -zxf zlib-1.2.11.tar.gz
cd zlib-1.2.11
./configure
make
sudo make install
cd ..
wget http://www.openssl.org/source/openssl-1.0.2f.tar.gz
tar -zxf openssl-1.0.2f.tar.gz
cd openssl-1.0.2f
./config
make
sudo make install
cd ..
wget http://nginx.org/download/nginx-1.11.13.tar.gz
tar -zxf nginx-1.11.13.tar.gz
cd nginx-1.11.13
./configure --prefix=/etc/nginx --sbin-path=/usr/sbin/ --conf-path=/etc/nginx/nginx.comf --with-threads --with-file-aio --with-http_ssl_module --with-http_mp4_module --with-http_gzip_static_module --with-http_gunzip_module --with-http_secure_link_module --with-stream --with-stream_ssl_module --user www-data --group www-data
make
sudo make install
sudo mkdir -p /etc/nginx/sites-available
sudo mkdir -p /etc/nginx/sites-enabled
cd ..
#sudo ./certbot-auto certonly
#sudo service nginx restart
