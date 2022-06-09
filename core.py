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

    def generate(self, path: str, endpoints: dict) -> str :
        print('Starting Plugin')
        print('-' * 10)

        output = self._plugin.generate(path, endpoints)

        print('-' * 10)
        print('Ending Plugin')
        print()
        return output
