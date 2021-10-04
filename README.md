LibreZimbra - a libre enterprise collaboration / groupware suite
=================================================================

LibreZimbra is a fork of the opensource version of the Zimbra Collaboration Suite.


Why the fork ?
--------------

- the vendor (Synacor) did not care about many important bugs (eg. don't
  even get the installation process right) now for over 15 years (!),
  and directly told us (seasoned Zimbra integration experts) they're not
  not going change that anytime soon

- Synacor leaves it's integration partners alone - even for the expensive
  commercial version. with each project, each upgrade, we have to spend
  a great deal of time on finding workarounds for their bugs

- Synacor has no actual interest in any opensource community for Zimbra,
  it's just crooked marketing slang, nothing more

- even worse: they've got the audacity to ask us, the integrators, to
  fix their bugs for them, for free, and hand over all our copyrights
  when we want to contribute - that's the red line crossed.


What the fork will do ?
-----------------------

- provide an easy to use build system and development infrastructure, so
  everybody can easily work on and compile Zimbra on its own. no more
  dependency on unaudited Syncor's binary packages

- fixing the long outstanding bugs

- support cloud-native / container-native setups and fully automatic
  deployments, automatic scaling in kubernetes clusters

- free reimplementatioin commercial-only features, eg. a tool for moving
  around users not just within a cluster, but also across entirely separate
  clusters or even across several groupware solutions.

- move 3rdparty components closer to upstream

- for security critical components like OpenSSL directly from the underlying
  GNU/Linux distribution, in order to get security fixes automatically.

  Remember the Hearbleed incident: Zimbra took many weeks to provide some form
  of fix - common GNU/Linux distros had the fixes ready and deployed in the
  field within less than a day. Zimbra just unncessarily left the servers
  critically vulnerable for several weeks, just because of their lazyness and
  refusal to understand how GNU/Linux software distribution works.

- build up a living and flourishing opensource development community

- empowering organisations to do their own independent audits, individual
  customizations and massively reducing operating costs by automation

- Final goal: complete replacement for Synacor's Zimbra, especially the
  commercial version

Contributer Agreement
---------------------

In contrast to Synacor, we do NOT demand contributors to give away all their IPR
for free. We consider those demands very unethical and brazen. All contributors
will keep the ownership on their contributions - just like actual FOSS projects
work for decades.


Build requirements
------------------

* docker
* git
* gnu make
* python
* python-yaml


How to contact ?
----------------

The project is founded by the independent FOSS/Linux consulting firm
metux IT consult.

- email: info@metux.net
- phone: +49-151-27565287
- telegram group: https://t.me/librezimbra
