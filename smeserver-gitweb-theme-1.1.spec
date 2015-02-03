%define name smeserver-gitweb-theme
%define version 1.1.0
%define release 0
Summary: GitHub inspired look and feel for smeserver-gitweb
Name: %{name}
Version: %{version}
Release: %{release}%{?dist}
Distribution: SME Server
License: GNU GPL version 2
URL: http://www.through-ip.com
Group: SMEserver/addon
Source: smeserver-gitweb-theme-%{version}.tar.gz
Packager: Marco Hess <marco.hess@through-ip.com>
BuildArchitectures: noarch
BuildRoot: /var/tmp/%{name}-%{version}
BuildRequires: e-smith-devtools
Requires: e-smith-release >= 9.0
Requires: smeserver-gitweb
AutoReqProv: no

%description
Optional package for use with smeserver-gitweb to enable a more GitHub inspired
theme for gitweb. Based on http://kogakure.github.com/gitweb-theme/

%changelog
* Fri Jan 30 2015 Marco Hess <marco.hess@through-ip.com> 1.1.0-0
- Package rebuild for SME9
- Updated to latest CSS for gitweb-theme.
- Updated icons to latest git types.
- Removed own gitweb.js

* Mon Jul 23 2012 Marco Hess <marco.hess@through-ip.com> 1.0.0-3
- initial release

%prep
%setup
%build

%install
rm -rf $RPM_BUILD_ROOT
(cd root   ; find . -depth -print | cpio -dump $RPM_BUILD_ROOT)
rm -f %{name}-%{version}-filelist
/sbin/e-smith/genfilelist $RPM_BUILD_ROOT > %{name}-%{version}-filelist

%clean
rm -rf $RPM_BUILD_ROOT

%post
echo "Expanding gitweb.conf template ..."
/sbin/e-smith/expand-template /etc/gitweb.conf
echo "Expanding web server template ..."
/sbin/e-smith/expand-template /etc/httpd/conf/httpd.conf
/etc/rc7.d/S86httpd-e-smith sighup

%files -f %{name}-%{version}-filelist
%defattr(-,root,root)
