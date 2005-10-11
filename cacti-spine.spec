Summary:	A backend data gatherer for cacti
Name:		cacti-cactid
Version:	0.8.6f
Release:	0.1
License:	GPL
Group:		Applications
Source0:	http://www.cacti.net/downloads/cactid/%{name}-%{version}.tar.gz
# Source0-md5:	2b102f9029ffaa4fb0e186c6640b1851
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://www.cacti.net/
BuildRequires:	mysql-devel
BuildRequires:	net-snmp-devel
BuildRequires:	openssl-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A backend data gatherer for cacti. This package represents the future
replacement for cacti's cmd.php. It is almost 100% compatible with the
legacy cmd.php processor.

%prep
%setup -q

%build
%configure \
	--with-mysql \
	--with-snmp=%{_prefix}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{rc.d/init.d,sysconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install cactid.conf $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/cactid
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/cactid

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add cactid
if [ -f /var/lock/subsys/cactid ]; then
        /etc/rc.d/init.d/cactid restart 1>&2
else
        echo "Run \"/etc/rc.d/init.d/cactid start\" to start cactid daemon."
fi

%preun
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/cactid ]; then
                /etc/rc.d/init.d/cactid stop 1>&2
        fi
        /sbin/chkconfig --del cactid
fi


%files
%defattr(644,root,root,755)
%doc CHANGELOG README
%attr(755,root,root) %{_bindir}/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cactid.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sysconfig/cactid
%attr(754,root,root) /etc/rc.d/init.d/cactid
