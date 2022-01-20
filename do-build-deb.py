#!/usr/bin/env python
# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) Enrico Weigelt, metux IT consult <info@metux.net>

# This script builds all deb packages that are already migrated to
# native debian packaging. Those that aren't migrated yet are built
# with the 'build-legacy' script. See Makefile for more details.

from deb_autopkg import cmd
cmd.build_pool("cf/zimbra.yml", "default")
