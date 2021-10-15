# SPDX-License-Identifier: AGPL-3.0-or-later

# this file is meant to be shared/synced between many packages (v0.4)

ANT ?= ant
ZIMBRA_PREFIX ?= /opt/zimbra
INSTALL_DIR = $(DESTDIR)$(ZIMBRA_PREFIX)

include version.mk

ANT_ARG_BUILDINFO = -Dzimbra.buildinfo.versionmajor=$(ZIMBRA_VERSION_MAJOR) \
                    -Dzimbra.buildinfo.versionminor=$(ZIMBRA_VERSION_MINOR) \
                    -Dzimbra.buildinfo.microversion=$(ZIMBRA_VERSION_MICRO) \
                    -Dzimbra.buildinfo.majorversion=$(ZIMBRA_VERSION_MAJOR) \
                    -Dzimbra.buildinfo.minorversion=$(ZIMBRA_VERSION_MINOR) \
                    -Dzimbra.buildinfo.versionmicro=$(ZIMBRA_VERSION_MICRO) \
                    -Dzimbra.buildinfo.buildnum=$(ZIMBRA_VERSION_PATCH)

define mk_install_dir
mkdir -p $(INSTALL_DIR)/$(strip $(1))
endef

define install_conf
mkdir -p $(INSTALL_DIR)/conf
cp $(1) $(INSTALL_DIR)/conf/$(notdir $(strip $(1)))
endef

define install_jetty_lib
mkdir -p $(INSTALL_DIR)/jetty_base/common/lib
cp $(1) $(INSTALL_DIR)/jetty_base/common/lib/$(notdir $(strip $(1)))
endef

define install_jar_lib
mkdir -p $(INSTALL_DIR)/lib/jars
cp $(1) $(INSTALL_DIR)/lib/jars/$(notdir $(strip $(1)))
endef

define install_libexec
mkdir -p $(INSTALL_DIR)/libexec
cp $(1) $(INSTALL_DIR)/libexec/$(notdir $(strip $(1)))
endef

define install_wa_service_lib
mkdir -p $(INSTALL_DIR)/jetty_base/webapps/service/WEB-INF/lib/
cp $(1) $(INSTALL_DIR)/jetty_base/webapps/service/WEB-INF/lib/$(notdir $(strip $(1)))
endef

build-ant:
	rm -Rf build
	$(ANT) $(ANT_TARGET)

clean-ant:
	rm -Rf build

.PHONY: build-ant clean-ant
