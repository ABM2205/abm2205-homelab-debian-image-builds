from pyinfra.api import FactBase


class dockerCompose(FactBase):
    '''
    Returns information about a docker compose service
    '''

    def command(self, path):
        # Find files in the given location
        return 'find {0} -type f'.format(path)

    def process(self, output):
        return output  # return the list of lines (files) as-is