# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) Enrico Weigelt, metux IT consult <info@metux.net>

. /opt/zimbra/libexec/zm-util-base.sh
. /opt/zimbra/libexec/zm-load-localconfig.sh

zm_ldapadd() {
    for url in $ldap_master_url ; do
        zm_log_info "$0: trying ldap master: $url"
        $ZM_LDAP_BINDIR/ldapadd -D "$zimbra_ldap_userdn" -w "$zimbra_ldap_password" -Q -H "$url" "$@"
        # fixme: check whether we reached him
        return $?
    done
}

zm_ldapsearch() {
    for url in $ldap_master_url ; do
        zm_log_info "$0: trying ldap master: $url"
        $ZM_LDAP_BINDIR/ldapsearch -D "$zimbra_ldap_userdn" -w "$zimbra_ldap_password" -H "$url" "$@"
        # fixme: check whether we reached him
        return $?
    done
}

zm_ldapmodify() {
    for url in $ldap_master_url ; do
        zm_log_info "$0: trying ldap master: $url"
        $ZM_LDAP_BINDIR/ldapmodify -D "$zimbra_ldap_userdn" -w "$zimbra_ldap_password" -H "$url" "$@"
        return $?
    done
}

#zm_ldap_check_obj_oc() {
#    local basedn="$1"
#    local oc="$2"
#
#    zm_ldapsearch -b "$basedn" "(objectclass=$oc)" dn 2>/dev/null | \
#        grep "dn: $basedn" >/dev/null
#    return $?
#}

#zm_ldap_install_ca() {
#    mkdir -p "$ZM_CA_DIR"
#    cp "$@" "$ZM_CA_DIR"
#    chown -R "$ZM_LDAP_USER:$ZM_LDAP_GROUP" "$ZM_CA_DIR"
#}

zm_mbox_createserver() {
    local nodename="$1"
    zm_server_create "$nodename"
    zm_server_enable_service "$nodename" "mailbox"
}
