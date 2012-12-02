%define name smeserver-git
%define version 1.0.0
%define release 11
Summary: HTTPS access to centralised Git repositories on SME Server.
Name: %{name}
Version: %{version}
Release: %{release}%{?dist}
Distribution: SME Server
License: GNU GPL version 2
URL: http://www.through-ip.com
Group: SMEserver/addon
Source: smeserver-git-%{version}.tar.gz
Packager: Marco Hess <marco.hess@through-ip.com>
BuildArchitectures: noarch
BuildRoot: /var/tmp/%{name}-%{version}
BuildRequires: e-smith-devtools
Requires: e-smith-release >= 8.0
Requires: git
AutoReqProv: no

%description
smeserver-git enables centralised git repositories on an SME server and enables 
access to these repositories through HTTP/HTTPS. Repositories are created and
managed through a server-manager panel that also configures the access permissions
to the repositories based on the existing SME users and groups. The package
installes and enables the git server on the current host like in
host.com/git. Repositories are then available as https://host.com/git/gitrepo.git.

%changelog
* Sat Jul 21 2012 Marco Hess <marco.hess@through-ip.com> 1.0.0-3
- Ensure git database is present in /home/e-smith/db
- Create default config database entries for 'git'
- Moved retrieving maxNameLength for panel validations from config 'git'
- In the user and group list boxes, added support to the special group admin
  and shared to allow either the admin or everybody to be included in the access lists.
- Updated the HTTP config db error messages to be more clear as to which property needs
  to be configured.  
  
* Sun Jun 17 2012 Jonathan Martens <smeserver-contribs@snetram.nl> 1.0.0-2
- Rip out gitweb and create tgz file

* Sun Apr 29 2012 Marco Hess <marco.hess@through-ip.com> 1.0.0-1
- initial release

%prep
%setup
mkdir -p root/home/e-smith/files/git/
true

%build
perl createlinks
true 

%install
rm -rf $RPM_BUILD_ROOT
(cd root   ; find . -depth -print | cpio -dump $RPM_BUILD_ROOT)
rm -f %{name}-%{version}-filelist
/sbin/e-smith/genfilelist $RPM_BUILD_ROOT > %{name}-%{version}-filelist
true

%clean
rm -rf $RPM_BUILD_ROOT
true

%post

echo "--------------------------------------------------------------------------------------------"

echo "Setting up git repositories configuration database ..."
touch /home/e-smith/files/git

echo "Setting up git repositories root directory ..."
mkdir -p /home/e-smith/files/git
chown admin:www /home/e-smith/files/git
chmod 770 /home/e-smith/files/git
chmod g+s /home/e-smith/files/git

echo "Rebuilding server-manager ..."
/sbin/e-smith/expand-template /etc/httpd/conf/httpd.conf
/etc/e-smith/events/actions/navigation-conf
/etc/rc7.d/S86httpd-e-smith sighup

echo "--------------------------------------------------------------------------------------------"

%postun

echo "--------------------------------------------------------------------------------------------"

echo "smeserver-git has been removed but the git repositories and the git config database are left in place ..."
echo "To remove the git repositories, use: 'rm -rf /home/e-smith/files/git'"
echo "To remove the git config database, use: 'rm -rf /home/e-smith/db/git'"

echo "--------------------------------------------------------------------------------------------"

echo "Rebuilding server-manager ..."
/sbin/e-smith/expand-template /etc/httpd/conf/httpd.conf
/etc/e-smith/events/actions/navigation-conf
/etc/rc7.d/S86httpd-e-smith sighup

%files -f %{name}-%{version}-filelist
%defattr(-,root,root)
