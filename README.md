SME Server GitWeb
-----------------

This package adds the gitweb viewer to an SME Server git installation.

While the HTTP configuration for this gitweb is done in the smeserver-git
package, this one adds SME Server template handling for the gitweb configuration
with the following features:

* Many gitweb.conf configuration items configured with sensible defaults pulled from 
  the local system configuration e.g. $projectroot, $homelink, $home_text, $base_url, etc.
* Highlight package installed and enabled for colorised code viewing.
* Local users will be able to view all repositories.
* Unauthenticated internet users will only be able to see 'internet' repositories that have anonymous pull access.
* Authenticated internet users will be able to see 'internet' repositories for which they have pull access.

Required Packages
-----------------
* smeserver-git <https://github.com/MarcoHess/smeserver-git/tree/smeserver-git>

Optional Packages
-----------------
* smeserver-gitweb-theme <https://github.com/MarcoHess/smeserver-git/tree/smeserver-gitweb-theme>
