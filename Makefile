#!/usr/bin/make -f
# SPDX-License-Identifier: AGPL-3+

export BUILD_TARGET_DISTRO=ubuntu-focal-amd64
export BUILD_TARGET_APTREPO=$(CURDIR)/.aptrepo/default

help:
	@echo "LibreZimbra build sytem help"
	@echo "-------------------------------------------------------------------------"
	@echo ""
	@echo "$(MAKE) clone            - clone all git repositories"
	@echo "$(MAKE) build-deb        - build the debian native packages"
	@echo "$(MAKE) build-legacy     - build the legacy build system packages"
	@echo "$(MAKE) finish-repo      - update the apt repository index"
	@echo ""
	@echo "$(MAKE) all              - run the complete build process"
	@echo ""
	@echo "$(MAKE) clean            - clean up everything"
	@echo "-------------------------------------------------------------------------"

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
build-legacy:
	@echo "building legacy packages"
	@./start-build-container /bin/bash /home/build/src/do-build-legacy.sh

# update the apt repo index
finish-repo:
	@echo "updating apt repo index"
	@cd pkg/__dckbp__/ && \
            DCK_BUILDPACKAGE_TARGET_REPO=$(BUILD_TARGET_APTREPO) \
            ./dck-buildpackage --update-aptrepo --target $(BUILD_TARGET_DISTRO)

# clean up everything
clean:
	@rm -Rf .aptrepo .stat tmp build

.PHONY: all build-deb build-legacy finish-repo clean
