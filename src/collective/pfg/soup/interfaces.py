from zope.interface import Interface


class IPfgSoupLayer(Interface):
    """Browserlayer
    """


class IPfgSoupAdapter(Interface):
    """marker for a pfg soup adapter
    """


class IAddPfgIndex(Interface):

    def __call__(catalog):
        """adds an repoze.catalog compatible index to given catalog,
        context is supoosed to be a PFG Field.
        """
