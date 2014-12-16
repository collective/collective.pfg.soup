Soup Storage for PloneFormGen Form Data
=======================================

This PloneFormGen Storage Adapter saves and index form-data in so called
``soup``. A soup is an unstructured flat storage containing records with
attributes (form-data). Attributes are indexed in an ``repoze.catalog``. Thus
complex queries on the data are possible.

It ships with an full-featured table view based on ``jquery.datatables``.
Datatables server-side processing enables to have large datasets processed.
It provides a search over all columns and by single columns. Each column
can be sorted.

Additional to the form data userid and timestamp of creations is logged.

A row can be edited. After save modification-timestamp, userid and changed
fields are logged.

CSV-Export of all data is possible, including creators userid, creation- and
last-modified-timestamp if selected.


Installation
============

Just depend in your buildout on the egg ``collective.pfg.soup``. ZCML is
loaded automagically with z3c.autoinclude.

Install ``Soup Adapter for PloneFormGen`` as an addon in Plone control-panel or
portal_setup.

This package is written for Plone 4.2 or later.

Source Code and Contributions
=============================

If you want to help with the development (improvement, update, bug-fixing, ...)
of ``collective.pfg.soup`` this is a great idea!

The code is located in the
`github collective <https://github.com/collective/collective.pfg.soup>`_.

You can clone it or `get access to the github-collective
<http://collective.github.com/>`_ and work directly on the project.

Maintainer is Jens Klein and the BlueDynamics Alliance developer team. We
appreciate any contribution and if a release is needed to be done on pypi,
please just contact one of us
`dev@bluedynamics dot com <mailto:dev@bluedynamics.com>`_

Contributors
============

- Jens W. Klein <jens@bluedynamics.com>

- Benjamin Stefaner

- Peter Holzer

License GPL 2

Todos
=====

- only indexed fields are sortable - reflect this in UI

- create indexadapters for all field types

- binary handling
