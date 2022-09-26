from tokenize import Floatnumber
from sqlalchemy import Column, Integer, String, Float
from database import Base

# Define To AddressBook class inheriting from Base
class AddressBook(Base):
    __tablename__ = 'book_tbl'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(256))
    last_name = Column(String(256))
    address = Column(String(256))
    lat =  Column(Float)
    lon =  Column(Float)
    class Config:
        orm_mode = True
