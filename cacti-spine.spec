Summary:	A backend data gatherer for cacti
Summary(pl.UTF-8):	Backend gromadzący dane dla cacti
Name:		cacti-spine
Version:	0.8.7g
Release:	2
License:	GPL
Group:		Applications
Source0:	http://www.cacti.net/downloads/spine/%{name}-%{version}.tar.gz
# Source0-md5:	22c2b1986c880b9c587876c18d5c3f9f
Patch0:		%{name}-paths.patch
URL:		http://www.cacti.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	mysql-devel
BuildRequires:	net-snmp-devel
BuildRequires:	openssl-devel
BuildRequires:	rpmbuild(macros) >= 1.502
BuildRequires:	zlib-devel
%requires_eq	net-snmp-libs
Requires:	cacti
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		cacti
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_bindir		%{_sbindir}

%description
A backend data gatherer for cacti. This package represents the future
replacement for cacti's cmd.php. It is almost 100% compatible with the
legacy cmd.php processor.

%description -l pl.UTF-8
Backend gromadzący dane dla cacti. Ten pakiet reprezentuje przyszły
zamiennik cmd.php z cacti. Jest prawie w 100% kompatybilny ze starym
procesorem cmd.php.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__automake}
%{__autoconf}
chmod +x ./configure
%configure \
	--with-results-buffer=4096 \
	--with-mysql \
	--with-snmp=%{_prefix}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_sbindir}/{spine,cacti-poller-spine}
mv $RPM_BUILD_ROOT%{_sysconfdir}/spine.conf{.dist,}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/spine.conf
%attr(755,root,root) %{_sbindir}/cacti-poller-spine
