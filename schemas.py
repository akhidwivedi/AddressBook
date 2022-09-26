from turtle import distance
from pydantic import BaseModel

# Create ToDo Schema (Pydantic Model)
class BookSchema(BaseModel):
    id : int = None
    first_name : str = None
    last_name :str = None
    address : str = None
    lat : float = None
    lon : float = None
class NearestAddressSchema(BaseModel):
    id : int = None
    first_name : str = None
    last_name :str = None
    address : str = None
    lat : float = None
    lon : float = None
    distance : float = None