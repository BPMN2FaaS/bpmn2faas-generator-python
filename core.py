import importlib


class Generator:
    def __init__(self, provider: str):
        if provider is not None:
            plugin = f'bpmn2faas_{provider}_plugin_python'

            try:
                self._plugin = importlib.import_module('.main', 'plugins.' + plugin).Plugin()
            except ModuleNotFoundError:
                raise ModuleNotFoundError(f'Plugin {plugin} not found!')
        else:
            raise ImportError('No plugin provided')

    def generate(self, bpmn_path: str, endpoints: object):
        print('Starting Plugin')
        print('-' * 10)

        # We is were magic happens, and all the plugins are going to be printed
        print(self._plugin.generate(bpmn_path, endpoints))

        print('-' * 10)
        print('Ending Plugin')
        print()
