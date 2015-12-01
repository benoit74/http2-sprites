Do not throw sprites with HTTP/2
================================

This repository contains the material used to generate OCTO blog article about sprites and HTTP/2.

EN : http://blog.octo.com/en/?p=58039
FR : http://blog.octo.com/?p=57599

Nginx
---------

Nginx has been used as webserver for our tests. If you want more information about HTTP/2 in nginx, there is a [whitepaper](https://www.nginx.com/wp-content/uploads/2015/09/NGINX_HTTP2_White_Paper_v4.pdf) published on this subject.

In our tests nginx was hosted on a Debian Jessie VM. 

### Install nginx 1.9.5 mini

The minimum version with HTTP/2 support is nginx 1.9.5

This version has not yet been validated for many distributions, including Debian Jessie, so we had to include nginx own repository to install this version.

First, install the nginx repositories key

```bash
sudo apt-key add nginx_signing.key
```

Then, add the mainline nginx repository in the apt sources file.

```bash
sudo nano /etc/apt/sources.list
deb http://nginx.org/packages/mainline/debian/ wheezy nginx
deb-src http://nginx.org/packages/mainline/debian/ wheezy nginx
```

And update apt-get to grab this repository content.

```bash
sudo apt-get update
```

Install nginx

```bash
sudo apt-get install nginx
```

### Configure nginx 

Edit the default nginx configuration (location below might change depending on your linux distribution)

```bash
sudo nano /etc/nginx/conf.d/default.conf
```

You first need a simple redirect of all non-encrypted traffic on port 80 to encrypted traffic on port 443

```
server {
    listen       80;
    server_name  localhost;
    location / {
        return 301 https://$host$request_uri:443;
    }
}
```

And you then have to activate https with (or without) http2. The certificates are mandatory for HTTPS operation. HTTP/2 activation or deactivation is simply based on the presence or abscence of the `http2` parameter at the end of the `listen` line

```
server {
    listen      443 ssl http2;
    server_name  localhost;

    ssl_certificate    server.crt;
    ssl_certificate_key server.key;
    
    ... continued with usual configuration ...
```

Since a self-signed certificate is sufficient for our tests, we can create it (and place it in the `/etc/nginx` directory in Debian)

```
sudo bash
cd /etc/nginx
openssl genrsa 1024 > server.key
chmod 400 server.key
openssl req -new -x509 -nodes -sha1 -days 365 -key server.key > server.crt
nginx -s reload
exit
```

### Install HTML/IMG files

We then have to install the HTML/IMG files to be served by nginx. The last version is available at xxx. By default, it has to be placed in the `/usr/share/nginx/html` directory.

```bash
cd /usr/share/nginx/html
wget http://www.oviles.info/sprites.zip
sudo apt-get install unzip
unzip sprites.zip
rm -r __MACOSX/
```

Test client computer
---------

On the client computer, you first need a python installation (most versions are OK) and a working version of Firefox and Chrome.

You then have to install selenium for python, with easy_install for instance:

```bash
sudo easy_install selenium
```

And you also have to install the [ChromeDriver](https://code.google.com/p/selenium/wiki/ChromeDriver) in order to be able to drive Chrome from selenium.

Firefox driver is already available with selenium.
