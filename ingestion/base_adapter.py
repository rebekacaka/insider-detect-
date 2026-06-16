

"""
I implemented the adapter pattern using Python's ABC module to enforce a consistent interface across all data sources. 
Each adapter must implement fetch() and available_tickers()-if they don't, Python raises an error immediately. 
I used dataclasses for the return type to ensure type safety across the pipeline.

I initially used pass in the abstract methods, but while researching production pipeline patterns I
found a DEV Community article about a fraud detection system that switched to raise NotImplementedError after a 
production failure caused by silent method misimplementation. 
I applied the same fix.
"""

from abc import ABC, abstractmethod 
from dataclasses import dataclass
from datetime import date 
from typing import List 
#ABC- ABstract Base Class. ANy class that inherits from this can not be used directly, only inherited. 
#abstractmethod its like a decorator that marks a function as must be implemented by child classes 

@dataclass
class MarketRecord: #simple data container classs and uses dataclass so we dont have to write everything everytime like init etc
    source:str  
    ticker:str
    market:str
    record_date:date
    open_price: float
    close_price: float
    volume:int 

#ABC means this class can only be inherited not used diretly 
class BaseAdapter(ABC):
    source:str
    market:str

    @abstractmethod #The @abstractmethod decorator means every child class MUST implement this function. If they don't, Python raises an error the moment you try to use the class.
    def fetch(self, ticker: str, start: date, end: date) -> List[MarketRecord]:
        raise NotImplementedError("Each adapter must implement its own fetch() method")
    
    # returns list of tickers this adapter can fetch
    @abstractmethod
    def available_tickers(self) -> List[str]:
        raise NotImplementedError("Each adapter must implement its own available_tickers() method")

