class Product:
    def __init__(self, code, name, nutriments):
        self._code = code
        self._name = name
        self._nutriments = nutriments

    @property
    def code(self):
        return self._code

    @property
    def name(self):
        return self._name
    
    @property
    def nutriments(self):
        return self._nutriments