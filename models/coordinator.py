# from dataclasses import dataclass, field
import primitives

class ManagePortfolio:


"""
@dataclass
class Ceo:
    "Class for coordinating over exchanges"
    exchangesNames: list = field(default_factory=list)
    userName: str = field(default_factory=str)  # ""
    workers: set() = field(default_factory=set)
    def __post_init__(self):
        userData = primitives.getJsoned(f'users/{self.userName}.json') 
        if userData:
            print('unbelievable')
        else:
            exchangesNames = ["bitstamp.client"]
            workersRaw = map(__import__, exchangesNames)
            for exchangeClass in workersRaw:
                self.workers.add(primitives.Worker(exchangeClass))
            print(self.workers)
            pass

    
    def importExchange(self):
        self.exchangeClass = __import__(self.exchange+".client")
"""

if __name__ == '__main__':
    # userGen('bitstamp')
    pass
