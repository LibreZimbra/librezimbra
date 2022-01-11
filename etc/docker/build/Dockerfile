# SPDX-License-Identifier: AGPL-3+
FROM zimbra/zm-base-os:devcore-ubuntu-20.04

ARG BUILD_UID
ARG BUILD_GID
ARG DOCKER_GID

USER root

# create the docker group + fixup the build user
RUN groupadd -g ${DOCKER_GID} docker && \
    groupmod -g ${BUILD_GID} build && \
    usermod -u ${BUILD_UID} -g ${BUILD_GID} build && \
    chown -R build:build /home/build && \
    usermod -a -G docker build && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 9BE6ED79 && \
    apt-get install -y \
        bundler mc libssl-dev libsasl2-dev docker.io tig git rsync \
        apt-transport-https aptitude python python-yaml uuid-runtime ant \
        ant-contrib ivy telnet iputils-ping && \
    gem install bundler:1.17.3 jekyll i18n

USER build
