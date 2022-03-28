import importlib

class Generator:
    # We are going to receive a plugin as parameter
    def __init__(self, plugin):
        # Checking if plugin were sent
        if plugin != None:
            # create a list of plugins
            try:
                self._plugin = importlib.import_module(plugin, './plugins/' + plugin).Plugin()
            except AttributeError:
                raise ImportError('Plugin ' + plugin + ' not found!')
        else:
            raise ImportError('No plugin provided')


    def run(self):
        print('Starting Plugin')
        print('-' * 10)

        # We is were magic happens, and all the plugins are going to be printed
        print(self._plugin)

        print('-' * 10)
        print('Ending Plugin')
        print()