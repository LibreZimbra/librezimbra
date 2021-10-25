#!/bin/bash
# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) Enrico Weigelt, metux IT consult <info@metux.net>

set -m

ZM_LDAP_LOGLEVEL="sync"

. /opt/zimbra/libexec/zm-ldap-util.sh

read_tag() {
    local tag="$1"
    if [ -f /conf/$tag ]; then
        cat /conf/$tag
    fi
}

copy_certs() {
    zm_ldap_install_ca /conf/ca/*.pem
    zm_ldap_install_keys /conf/slapd.crt /conf/slapd.key
}

start_master() {
    if ! zm_ldap_start_wait ; then
        echo "falling back to shell"
        bash
    fi
    zm_ldap_set_serverid `read_tag server-id`
    update_masters
}

start_primary() {
    start_master
    zm_ldap_load_initdata `read_tag ldap-replication-password`
    zm_ldap_setpass $ZM_LDAP_ZIMBRA_DN `read_tag ldap-zimbra-password`
}

start_slave() {
    zm_log_err "start_slave not implemented yet"
    exit 1
}

update_masters() {
    local myself=`read_tag node-name`
    local bindpw=`read_tag ldap-replication-password`
    local masters=`read_tag ldap-masters`

    zm_configure_mmr \
        "$myself" \
        "$bindpw" \
        $masters

    return $?
}

zm_ldap_init
copy_certs

node_name=`read_tag node-name`
node_type=`read_tag node-type`
zm_log_info "node type: $node_type"
case "$node_type" in
    ldap-primary)
        start_primary
    ;;
    ldap-master)
        start_master
    ;;
    ldap-slave)
        start_slave
    ;;
esac

zm_ldap_createserver "$node_name"

zm_log_info "reattaching to slapd"
fg
