from fastapi import FastAPI, status, Depends, HTTPException
from database import get_session, Base, engine
from models import AddressBook
from schemas import BookSchema, NearestAddressSchema
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from typing import List
from helper import CalculateDistance


# Create the database


# Initialize app
app = FastAPI()
Base.metadata.create_all(engine)

@app.post("/book", response_model=BookSchema, status_code=status.HTTP_201_CREATED)
def create_book(book: BookSchema, session: Session = Depends(get_session)):

    # create an instance of the ToDo database model
    book_db = AddressBook(
            first_name = book.first_name,
            last_name = book.last_name,
            address = book.address,
            lat = book.lat,
            lon= book.lon)

    

    # add it to the session and commit it
    session.add(book_db)
    session.commit()
    session.refresh(book_db)
    book.id = book_db.id

    # return the todo object
    return book

@app.get("/book/{id}")
def read_book(id: int,session: Session = Depends(get_session)):

    # create a new database session
   
    # get the AddressBook item with the given id
    book_db = session.query(AddressBook).get(id)

    # check if AddressBook item with given id exists. If not, raise exception and return 404 not found response
    if not book_db:
        raise HTTPException(status_code=404, detail=f"AddressBook item with id {id} not found")

    return book_db

@app.put("/book/{id}")
def update_book(id: int, lat: float,lon : float, address : str, session: Session = Depends(get_session)):

    # create a new database session
    # get the AddressBook item with the given id
    book_db = session.query(AddressBook).get(id)

    # update AddressBook item with the given fields (if an item with the given id was found)
    if book_db:
        book_db.lat = lat
        book_db.lon =  lon
        book_db.address = address 
        session.add(book_db)
        session.commit()
        session.refresh(book_db)
        
    # check if AddressBook item with given id exists. If not, raise exception and return 404 not found response
    if not book_db:
        raise HTTPException(status_code=404, detail=f"AddressBook item with id {id} not found")

    return book_db

@app.delete("/book/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(id: int,session: Session = Depends(get_session)):

    # create a new database session
    
    # get the AddressBook item with the given id
    book_db = session.query(AddressBook).get(id)

    # if AddressBook item with given id exists, delete it from the database. Otherwise raise 404 error
    if book_db:
        session.delete(book_db)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"AddressBook item with id {id} not found")

    return None

@app.get("/readBook")
def read_book_list(session: Session = Depends(get_session)):
    # create a new database session
    # get all AddressBook items
    book_list = session.query(AddressBook).all()
    # close the session
    return list(book_list)

@app.get("/getNearbyAddresses")
def get_address(lat : float, lon : float , distance : float,session: Session = Depends(get_session)):
    # create a new database session
    
    with engine.connect() as con:
        query = CalculateDistance(lat, lon, distance)
        print(query)
        statement = text(query)
        res = con.execute(statement)
        resArr = []
        # get all AddressBook items with given co-ordinates nearest to the distance
        for rows in res:
            book = NearestAddressSchema()
            book.id = rows[0]
            book.first_name = rows[1]
            book.last_name = rows[2]
            book.address = rows[3]
            book.lat = rows[4]
            book.lon = rows[5]
            book.distance = rows[6]
            resArr.append(book)

        return resArr