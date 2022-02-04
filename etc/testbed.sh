# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) Enrico Weigelt, metux IT consult <info@metux.net>

set -e

TESTBED_MYSELF=$(readlink -f "$0")
TESTBED_WORK_DIR=$(dirname "$TESTBED_MYSELF")

[ "$TESTBED_NETWORK" ]      || TESTBED_NETWORK="librezimbra-testnet"
[ "$TESTBED_NODE_CONFDIR" ] || TESTBED_NODE_CONFDIR="$TESTBED_WORK_DIR/tmp/conf/$TESTBED_NODE_NAME"
[ "$TESTBED_NODE_DATADIR" ] || TESTBED_NODE_DATADIR="$TESTBED_WORK_DIR/tmp/data/$TESTBED_NODE_NAME"

testbed_createnet() {
    docker network create "$TESTBED_NETWORK"
}

testbed_genkeys() {
    ( cd etc && ./generate-tls-keys HOSTS=$TESTBED_NODE_NAME) || exit 1
}

testbed_cf_ca() {
    mkdir -p $TESTBED_NODE_CONFDIR/ca
    cp tmp/ca/ca.pem $TESTBED_NODE_CONFDIR/ca
}

testbed_write_tag() {
    local tag="$1"
    shift
    mkdir -p "$TESTBED_NODE_CONFDIR"
    echo "$*" > "$TESTBED_NODE_CONFDIR/$tag"
}

testbed_conffile() {
    local target="$1"
    local src="$2"
    mkdir -p "$TESTBED_NODE_CONFDIR"
    cp "$src" "$TESTBED_NODE_CONFDIR/$target"
    return $?
}

testbed_cf_ldap() {
    testbed_genkeys
    testbed_cf_ca
    testbed_conffile slapd.crt tmp/ca/host-$TESTBED_NODE_NAME.crt
    testbed_conffile slapd.key tmp/ca/host-$TESTBED_NODE_NAME.key
    testbed_write_tag "node-type"    "$TESTBED_NODE_TYPE"
    testbed_write_tag "ldap-masters" "$TESTBED_LDAP_MASTERS"
    testbed_write_tag "node-name"    "$TESTBED_NODE_NAME"
    testbed_write_tag "ldap-replication-password" "$TESTBED_LDAP_REPLICATION_PASSWORD"
    testbed_write_tag "ldap-zimbra-password"      "$TESTBED_LDAP_ZIMBRA_PASSWORD"
    [ "$TESTBED_NODE_ID" ] && testbed_write_tag "server-id" "$TESTBED_NODE_ID"
}

testbed_start_ldap() {
    make image-librezimbra-test-ldap || exit 1

    testbed_cf_ldap
    testbed_createnet || true
    cp tmp/ca/host-$TESTBED_NODE_NAME.crt $TESTBED
    mkdir -p $TESTBED_NODE_DATADIR
    docker run --rm --privileged -it \
        --hostname "$TESTBED_NODE_NAME" \
        --network "$TESTBED_NETWORK" \
        --name "$TESTBED_NODE_NAME" \
        --mount "src=$TESTBED_NODE_CONFDIR,target=/conf,type=bind,ro" \
        --mount "src=$TESTBED_NODE_DATADIR,target=/opt/zimbra/data/ldap,type=bind" \
        $TESTBED_NODE_DOCKER_OPT \
        librezimbra-test-ldap $CMD "$@"
}

testbed_cf_mbox() {
    testbed_genkeys
    testbed_cf_ca
    testbed_conffile mailboxd.crt tmp/ca/host-$TESTBED_NODE_NAME.crt
    testbed_conffile mailboxd.key tmp/ca/host-$TESTBED_NODE_NAME.key
    testbed_conffile mailboxd.p12 tmp/ca/host-$TESTBED_NODE_NAME.p12
    testbed_write_tag "node-name"               "$TESTBED_NODE_NAME"
    testbed_write_tag "node-type"               "$TESTBED_NODE_TYPE"
    testbed_write_tag "ldap-masters"            "$TESTBED_LDAP_MASTERS"
    testbed_write_tag "ldap-readonly"           "$TESTBED_LDAP_READONLY"
    testbed_write_tag "ldap-zimbra-password"    "$TESTBED_LDAP_ZIMBRA_PASSWORD"
}

testbed_start_mbox() {
    make image-librezimbra-test-mbox || exit 1

    testbed_cf_mbox
    testbed_createnet || true
    mkdir -p $TESTBED_NODE_DATADIR
    docker run --rm --privileged -it \
        --hostname "$TESTBED_NODE_NAME" \
        --network "$TESTBED_NETWORK" \
        --name "$TESTBED_NODE_NAME" \
        --mount "src=$TESTBED_NODE_CONFDIR,target=/conf,type=bind,ro" \
        --mount "src=$TESTBED_NODE_DATADIR,target=/opt/zimbra/data,type=bind" \
        $TESTBED_NODE_DOCKER_OPT \
        librezimbra-test-mbox $CMD "$@"
}
