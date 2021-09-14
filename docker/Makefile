
DOCKER_GID := $(shell getent group docker | awk -F: '{printf "%d\n", $$3}')
BUILD_UID  := $(shell id -u)
BUILD_GID  := $(shell id -g)

DOCKER     ?= docker

all: librezimbra-build librezimbra-test

librezimbra-build:
	$(DOCKER) build -f Dockerfile.build \
            --build-arg BUILD_UID=$(BUILD_UID) \
            --build-arg BUILD_GID=$(BUILD_GID) \
            --build-arg DOCKER_GID=$(DOCKER_GID) \
            -t librezimbra-build .

librezimbra-test:
	$(DOCKER) build -f Dockerfile.test \
            --build-arg BUILD_UID=$(BUILD_UID) \
            --build-arg BUILD_GID=$(BUILD_GID) \
            --build-arg DOCKER_GID=$(DOCKER_GID) \
            -t librezimbra-test .
