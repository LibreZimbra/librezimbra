
This directory contains oss-qm public repository configurations
which are referenced by the actual build specs.

They're loaded automatically when package configs are loaded,
and keys not present in package spec are populated:

  git.url    -> oss-qm-pub-url
  git.branch -> oss-qm-pub-branch
