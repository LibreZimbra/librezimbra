# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) Enrico Weigelt, metux IT consult <info@metux.net>

FROM zimbra/zm-base-os:devcore-ubuntu-20.04

ARG REPO_URL
ARG REPO_DISTRO
ARG REPO_SECTIONS

USER root

RUN curl ${REPO_URL}/apt-repo.pub | apt-key add - && \
    echo "deb ${REPO_URL} ${REPO_DISTRO} ${REPO_SECTIONS}" >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y mc iputils-ping net-tools
