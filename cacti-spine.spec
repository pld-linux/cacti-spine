Summary:	A backend data gatherer for cacti
Summary(pl.UTF-8):	Backend gromadzący dane dla cacti
Name:		cacti-spine
Version:	0.8.7a
Release:	3
License:	GPL
Group:		Applications
Source0:	http://www.cacti.net/downloads/spine/%{name}-%{version}.tar.gz
# Source0-md5:	85a32d256c056a3a4adb8bf3dff5e2dc
URL:		http://www.cacti.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	mysql-devel
BuildRequires:	net-snmp-devel
BuildRequires:	openssl-devel
BuildRequires:	zlib-devel
%requires_eq_to	net-snmp-libs
Requires:	cacti
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%configure \
	--with-mysql \
	--with-snmp=%{_prefix}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install spine.conf $RPM_BUILD_ROOT%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/*
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/spine.conf
