from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from config.db import get_db
from models import Student, Connection
from schemas import student
from respository.oauth2 import get_current_user
from typing import Optional
from datetime import datetime
from schemas import connection as schema

connection = APIRouter(tags=["connection"],prefix='/connection')


@connection.post("/request}", response_model=schema.Connection)
def create_connection(connection: schema.ConnectionCreate, db: Session = Depends(get_db), current_user: student.Student = Depends(get_current_user)):
    """
    Send a connection request to another user.
    """
    db_student = db.query(Student).filter(Student.id == connection.receiver_id).first()
    if not db_student:
        raise HTTPException(status_code=400, detail="receiver id is the invalid student id ")
    # Check if the sender and receiver are different users
    if current_user.id == connection.receiver_id:
        raise HTTPException(status_code=400, detail="You cannot connect with yourself.")
    

    # Check if a connection request already exists between these two users
    existing_connection = db.query(Connection).filter(
        (Connection.sender_id == current_user.id) &
        (Connection.receiver_id == connection.receiver_id)
    ).first()

    if existing_connection:
        if existing_connection.status == "pending":
            raise HTTPException(status_code=400, detail="A connection request has already been sent to this user.")
        elif existing_connection.status == "accepted":
            raise HTTPException(status_code=400, detail="You are already connected with this user.")

    # Create a new connection request
    new_connection = Connection(
        sender_id=current_user.id,
        receiver_id=connection.receiver_id,
        status="pending",
        created_at=datetime.now()
    )
    
    db.add(new_connection)
    db.commit()
    db.refresh(new_connection)

    return new_connection



@connection.post("/accept", response_model=schema.Connection)
def accept_connection(connectionUpd: schema.ConnectionUpdate,db: Session = Depends(get_db),current_user: student.Student = Depends(get_current_user)):
    # db_conn = db.query(Connection).get(connectionUpd.sender_id==Connection.sender_id)
    db_conn = db.query(Connection).filter(
        (connectionUpd.sender_id == Connection.sender_id)&(current_user.id == Connection.receiver_id)).first()
    if not db_conn:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Connection Request not found"
        )
    if db_conn.receiver_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized access"
        )
    if db_conn.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Connection already accepted or rejected"
        )
    db_conn.status = "accepted"
    db.add(db_conn)
    db.commit()
    db.refresh(db_conn)
    return db_conn



@connection.delete("/connection_req_reject", response_model=schema.Connection)
def reject_connection(connectionUpd: schema.ConnectionUpdate,db: Session = Depends(get_db),current_user: student.Student = Depends(get_current_user)):
    db_conn = db.query(Connection).get(connectionUpd.sender_id)
    db_conn = db.query(Connection).filter(
        (connectionUpd.sender_id == Connection.sender_id)&(current_user.id == Connection.receiver_id)
        ).first()
    # return db_conn
    if not db_conn:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Connection Request not found"
        )
    if db_conn.receiver_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized access"
        )
    if db_conn.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Connection already accepted or rejected"
        )
    db.delete(db_conn)
    db.commit()
    # db.refresh(db_conn)
    return db_conn