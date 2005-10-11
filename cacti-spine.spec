Summary:	A backend data gatherer for cacti
Name:		cacti-cactid
Version:	0.8.6f
Release:	0.1
License:	GPL
Group:		Applications
Source0:	http://www.cacti.net/downloads/cactid/%{name}-%{version}.tar.gz
# Source0-md5:	2b102f9029ffaa4fb0e186c6640b1851
URL:		http://www.cacti.net/
BuildRequires:	automake
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
install /usr/share/automake/config.* config
%configure \
	--with-mysql \
	--with-snmp=%{_prefix}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install cactid.conf $RPM_BUILD_ROOT%{_sysconfdir}

cat  << EOF > $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/%{name}
*/5 * * * * nobody umask 022; /usr/bin/cactid > /dev/null 2>&1
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG README
%attr(755,root,root) %{_bindir}/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cactid.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/cron.d/%{name}
