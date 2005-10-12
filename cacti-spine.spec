Summary:	A backend data gatherer for cacti
Summary(pl):	Backend gromadz±cy dane dla cacti
Name:		cacti-cactid
Version:	0.8.6f
Release:	1
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
Requires:	cacti
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A backend data gatherer for cacti. This package represents the future
replacement for cacti's cmd.php. It is almost 100% compatible with the
legacy cmd.php processor.

%description -l pl
Backend gromadz±cy dane dla cacti. Ten pakiet reprezentuje przysz³y
zamiennik cmd.php z cacti. Jest prawie w 100% kompatybilny ze starym
procesorem cmd.php.

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
install -d $RPM_BUILD_ROOT%{_sysconfdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install cactid.conf $RPM_BUILD_ROOT%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG README
%attr(755,root,root) %{_bindir}/*
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cactid.conf
