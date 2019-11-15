#!/bin/bash

#wget https://downloads.wkhtmltopdf.org/0.12/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz -O mktemp.tar.xz
#tar xf mktemp.tar.xz
#sudo cp wkhtmltox/bin/wkhtmltopdf /usr/bin/wkhtmltopdf
#sudo chmod +x /usr/bin/wkhtmltopdf
#rm mktemp.tar.xz
#rm wkhtmltox -rf
sudo yum install redhat-rpm-config python-devel python-pip python-setuptools python-wheel python-cffi libffi-devel cairo pango gdk-pixbuf2
sudo python3.6 -m pip install  -r requirement.txt
sudo yum install -y ImageMagick-devel
sudo yum install -y ghostscript