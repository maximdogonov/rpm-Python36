# To Build:
#
# sudo yum -y install rpmdevtools && rpmdev-setuptree
# sudo yum -y install tk-devel tcl-devel expat-devel db4-devel gdbm-devel sqlite-devel bzip2-devel openssl-devel ncurses-devel readline-devel
# rpmbuild -bb ~/rpmbuild/SPECS/python363.spec


##########################
#  User-modifiable configs
##########################
## WARNING:
##  Commenting out doesn't work
##  Last line is what's used.

#  Define Constants
%define name python36
%define version 3.6.3
%define libvers 3.6
%define release 1
%define __prefix /usr


#  Build tkinter?  "auto" enables it if /usr/bin/wish exists.
%define config_tkinter yes
#%define config_tkinter auto
#%define config_tkinter no


#  Include HTML documentation?
#%define config_include_docs yes
%define config_include_docs no


#  Include tools?
#%define config_include_tools no
%define config_include_tools yes


#  Enable IPV6?
#%define config_ipv6 yes
%define config_ipv6 no


#  Use pymalloc?
#%define config_pymalloc no
%define config_pymalloc yes


#  Is the resulting package and the installed binary named "python" or "python2"?
#%define config_binsuffix none
%define config_binsuffix 3.6


#  Build shared libraries or .a library?
%define config_sharedlib yes
#%define config_sharedlib no


#  Location of the HTML directory to place tho documentation in?
%define config_htmldir /var/www/html/python%{version}


#################################
#  End of user-modifiable configs
#################################

#  detect if tkinter should be included
%define include_tkinter %(if [ \\( "%{config_tkinter}" = auto -a -f /usr/bin/wish \\) -o "%{config_tkinter}" = yes ]; then echo 1; else echo 0; fi)

#  detect if documentation is available
%define include_docs %(if [ "%{config_include_docs}" = yes ]; then echo 1; else echo 0; fi)

#  detect if tools should be included
%define include_tools %(if [ "%{config_include_tools}" = yes ]; then echo 1; else echo 0; fi)


#  kludge to get around rpm <percent>define weirdness
%define ipv6 %(if [ "%{config_ipv6}" = yes ]; then echo --enable-ipv6; else echo --disable-ipv6; fi)
%define pymalloc %(if [ "%{config_pymalloc}" = yes ]; then echo --with-pymalloc; else echo --without-pymalloc; fi)
%define binsuffix %(if [ "%{config_binsuffix}" = none ]; then echo ; else echo "%{config_binsuffix}"; fi)
%define libdirname lib
%define sharedlib %(if [ "%{config_sharedlib}" = yes ]; then echo --enable-shared; else echo ; fi)
%define include_sharedlib %(if [ "%{config_sharedlib}" = yes ]; then echo 1; else echo 0; fi)


##############
#  PREAMBLE  #
##############
Summary: An interpreted, interactive, object-oriented programming language.
Name: %{name}
Version: %{version}
Release: %{release}
License: PSF
Group: Development/Languages
Provides: python-abi = %{libvers}
Provides: python(abi) = %{libvers}
Source: https://www.python.org/ftp/python/%{version}/Python-%{version}.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: gcc make expat-devel db4-devel gdbm-devel sqlite-devel readline-devel zlib-devel bzip2-devel openssl-devel
AutoReq: no
Prefix: %{__prefix}
Vendor: Sean Reifschneider <jafo-rpms@tummy.com>
Packager: Maksim Dogonov <maxim.dogonov@alfatell.ru>

%description
Python is an interpreted, interactive, object-oriented programming
language.  It incorporates modules, exceptions, dynamic typing, very high
level dynamic data types, and classes. Python combines remarkable power
with very clear syntax. It has interfaces to many system calls and
libraries, as well as to various window systems, and is extensible in C or
C++. It is also usable as an extension language for applications that need
a programmable interface.  Finally, Python is portable: it runs on many
brands of UNIX, on PCs under Windows, MS-DOS, and OS/2, and on the
Mac.

%package devel
Summary: The libraries and header files needed for Python extension development.
Requires: %{name} = %{version}-%{release}
Group: Development/Libraries

%description devel
The Python programming language's interpreter can be extended with
dynamically loaded extensions and can be embedded in other programs.
This package contains the header files and libraries needed to do
these types of tasks.

Install python-devel if you want to develop Python extensions.  The
python package will also need to be installed.  You'll probably also
want to install the python-docs package, which contains Python
documentation.

#######
#  PREP
#######
%prep
%setup -n Python-%{version}


