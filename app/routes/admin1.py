from fastapi import FastAPI, Query, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from config.db import Base, get_db
from fastapi import APIRouter
from typing import List
from fastapi.responses import JSONResponse
from respository.my_token import create_access_token_admin,is_admin_authenticated
from fastapi.responses import Response
from respository.hashing import Hash
from schemas.admin import AdminCreateSchema,AdminSchema,AdminLoginSchema
from models import Admin,Student
import pandas as pd

base_path = "/The_Page_Turners"



admin = APIRouter(
    tags=["Admin"],prefix='/admin'
)

@admin.post("/signup", response_class=JSONResponse)
async def signup(admin: AdminCreateSchema, db: Session = Depends(get_db)):
    try:
        ad = db.query(Admin).filter(
            Admin.email == admin.email).first()
        if ad:
            return{"This email already exists. Please try with other one."}
        else:
            admin.password = Hash.bcrypt(admin.password)
            ad = Admin(**admin.__dict__)
            db.add(ad)
            db.commit()
            return {"status_code : 200", "Registration done successfully"}

    except:
        return HTTPException(status_code=404, detail="something went wrong.")

@admin.post("/signin", response_class=JSONResponse)
async def signin(admin: AdminLoginSchema, response: Response, db: Session = Depends(get_db)):
    try:
        ad = db.query(Admin).filter(
            Admin.email == admin.email).first()

        print(ad.password)
        if not ad:
            return{"Email id is incorrect"}

        is_password_correct = Hash.verify(ad.password,admin.password)
        
        print(is_password_correct)

        if not is_password_correct:
            return {"Password is incorrect"}

        else:
            jwt_token = create_access_token_admin(admin.email)
            print(jwt_token)
            response.set_cookie(key="admin_session_cookie",
                                value=f"Bearer {jwt_token}", max_age=60*60)
            return {"status_code": 200, "admin_access_token": jwt_token, "token_type": "bearer"}

    except:
        return HTTPException(status_code=404, detail="Couldn't logged in. Please try again.")

@admin.get("/my_profile", response_class=JSONResponse)
async def my_profile(is_auth=Depends(is_admin_authenticated),  db: Session = Depends(get_db)):
    try:
        if is_auth['flag']:
            print(is_auth)
            email = is_auth['payload']['sub']
            print(email)
            ad = db.query(Admin).filter(Admin.email == email).first()
            ad = {"name": ad.name, "role": ad.role,
                    "email": ad.email}
            return ad
        else:
            return {"message": "Unauthorized access. Please login to see the profile."}
    except:
        return HTTPException(status_code=404, detail="something went wrong. Please try again")

@admin.get("/logout", response_class=JSONResponse)
async def logout(response: Response, is_auth=Depends(is_admin_authenticated)):
    try:
        if is_auth['flag']:
            response.delete_cookie('admin_session_cookie')
        return {"message": "You logged out successfully."}
    except:
        return HTTPException(status_code=404, detail="Couldn't logged out. Please try again.")
    


    



