# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) Enrico Weigelt, metux IT consult <info@metux.net>

FROM librezimbra-test-base

COPY files/Release /tmp
RUN apt-get update && \
    apt-get install -y zimbra-ldap zimbra-openldap-client-dbg \
                       zimbra-openldap-lib-dbg zimbra-openldap-server-dbg uuid

EXPOSE 389/tcp
ENTRYPOINT "/entrypoint.sh"

RUN cd /usr/bin && \
    ln -s /opt/zimbra/common/bin/ldapsearch
COPY files/zm-* /
COPY files/entrypoint.sh /
