#----------------------------------------------------------------------
#
# Copyright (C) 2012-2015 - Marco Hess <marco.hess@through-ip.com>
#
# This file is part of the "Git Repositories" panel in the
# SME Server server-manager panel to configure git repositories.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA
#----------------------------------------------------------------------

package esmith::GitDB;

use strict;
use warnings;
use esmith::db;
use esmith::AccountsDB;

use vars qw( $AUTOLOAD @ISA );

use esmith::DB::db;
@ISA = qw(esmith::DB::db);

=head1 NAME

esmith::GitDB - interface to the Git repositories database

=head1 SYNOPSIS

  use esmith::GitDB;
  my $g = esmith::GitDB->open;

  my @repos = $g->repositories();

=head1 DESCRIPTION

This module provides an abstracted interface to the Git repositiries
database. The Git repositories are maintained in a separate database
so the Git repositories have their own name space and won't clash
with the accounts database entries such as ibays, pseudonyms and users.

=cut

our $VERSION = sprintf '%d.%03d', q$Revision: 1.0 $ =~ /: (\d+).(\d+)/;

=head2 open()

Loads an existing git database and returns an esmith::GitDB
object representing it.

=cut

sub open {
  my($class, $file) = @_;
  $file = $file || $ENV{ESMITH_GIT_DB} || "git";
  return $class->SUPER::open($file);
}

sub open_ro {
  my($class, $file) = @_;
  $file = $file || $ENV{ESMITH_GIT_DB} || "git";
  return $class->SUPER::open_ro($file);
}

sub AUTOLOAD {
  my $self = shift;
  my ($called_sub_name) = ($AUTOLOAD =~ m/([^:]*)$/);
  my @types = qw( repositories );
  if( grep /^$called_sub_name$/, @types ) {
    $called_sub_name =~ s/s$//g;    # de-pluralize
    return $self->get_all_by_prop(type => qw( repository ));
  }
}

#----------------------------------------------------------------------

### Generate an effective users list from them given list of
### groups and users where groups are expanded in their list
### of members. Members from groups are assumed to valid
### members. Individual users are validated to be an active
### system user. In case there are groups and user defined
### but we end up with an empty list of users, 'admin' is 
### added to prevent an empty list and thus prevent unintentional
### Anonymous access to the git repository.
sub effective_users_list_from {
  my( $class, $groups1, $users1, $groups2, $users2 ) = @_;

  ### Generate effective list of users from the groups and individual users combined ### 
  my @effective_users_list;

  ### Open the accounts database
  my $accounts_db = esmith::AccountsDB->open_ro()
    or die( "Failed to open Accounts database : $!. The database file may not be readable by this user.\n" );

  ### Get the list of active system users so we can validate
  ### the git users against this list.
  my @active_system_users = $accounts_db->activeUsers();
  
  ### Collect users listed for the named groups
  if( $groups1 || $groups2 ) {
    my @groups;
    if( $groups1 ) {
      push @groups, split ( /,/, $groups1 );
    }
    if( $groups2 ) {
      push @groups, split ( /,/, $groups2 );
    }
      
    foreach my $group ( @groups ) {
      if( $group eq 'admin' ) {
        push @effective_users_list, 'admin';
      } elsif( $group eq 'shared' ) {
        push @effective_users_list, $_->key foreach( @active_system_users );
      } else {
        my $record = $accounts_db->get( $group );
        if( $record ) {
          my $members = $record->prop( 'Members' ) || "";
          if( length($members) > 0 ) {
            push @effective_users_list, split( /,/, $members );
          }
        }
        undef $record;
      }
    }
    
    ### When we reach here and there are no effective users even though
    ### one or more groups were defined, we need to prevent that we 
    ### unintentionally allow Anonymous access to the repository.
    ### So we push the 'admin' user as an effective user. This 
    ### prevents the http.conf script allowing anonymous access.
    unless( @effective_users_list ) {
      push @effective_users_list, 'admin';      
    }
  }

  ### Combine individual users into the list generated so far
  ### Ensure that the user is an active SME user as the user
  ### could have been disabled or deleted.
  if( $users1 || $users2 ) {
    if( $users1 ) {
      foreach my $user ( split ( /,/, $users1 ) ) {
        if( grep( /^$user$/, @active_system_users ) ) {      
          push @effective_users_list, $user;
        }
      }
    }
    if( $users2 ) {
      foreach my $user ( split ( /,/, $users2 ) ) {
        if( grep( /^$user$/, @active_system_users ) ) {      
          push @effective_users_list, $user;
        }
      }
    }
    
    ### Again, when we reach here and there are still no effective 
    ### users even though some users were specified, we need to 
    ### prevent unintentionally Anonymous access to the repository
    ### and we push the 'admin' user as a minimum effective user.
    unless( @effective_users_list ) {
      push @effective_users_list, 'admin';      
    }
  }

  ### When there is more than one entry, sort it
  if( @effective_users_list > 1 ) {
    @effective_users_list = sort( @effective_users_list );
  }

  ### Ensure we only have unique entries
  my $effective_users_list;
  my $prev = '';
  @effective_users_list = grep( $_ ne $prev && (($prev) = $_), @effective_users_list );
  $effective_users_list = join( " ", @effective_users_list ) || '';
  undef @effective_users_list;

  return $effective_users_list;
}

#----------------------------------------------------------------------
