#!/bin/bash
# SPDX-License-Identifier: AGPL-3+

set -e

if [ `hostname` != 'librezimbra-build' ]; then
    echo "=== run me inside the build container" >&2
    exit 1
fi

export ENV_RESUME_FLAG=1
export ENV_SKIP_CLEAN_FLAG=1

export BUILD_DESTINATION_BASE_DIR=$(pwd)/build/target
export BUILD_DIR=$(pwd)/build/staging

export BUILDER_ROOT=$(dirname $(realpath $0))
export PACKAGE_DIR=$BUILDER_ROOT/.aptrepo/default/ubuntu-focal-amd64/pool/dists/focal/contrib/zimbra

mkdir -p $PACKAGE_DIR

cd $BUILDER_ROOT/pkg/zm-build && ./build.pl \
    --build-no=1984 \
    --build-release=KILEZMORE \
    --build-release-no=9.0.1 \
    --build-release-candidate=ALCHEMIST \
    --ant-options="-DskipTests=1" \
    --build-destination-base-dir=$BUILD_DESTINATION_BASE_DIR \
    --build-dir=$BUILD_DIR
