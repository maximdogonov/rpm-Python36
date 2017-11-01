rpm-python36
============

An RPM spec file build and alt-install Python 3.6.3 on RHEL.

To Build:

`mkdir -p ~/rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}`

`sudo yum -y install rpmdevtools && rpmdev-setuptree`

`sudo yum -y install tk-devel tcl-devel expat-devel db4-devel gdbm-devel sqlite-devel bzip2-devel openssl-devel ncurses-devel readline-devel`

`wget https://raw.github.com/maximdogonov/rpm-Python36/master/python363.spec -O ~/rpmbuild/SPECS/python363.spec`

`wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tgz -O ~/rpmbuild/SOURCES/Python-3.6.3.tgz`

`rpmbuild -bb ~/rpmbuild/SPECS/python363.spec`

`yum --nogpgcheck localinstall rpmbuild/RPMS/x86_64/python36-3.6.3-1.x86_64.rpm rpmbuild/RPMS/python36-devel-3.6.3-1.x86_64.rpm`