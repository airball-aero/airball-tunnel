import pressure.source
import random

class Source(pressure.source.Source):
    '''Fake pressure source for software testing.'''
    
    def scan(self):
        return [random.uniform(0.0, 100.0) for i in range(0, 16)]
