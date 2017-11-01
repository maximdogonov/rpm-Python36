rpm-python36
============

An RPM spec file build and alt-install Python 3.6.3 on RHEL.

To Build:

`sudo yum -y install rpmdevtools && rpmdev-setuptree`

`sudo yum -y install tk-devel tcl-devel expat-devel db4-devel gdbm-devel sqlite-devel bzip2-devel openssl-devel ncurses-devel readline-devel`

`wget https://raw.github.com/nmilford/rpm-python27/master/python363.spec -O ~/rpmbuild/SPECS/python363.spec`

`wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tgz -O ~/rpmbuild/SOURCES/Python-3.6.3.tgz`

`rpmbuild -bb ~/rpmbuild/SPECS/python363.spec`
