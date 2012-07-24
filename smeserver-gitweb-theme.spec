%define name smeserver-gitweb-theme
%define version 1.0.0
%define release 3
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
Requires: e-smith-release >= 8.0
Requires: smeserver-gitweb
AutoReqProv: no

%description
Optional package for use with smeserver-gitweb to enable a more GitHub inspired
theme for gitweb. Based on http://kogakure.github.com/gitweb-theme/

%changelog
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

%files -f %{name}-%{version}-filelist
%defattr(-,root,root)
