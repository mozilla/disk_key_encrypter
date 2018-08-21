# Overview

This directory contains configuration files for deploying [OpenResty](https://openresty.org/)
as well as instructions for deploying WDE in a dual instance model using Openresty
as an authenticating reverse proxy.

One instance of WDE will be the non-public instance which will surface the administrative
interface, will bind to port 443 and will be accessed exclusively via VPN on a
private IP

The other instance of WDE will be the public instance which will not surface the
administrative interface, will bind to port 81 and will be fronted by the Zeus
load balancer which will take care of terminating TLS and forwarding traffic to
port 81 on the server

# Pre-requisites

* Ensure the server has outbound internet access to the [OpenResty Package Manager](https://opm.openresty.org/)
  which may require establishing proxy ACLs as in [Bug 1483054](https://bugzilla.mozilla.org/show_bug.cgi?id=1483054)
* Get rid of the dual network interface cards and IPs as this setup will use a
  single IP with listeners on two different ports
* Have Auth0 client_id and client_secrets provisioned for the instances. You'll
  need these values to configure OpenResty

# Deployment

## Install packages

```
gpg="gpg --no-default-keyring --secret-keyring /dev/null --keyring /dev/null --no-option --keyid-format 0xlong"
rm /etc/yum.repos.d/CentOS-*  # https://bugzilla.mozilla.org/show_bug.cgi?id=1329078
rpmkeys --import /etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7
rpm -qi gpg-pubkey-f4a80eb5 | $gpg | grep 0x24C6A8A7F4A80EB5
rpmkeys --import https://dl.fedoraproject.org/pub/epel/RPM-GPG-KEY-EPEL-7
rpm -qi gpg-pubkey-352c64e5 | $gpg | grep 0x6A2FAEA2352C64E5
rpmkeys --import https://openresty.org/package/pubkey.gpg
rpm -qi gpg-pubkey-d5edeb74 | $gpg | grep 0x97DB7443D5EDEB74
yum-config-manager --add-repo https://openresty.org/package/centos/openresty.repo
# yum update -y
yum install -y --setopt=tsflags=nodocs epel-release
yum install -y --setopt=tsflags=nodocs sudo openssl-devel lua-devel yum-utils openresty openresty-resty openresty-opm python-pip
opm get zmartzone/lua-resty-openidc
opm get pintsized/lua-resty-http\>=0.12  # 0.12 or newer is required to support our datacenter http proxies
```

## Make TLS certs for non-public instance

This is a placeholder for whatever actual cert we'll use on the non-public instance.
This will be replaced by letsencrypt or digicert or the Mozilla CA.

```
mkdir -v /usr/local/openresty/nginx/conf/ssl
openssl_cnf_filename=`mktemp`
printf "[dn]\nCN=localhost\n[req]\ndistinguished_name = dn\n[EXT]\nsubjectAltName=DNS:localhost\nkeyUsage=digitalSignature\nextendedKeyUsage=serverAuth" > $openssl_cnf_filename
/usr/local/openresty/openssl/bin/openssl req -x509 -out /usr/local/openresty/nginx/conf/ssl/localhost.crt \
  -keyout /usr/local/openresty/nginx/conf/ssl/localhost.key \
  -newkey rsa:2048 -nodes -sha256 -subj '/CN=localhost' -extensions EXT -config $openssl_cnf_filename
```

## Deploy the OpenResty configuration files

Run this from the deployed root of this repo

```
mkdir -v /usr/local/openresty/nginx/conf/conf.d/
cp openresty/conf.d/* /usr/local/openresty/nginx/conf/conf.d/
cp openresty/nginx.conf /usr/local/openresty/nginx/conf/
```

## Deploy the Apache configuration files

Run this from the deployed root of this repo

```
cp apache/config.d/desktop_disk_encrypter_public_localhost.conf /etc/httpd/conf.d/
cp apache/config.d/desktop_disk_encrypter_localhost.conf /etc/httpd/conf.d/
```

In addition to deploying these new Apache configs, you'll need to disable the
existing configs.

```
mv -v /etc/httpd/conf.d/00-custom.conf /etc/httpd/conf.d/00-custom.conf.disabled
mv -v /etc/httpd/conf.d/00-81.conf /etc/httpd/conf.d/00-81.conf.disabled
mv -v /etc/httpd/conf.d/desktop_disk_encrypter.conf /etc/httpd/conf.d/desktop_disk_encrypter.conf.disabled
mv -v /etc/httpd/conf.d/ssl.conf /etc/httpd/conf.d/ssl.conf.disabled
mv -v /etc/httpd/conf.d/desktop_disk_encrypter_ssl.conf /etc/httpd/conf.d/desktop_disk_encrypter_ssl.conf.disabled
apachectl configtest
apachectl graceful
```

If you need to revert this you can run

```
mv -v /etc/httpd/conf.d/00-custom.conf.disabled /etc/httpd/conf.d/00-custom.conf ; mv -v /etc/httpd/conf.d/00-81.conf.disabled /etc/httpd/conf.d/00-81.conf ; mv -v /etc/httpd/conf.d/desktop_disk_encrypter.conf.disabled /etc/httpd/conf.d/desktop_disk_encrypter.conf ; mv -v /etc/httpd/conf.d/ssl.conf.disabled /etc/httpd/conf.d/ssl.conf ; mv -v /etc/httpd/conf.d/desktop_disk_encrypter_ssl.conf.disabled /etc/httpd/conf.d/desktop_disk_encrypter_ssl.conf
```

Once you've configured Apache, restart it to bring the new configs live

## Update the Django code

Update the Django code in the two deployed instances with the new code that supports
OpenResty and uses the RemoteUserBackend

## Configure OpenResty secrets

Create the two secrets files for OpenResty. These files are called
* `/usr/local/openresty/nginx/conf/conf.d/secrets-non-public.conf`
* `/usr/local/openresty/nginx/conf/conf.d/secrets-public.conf`

Base them off the [`openresty/conf.d/secrets.conf-dist`](conf.d/secrets.conf-dist)
file's contents

## Configure Django secrets

Create the two Django settings files for the public and non-public instances.
These files are called
* `/data/desktop_disk_encrypter/settings_non_public.py`
* `/data/desktop_disk_encrypter/settings_public.py`

Base them off the [`settings_public_or_non_public.py-dist`](../settings_public_or_non_public.py-dist)
file's contents

## Start OpenResty

You can start OpenResty manually by running

```
/usr/bin/openresty -g 'daemon off;'
```

Or you can use the included `init.d` script by running

```
service openresty start
```

Or you can create a systemd file to launch it.

`/usr/bin/openresty` is a symlink to `/usr/local/openresty/nginx/sbin/nginx`.

You can view OpenResty logs with

```
tail -f /usr/local/openresty/nginx/logs/*.log
```

# Access Control

Access to WDE is governed differently for the two different instances of the
Django app.

## Public Site Access Control

The public site (which is accessed via port 81 on OpenResty) requires that users
log into Mozilla Single Sign On (SSO) with a valid user. Beyond logging in,
there are no authorization requirements for users. This means that most any user
can log in and submit a key that they'd like escrowed in WDE

## Non-Public Site Access Control

The non-public site (which is accessed via port 443 on OpenResty) requires that
users log into Mozilla SSO with a valid user and that they be a member of the
group configured in  `/usr/local/openresty/nginx/conf/conf.d/secrets-non-public.conf`
and `/data/desktop_disk_encrypter/settings_non_public.py`. The list of groups
that the user is a member of is conveyed to OpenResty via an OIDC claim. This
in turn is passed to the Django app via HTTP headers.

The group that users must be a member of is set in the setting `OIDC_DESKTOP_CLAIM_GROUP`
in `/data/desktop_disk_encrypter/settings_non_public.py` and in the setting
`$allowed_group` in `/usr/local/openresty/nginx/conf/conf.d/secrets-non-public.conf`

Any user who logs in and is a member of the group set in those settings will be
able to access the administration interface via the non-public site but any user
that logs in and is not a member of that group will be redirected to an error
page.

The reason that the group must be configured no only in OpenResty (via `/usr/local/openresty/nginx/conf/conf.d/secrets-non-public.conf`)
but also in Django (via `/data/desktop_disk_encrypter/settings_non_public.py`)
is that both OpenResty and Django check the user's group membership. This is an
added layer of redundancy if OpenResty was somehow circumvented.

# Flows

## Public Instance

* User browses to the WDE DNS name over https which resolves to the IP of a Zeus
  VIP
* The Zeus VIP terminates TLS and forwards the connection to the backend server
  on port 81
* Listening on port 81 is OpenResty which takes the connection, authenticates
  user and forward the traffic to 127.0.0.1:5001
* Listening on 127.0.0.1:5001 is Apache which passes the request to the Django 
  wsgi server which hosts the public WDE instance

## Non Public Instance
 
* User browses to the internal WDE DNS name over https which resolves to the
  private IP of the WDE server
* Listening on port 443 is OpenResty which takes the connection, authenticates
  user and forward the traffic to 127.0.0.1:5000
* Listening on 127.0.0.1:5000 is Apache which passes the request to the Django
  wsgi server which hosts the non-public WDE instance
