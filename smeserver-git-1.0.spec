%define name smeserver-git
%define version 1.0.0
%define release 39
Summary: Centralised Git repositories with setup and configuration through SME Server admin panels.
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
installs and enables the git server on the current host like in
host.com/git. Repositories are then available as https://host.com/git/gitrepo.git.

%changelog
* Tue Feb 2 2015 Marco Hess <marco.hess@through-ip.com> 1.0.0-38
- Backport changes from 1.1.

* Fri May 30 2014 Marco Hess <marco.hess@through-ip.com> 1.0.0-37
- Fixed the HTTPS redirection loop. HTTPS redirection is now only done on the HTTP part of of
  the web server configuration and the full Git configuration part is only done in the HTTPS
  section.

* Tue May 27 2014 Marco Hess <marco.hess@through-ip.com> 1.0.0-36
- Changed how git update-server-info is run as the location of the executable changed in git 1.8.

* Fri Jan 24 2014 Marco Hess <marco.hess@through-ip.com> 1.0.0-35
- Systax error in 29GitRepositories that I though I fixed.

* Fri Jan 24 2014 Marco Hess <marco.hess@through-ip.com> 1.0.0-34
- git version 1.8 has shifted the location of some executables. Modified the scripts
  to test on these locations so we generate the right paths.
  
* Sun May 21 2013 Marco Hess <marco.hess@through-ip.com> 1.0.0-33
- Set permissions on git repository databaase for GitWeb access also on upgrade install.
  
* Sun May 21 2013 Marco Hess <marco.hess@through-ip.com> 1.0.0-32
- Fixed a problem in the repository delete script where File::Path is needed
  to reference rmtree.
- Also cleanup the entry from the database so that repositories of the same 
  name can be created again.

* Sun May 21 2013 Marco Hess <marco.hess@through-ip.com> 1.0.0-31
- Changed the repository-delete script to ensure the SME Git database 
  permissions are Ok for use by GitWeb after a delete.
- Ensure that on 64-bit systems we use /usr/lib64/httpd/modules/pwauth
  
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

%build
perl createlinks

%install
rm -rf $RPM_BUILD_ROOT
(cd root   ; find . -depth -print | cpio -dump $RPM_BUILD_ROOT)
rm -f %{name}-%{version}-filelist
/sbin/e-smith/genfilelist $RPM_BUILD_ROOT > %{name}-%{version}-filelist

%clean
rm -rf $RPM_BUILD_ROOT

%post
echo "---------------------------------------------------------"
if [ $1 -eq 1 ] ; then
  echo "Initial installation:"
  echo " - Ensuring git repositories configuration database exist ..."
  touch /home/e-smith/db/git
  echo " - Ensuring git repositories root directory exist with the right permissions ..."
  mkdir -p /home/e-smith/files/git
  chmod 770 /home/e-smith/files/git
  chmod g+s /home/e-smith/files/git
  echo " - Rebuilding server-manager ..."
  /sbin/e-smith/expand-template /etc/httpd/conf/httpd.conf
  /etc/e-smith/events/actions/navigation-conf
fi
echo " - Ensuring git repositories configuration database has the right permissions ..."
chmod 664 /home/e-smith/db/git
chown admin:www /home/e-smith/files/git
/etc/rc7.d/S86httpd-e-smith sighup
echo "---------------------------------------------------------"

%postun
if [ $1 -eq 0 ] ; then
  echo "---------------------------------------------------------"
  echo " - Rebuilding server-manager ..."
  /sbin/e-smith/expand-template /etc/httpd/conf/httpd.conf
  /etc/e-smith/events/actions/navigation-conf
  echo " - Final Uninstall:"
  echo "  smeserver-git has been removed but the git repositories and the git config database are left in place ..."
  echo "  To manually remove the git repositories, use: 'rm -rf /home/e-smith/files/git'"
  echo "  To manually remove the git config database, use: 'rm -rf /home/e-smith/db/git'"
  echo "---------------------------------------------------------"
fi

%files -f %{name}-%{version}-filelist
%defattr(-,root,root)
