# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) Enrico Weigelt, metux IT consult <info@metux.net>

FROM librezimbra-test-base

COPY files/Release /tmp
RUN apt-get update && \
    apt-get install -y zimbra-store uuid zimbra-openldap-client zimbra-mbox-webclient-war rsyslog

EXPOSE 8080/tcp
ENTRYPOINT "/entrypoint.sh"

COPY files/zm-jetty /
COPY files/rsyslog.conf /etc
COPY files/zm-mbox-util.sh /opt/zimbra/libexec
COPY files/entrypoint.sh /
COPY files/my.cnf /opt/zimbra/conf
COPY files/zm-mbox-mysql-init /opt/zimbra/libexec
COPY files/zm-mbox-mysql-start /opt/zimbra/libexec
