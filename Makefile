#!/usr/bin/make -f
# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) Enrico Weigelt, metux IT consult <info@metux.net>

export TARGET_DISTRO_NAME    ?= ubuntu
export TARGET_DISTRO_RELEASE ?= focal
export TARGET_DISTRO_ARCH    ?= amd64

export BUILD_TARGET_DISTRO   = $(TARGET_DISTRO_NAME)-$(TARGET_DISTRO_RELEASE)-$(TARGET_DISTRO_ARCH)
export BUILD_TARGET_APTREPO  = $(CURDIR)/.aptrepo/default
export BUILD_DOCKER_IMAGE    := librezimbra-build

export DOCKER     ?= docker
export DOCKER_GID := $(shell getent group docker | awk -F: '{printf "%d\n", $$3}')
export BUILD_UID  := $(shell id -u)
export BUILD_GID  := $(shell id -g)

help:
	@echo "LibreZimbra build sytem help"
	@echo "-----------------------------------------------------------------------------"
	@echo ""
	@echo "$(MAKE) clone                      - clone all git repositories"
	@echo "$(MAKE) build-deb                  - build the debian native packages"
	@echo "$(MAKE) build-legacy               - build the legacy build system packages"
	@echo "$(MAKE) finish-repo                - update the apt repository index"
	@echo ""
	@echo "$(MAKE) all                        - run the complete build process"
	@echo ""
	@echo "$(MAKE) clean                      - clean up everything"
	@echo ""
	@echo "$(MAKE) check-update-synacor       - check for updates from synacor repos"
	@echo "$(MAKE) check-update-librezimbra   - check for updates from librezimbra repos"
	@echo "-----------------------------------------------------------------------------"

# do it all - note that the order is important
all: clone build-deb build-legacy finish-repo

# clone repos
clone:
	@echo "cloning git repos"
	@env python do-clone.py

# build the debian native packages
build-deb:
	@echo "building deb packages"
	@env python do-build-deb.py

# build legacy packages (not debian native yet)
build-legacy: image-$(BUILD_DOCKER_IMAGE)
	@echo "building legacy packages"
	@./start-build-container /bin/bash /home/build/src/do-build-legacy.sh
	@$(MAKE) finish-repo

# update the apt repo index
finish-repo:
	@echo "updating apt repo index"
	@cd pkg/__dckbp__/ && \
            DCK_BUILDPACKAGE_TARGET_REPO=$(BUILD_TARGET_APTREPO) \
            ./dck-buildpackage --update-aptrepo --target $(BUILD_TARGET_DISTRO)

# check whether we missed an update from synacor
check-update-synacor:
	@for r in `cat cf/repos-zimbra` ; do ( \
            cd pkg/$$r && \
            if [ `git rev-list --left-right --count synacor/develop...HEAD | sed 's~\t.*~~'` != '0' ]; then \
                echo "new commits from synacor in pkg/$$r" ; \
            fi ; \
        ) ; done

check-update-librezimbra:
	@for r in `cat cf/repos-zimbra cf/repos-extra` ; do ( \
            cd pkg/$$r && \
            if [ `git rev-list --left-right --count librezimbra/develop...HEAD | sed 's~\t.*~~'` != '0' ]; then \
                echo "new commits from librezimbra in pkg/$$r" ; \
            fi ; \
        ) ; done

image-$(BUILD_DOCKER_IMAGE):
	cd etc/docker/build && $(DOCKER) build \
            --build-arg BUILD_UID=$(BUILD_UID) \
            --build-arg BUILD_GID=$(BUILD_GID) \
            --build-arg DOCKER_GID=$(DOCKER_GID) \
            -t $(BUILD_DOCKER_IMAGE) .

# clean up everything
clean:
	@rm -Rf .aptrepo .stat tmp build
	@docker rmi -f $(BUILD_DOCKER_IMAGE)

.PHONY: all build-deb build-legacy finish-repo clean
