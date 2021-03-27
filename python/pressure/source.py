

class Source:
    '''Abstract base class for a source of test pressures.'''

    def scan(self):
        '''Measure and return an array of pressures as configured.'''
        return []
