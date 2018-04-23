
This directory contains upstream repository configurations which
are referenced by the actual build specs.

They're loaded automatically when package configs are loaded,
and keys not present in package spec are populated:

  git.url    -> upstream-url
  git.branch -> upstream-branch
