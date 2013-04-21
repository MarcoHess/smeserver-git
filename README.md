SME Server Git
--------------

This package installs Git on an SME Server and configures it to be used as 
a centralised git repository with the following features:

* Git repository access through HTTPS so it is easy to allow access from
  the internet connection.
* Network Access configurable per repository for local network only or internet.
* User Access setup per repository based around SME Server users and groups
  while also allowing Anonymous access.
* Separate access permissions for PULL and PUSH access.
* Automatic email notification configuration for Git repository updates based
  on the combined PULL & PUSH User Access list.
* All Git repository creation and user access setup through SME server-manager panel.
* Configured to operate as separate local host/subdomain 'git' on your domain so 
  repository names don't confict with ibay names or other accounts on SME Server.
* Repository file permissions setup admin;www to allow web server access for 3rd party
  repository viewers e.g. Redmine.
* Optionally install the gitweb viewer for the git repositories.

Optional Packages
-----------------
* smeserver-gitweb <https://github.com/MarcoHess/smeserver-git/tree/smeserver-gitweb>
* smeserver-gitweb-theme <https://github.com/MarcoHess/smeserver-git/tree/smeserver-gitweb-theme>

Iassues/Bugs
------------
* After delete of a repository, the Git database (/home/e-smith/db/git) 
  becomes unreadable. It needs chmod a+r to be readable by the web server.
* Error messages about unreadble Git database it Gitweb could be improved.
* GitWeb home URl does not work when the name can not be resolved. Needs an option
  to set to IP address instead.
