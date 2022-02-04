# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) Enrico Weigelt, metux IT consult <info@metux.net>

FROM librezimbra-test-base

COPY files/Release /tmp
RUN apt-get update && \
    apt-get install -y zimbra-store uuid zimbra-openldap-client rsyslog

EXPOSE 8080/tcp
ENTRYPOINT "/entrypoint.sh"

COPY files/zm-jetty /
COPY files/rsyslog.conf /etc
COPY files/zm-mbox-util.sh /opt/zimbra/libexec
COPY files/entrypoint.sh /
