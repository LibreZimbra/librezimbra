#!/bin/bash
# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) Enrico Weigelt, metux IT consult <info@metux.net>

. /opt/zimbra/libexec/zm-util-base.sh

[ "$ZM_MYSQL_DATADIR" ] || ZM_MYSQL_DATADIR="$ZIMBRA_ROOT/db/data"

zm_mbox_mysql_init() {
    zm_service_dir $ZM_MYSQL_DATADIR

    if [ ! -d $ZM_MYSQL_DATADIR/mysql ]; then
        zm_log_info "need to initialize mysql database"
#        zm_runas mysql_install_db --defaults-file=/opt/zimbra/conf/my.cnf --datadir=$ZM_MYSQL_DATADIR
        zm_runas mysql_install_db --user=zimbra --datadir=$ZM_MYSQL_DATADIR
    else
        zm_log_info "mysql already initialized"
    fi
}
