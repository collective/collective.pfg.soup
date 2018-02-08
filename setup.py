from setuptools import setup, find_packages
import sys, os

version = '1.7.dev0'
shortdesc = 'PloneFormGen Adapter: store, show/search, edit, csv-export, based on souper.soup'
longdesc =  open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
longdesc += open(os.path.join(os.path.dirname(__file__), 'HISTORY.rst')).read()
# longdesc += open(os.path.join(os.path.dirname(__file__), 'LICENSE.rst')).read()

setup(name='collective.pfg.soup',
      version=version,
      description=shortdesc,
      long_description=longdesc,
      classifiers=[
            'Development Status :: 5 - Production/Stable',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Software Development',
            "Framework :: Plone",
      ],
      keywords='',
      author='BlueDynamics Alliance',
      author_email='dev@bluedynamics.com',
      license='GPLv2',
      url='https://pypi.python.org/pypi/collective.pfg.soup',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=True,
      install_requires=[
            'bda.calendar.base',
            'collective.js.datatables',
            'Products.CMFPlone',
            'Products.PloneFormGen',
            'setuptools',
            'souper.plone',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