########
#  BUILD
########
%build
echo "Setting for ipv6: %{ipv6}"
echo "Setting for pymalloc: %{pymalloc}"
echo "Setting for binsuffix: %{binsuffix}"
echo "Setting for include_tkinter: %{include_tkinter}"
echo "Setting for libdirname: %{libdirname}"
echo "Setting for sharedlib: %{sharedlib}"
echo "Setting for include_sharedlib: %{include_sharedlib}"
./configure --with-signal-module --with-threads %{sharedlib} %{ipv6} %{pymalloc} --prefix=%{__prefix} --with-ensurepip=install
make %{_smp_mflags}


##########
#  INSTALL
##########
%install
#  set the install path
echo '[install_scripts]' >setup.cfg
echo 'install_dir='"${RPM_BUILD_ROOT}%{__prefix}/bin" >>setup.cfg

[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{__prefix}/%{libdirname}/python%{libvers}/lib-dynload
make prefix=$RPM_BUILD_ROOT%{__prefix} altinstall

# Fix permissions
chmod 644 $RPM_BUILD_ROOT%{__prefix}/%{libdirname}/libpython%{libvers}*

########
#  Tools
%if %{include_tools}
cp -a Tools $RPM_BUILD_ROOT%{__prefix}/%{libdirname}/python%{libvers}
install -D -m 644 Tools/gdb/libpython.py $RPM_BUILD_ROOT%{__prefix}/%{libdirname}/debug/usr/bin/python%{libvers}.debug-gdb.py
echo "/usr/lib/debug/usr/bin/python3.6.debug-gdb.py" >> debugfiles.list
%endif

#  MAKE FILE LISTS
rm -f mainpkg.files
find "$RPM_BUILD_ROOT""%{__prefix}"/%{libdirname}/python%{libvers} -type f |
        sed "s|^${RPM_BUILD_ROOT}|/|" | grep -v -e '_tkinter.so$' >mainpkg.files
find "$RPM_BUILD_ROOT""%{__prefix}"/bin -type f -o -type l |
        sed "s|^${RPM_BUILD_ROOT}|/|" |
        grep -v -e '/bin/2to3-%{binsuffix}$' |
        grep -v -e '/bin/pydoc%{binsuffix}$' |
        grep -v -e '/lib//python%{binsuffix}/smtpd.py%{binsuffix}$' |
        grep -v -e '/bin/idle%{binsuffix}$' >>mainpkg.files
echo %{__prefix}/include/python%{libvers}m/pyconfig.h >> mainpkg.files


######
# Fix the #! line in installed files
find "$RPM_BUILD_ROOT" -type f -print0 |
      xargs -0 grep -l /usr/local/bin/python | while read file
do
   FIXFILE="$file"
   sed 's|^#!.*python|#!%{__prefix}/bin/python'"%{binsuffix}"'|' \
         "$FIXFILE" >/tmp/fix-python-path.$$
   cat /tmp/fix-python-path.$$ >"$FIXFILE"
   rm -f /tmp/fix-python-path.$$
done

########
#  CLEAN
########
%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT
rm -f mainpkg.files tools.files

########
#  FILES
########
%files -f mainpkg.files
%defattr(-,root,root)
#%doc Misc/README Misc/cheatsheet Misc/Porting
%doc LICENSE Misc/ACKS Misc/HISTORY Misc/NEWS
%doc %{__prefix}/share/man/man1/python3.6.1.gz

%{__prefix}/%{libdirname}/python%{libvers}/lib-dynload/
%{__prefix}/%{libdirname}/python%{libvers}/lib2to3/tests/data/
%{__prefix}/%{libdirname}/pkgconfig/python-%{libvers}.pc

%attr(755,root,root) %dir %{__prefix}/include/python%{libvers}m
%attr(755,root,root) %dir %{__prefix}/%{libdirname}/python%{libvers}/
%attr(755,root,root) %dir %{__prefix}/%{libdirname}/python%{libvers}/

%if %{include_sharedlib}
%{__prefix}/%{libdirname}/libpython*
%else
%{__prefix}/%{libdirname}/libpython*.a
%endif

# tools
%exclude %{__prefix}/bin/2to3-%{binsuffix}
%exclude %{__prefix}/bin/pydoc%{binsuffix}
%exclude %{__prefix}/lib/python3.6/smtpd.py
%exclude %{__prefix}/bin/idle%{binsuffix}

#tkinter
%if %{include_tkinter}
%defattr(-,root,root)
%{__prefix}/%{libdirname}/python%{libvers}/lib-tk
%{__prefix}/%{libdirname}/python%{libvers}/lib-dynload/_tkinter.so*
%endif
# docs
%if %{include_docs}
%files docs
%defattr(-,root,root)
%{config_htmldir}/*
%endif

%files devel
%defattr(-,root,root)
%{__prefix}/include/python%{libvers}m/*.h
#%{__prefix}/%{libdirname}/python%{libvers}/config