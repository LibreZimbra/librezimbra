# SPDX-License-Identifier: AGPL-3.0-or-later

# this file is meant to be shared/synced between many packages (v0.4)

ANT ?= ant
ZIMBRA_PREFIX ?= /opt/zimbra

INSTALL_DIR                   = $(DESTDIR)$(ZIMBRA_PREFIX)
INSTALL_DIR_JETTY_ETC         = $(INSTALL_DIR)/jetty_base/etc
INSTALL_DIR_ZIMLETS           = $(INSTALL_DIR)/zimlets
INSTALL_DIR_WA_SERVICE        = $(INSTALL_DIR)/jetty_base/webapps/service
INSTALL_DIR_WA_SERVICE_WEBINF = $(INSTALL_DIR_WA_SERVICE)/WEB-INF
INSTALL_DIR_LIB_JARS          = $(INSTALL_DIR)/lib/jars

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

define install_jetty_etc
mkdir -p $(INSTALL_DIR_JETTY_ETC)
cp $(1) $(INSTALL_DIR_JETTY_ETC)/$(notdir $(strip $(1)))
endef

define install_jar_lib
mkdir -p $(INSTALL_DIR_LIB_JARS)
cp $(1) $(INSTALL_DIR_LIB_JARS)/$(notdir $(strip $(1)))
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

build-ant-autover:
	rm -Rf build
	$(ANT) $(ANT_ARG_BUILDINFO) $(ANT_TARGET)

clean-ant:
	rm -Rf build

install-common:
	for i in $(INSTALL_CREATE_DIRS) ; do mkdir -p $(INSTALL_DIR)/$$i ; done
	if [ "$(INSTALL_FILES_JETTY_ETC)" ]; then \
            mkdir -p $(INSTALL_DIR_JETTY_ETC) ; \
            cp $(INSTALL_FILES_JETTY_ETC) $(INSTALL_DIR_JETTY_ETC) ; \
        fi
	if [ "$(INSTALL_FILES_ZIMLETS)" ]; then \
            mkdir -p $(INSTALL_DIR_ZIMLETS) ; \
            cp $(INSTALL_FILES_ZIMLETS) $(INSTALL_DIR_ZIMLETS) ; \
        fi
	if [ "$(INSTALL_FILES_WA_SERVICE_WEBINF)" ]; then \
            mkdir -p $(INSTALL_DIR_WA_SERVICE_WEBINF) ; \
            cp $(INSTALL_FILES_WA_SERVICE_WEBINF) $(INSTALL_DIR_WA_SERVICE_WEBINF) ; \
	fi

.PHONY: build-ant clean-ant
