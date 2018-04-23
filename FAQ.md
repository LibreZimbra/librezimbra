
Q: What does 'pool' mean here ?

A: Pools are used for organizing sets of packages. Each pool lives entirely on
   it's own, using an own apt repository (in `.aptrepo/<pool>`).

---

Q: How can I define which distros to build for ?

A: Use dck-buildpackage's target configs. The `targets:` section in the config
   yml tells the dck-buildpackage's target names.

---

Q: Where can I get dck-buildpackage ? What is that anyways ?

A: It's a little tool for building debian packages in docker containers.
   See: https://github.com/metux/docker-buildpackage

---

Q: How can I build packages that depend on others (that aren't in the distro yet) ?

A: Just add the dependencies to the packages (note: the names you're using in the
   config, not the debian package names). The packages will be built along the
   dependency tree and placed into the pool's repo. This repo is also added to
   the build container's package sources, so apt can automatically install the
   previously built packages from there.

---

Q: How can I trigger rebuild of packages that I already had built ?

A: Remove the corresponding state files in `.stat/`
