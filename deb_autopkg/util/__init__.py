# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) Enrico Weigelt, metux IT consult <info@metux.net>

__all__ = [ "log" ]

"""transform a list to printable text via given transform function"""
def list2text(data, func):
    return "\n".join(map(func, data))

"""transform a dict to printable text via given transform function"""
def dict2text(data, func):
    return "\n".join(map(func, data.values()))
