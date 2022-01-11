#!/bin/bash
# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) Enrico Weigelt, metux IT consult <info@metux.net>

set -m

. /opt/zimbra/libexec/zm-mbox-util.sh

## fixme:

read_tag() {
    local tag="$1"
    if [ -f /conf/$tag ]; then
        cat /conf/$tag
    fi
}

copy_certs() {
    zm_ldap_install_ca /conf/ca/*.pem
}

mk_ldap_url() {
    needspace=""
    while [ "$1" ]; do
        [ "$needspace" ] && echo -n " "
        echo -n "ldap://$1"
        needspace=1
        shift
    done
}

#copy_certs

node_name=`read_tag node-name`
node_type=`read_tag node-type`

ldap_masters=`read_tag ldap-masters`
ldap_readonly=`read_tag ldap-readonly`

zm_log_info "ldap masters: $ldap_masters"
zm_log_info "ldap_readonly: $ldap_readonly"

if [ ! "$ldap_readonly" ]; then
    zm_log_info "no readonly ldap nodes specified. using masters"
    ldap_readonly="$ldap_masters"
fi

zm_localconfig_set ldap_master_url `mk_ldap_url $ldap_masters`
zm_localconfig_set ldap_url `mk_ldap_url $ldap_readonly`
zm_localconfig_set zimbra_server_hostname "$node_name"
zm_localconfig_set zimbra_ldap_password `read_tag ldap-zimbra-password`

# need to reload localconfig
. $ZIMBRA_ROOT/libexec/zm-load-localconfig.sh

# tempdir for jython
zm_init_datatmp
zm_mbox_createserver "$node_name"

/etc/init.d/rsyslog start

zm_log_info "running zmconfigd"
su - $ZIMBRA_USER -c "$ZIMBRA_ROOT/libexec/zmconfigd"

echo "falling back to interactive shell"
bash