%define name smeserver-gitweb
%define version 1.0.0
%define release 12
Summary: GitWeb is a web based Git repository viewer on SME Server
Name: %{name}
Version: %{version}
Release: %{release}%{?dist}
Distribution: SME Server
License: GNU GPL version 2
URL: http://www.through-ip.com
Group: SMEserver/addon
Source: smeserver-gitweb-%{version}.tar.gz
Packager: Marco Hess <marco.hess@through-ip.com>
BuildArchitectures: noarch
BuildRoot: /var/tmp/%{name}-%{version}
BuildRequires: e-smith-devtools
Requires: e-smith-release >= 8.0
Requires: smeserver-git
Requires: gitweb
Requires: highlight
AutoReqProv: no

%description
HTTP access to https://git.host.com provides a gitweb view of the repositories.

%changelog
* Fri Jan 24 2014 Marco Hess <marco.hess@through-ip.com> 1.0.0-12
- Added support for displaying a clone URL.

* Mon Jul 23 2012 Marco Hess <marco.hess@through-ip.com> 1.0.0-3
- Setup default config parameters for gitweb as a service
- Removed HTTP template as this is shared with smeserver-git
- Added require on gitweb rpm

* Sun Jun 17 2012 Jonathan Martens <smeserver-contribs@snetram.nl> 1.0.0-2
- Remove all smeserver-git related files in order to split the packages

* Sun Apr 29 2012 Marco Hess <marco.hess@through-ip.com> 1.0.0-1
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
echo "Ensuring git database is accessible to GitWeb ..."
touch /home/e-smith/db/git
chmod 644 /home/e-smith/db/git
echo "Ensuring networks database is accessible to GitWeb ..."
chmod 644 /home/e-smith/db/networks
echo "Expanding gitweb.conf template ..."
/sbin/e-smith/expand-template /etc/gitweb.conf
echo "Expanding GitWeb home page text template ..."
/sbin/e-smith/expand-template /etc/e-smith/web/common/gitweb/home_text.html
echo "Expanding web server template ..."
/sbin/e-smith/expand-template /etc/httpd/conf/httpd.conf
/etc/rc7.d/S86httpd-e-smith sighup

%files -f %{name}-%{version}-filelist
%defattr(-,root,root)
