#
# Conditional build:
%bcond_without	cap	# Linux Capabilities support

Summary:	A backend data gatherer for Cacti
Summary(pl.UTF-8):	Backend gromadzący dane dla Cacti
Name:		cacti-spine
Version:	1.2.30
Release:	1
License:	GPL
Group:		Daemons
Source0:	https://files.cacti.net/spine/%{name}-%{version}.tar.gz
# Source0-md5:	249ca44c5a7863a2b5fcd382c8a77055
Patch0:		%{name}-paths.patch
# Official patches http://www.cacti.net/spine_download_patches.php
URL:		http://www.cacti.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	help2man
%{?with_cap:BuildRequires:	libcap-devel}
BuildRequires:	libtool
BuildRequires:	mysql-devel
BuildRequires:	net-snmp-devel
BuildRequires:	openssl-devel
BuildRequires:	rpmbuild(macros) >= 1.502
BuildRequires:	zlib-devel
%requires_eq	net-snmp-libs
Requires:	cacti
Obsoletes:	cacti-cactid < 0.8.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		cacti
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_bindir		%{_sbindir}

%description
A backend data gatherer for Cacti. This package represents the future
replacement for Cacti's cmd.php. It is almost 100% compatible with the
legacy cmd.php processor.

%description -l pl.UTF-8
Backend gromadzący dane dla Cacti. Ten pakiet reprezentuje przyszły
zamiennik cmd.php z Cacti. Jest prawie w 100% kompatybilny ze starym
procesorem cmd.php.

%prep
%setup -q
%patch -P0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoheader}
%{__automake}
%{__autoconf}
chmod +x ./configure
%configure \
	--with-results-buffer=4096 \
	--with-mysql \
	%{__enable_disable cap lcap} \
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
%doc README.md
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/spine.conf
%attr(755,root,root) %{_sbindir}/cacti-poller-spine
%{_mandir}/man1/spine.1*
