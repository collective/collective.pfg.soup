from zope.interface import Interface


class IAddPfgIndex(Interface):

    class __call__(catalog):
        """adds an repoze.catalog compatible index to given catalog,
        context is supoosed to be a PFG Field.
        """
