#!/usr/bin/env python
# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) Enrico Weigelt, metux IT consult <info@metux.net>

# this script clones all git repositories and checks out development branch
# (on the first run) or updates the remotes (on subsequent runs)

from deb_autopkg import cmd
cmd.clone_all("cf/zimbra.yml")
