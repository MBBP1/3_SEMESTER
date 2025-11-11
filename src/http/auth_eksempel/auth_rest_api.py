#auth_rest_api.py
import json
from fastapi import FastAPI, Depends, HTTPException, Header, Body
from typing import List

from src.http.auth_eksempel.user_service import User_service
from src.http.auth_eksempel.models import User, Role
from src.http.auth_eksempel.auth_rest_api_models import RegisterUserRequest, GetBearerTokenRequest, ActivateUserRequest


class Auth_rest_api:

    def __init__(self, database_file: str = "db_user_flat_file.json"):
        self.user_service = User_service(database_file)

        self.app = FastAPI()
        #self.app.add_event_handler("startup", self.on_startup)

        self.app.post("/register_user")(self.register_user)
        self.app.post("/get_bearer_token")(self.get_bearer_token)
        self.app.post("/deactivate_user")(self.deactivate_user)
        self.app.post("/activate_user")(self.activate_user)

        self.app.get("/user/status/{username}")(self.get_user_status)
        self.app.get("/user/address/{username}")(self.get_user_address)

    def register_user(self, post_variables: RegisterUserRequest):
        self.user_service.register_user(
            post_variables.username, 
            post_variables.password, 
            post_variables.first_name, 
            post_variables.last_name,
            post_variables.country,
            post_variables.city,
            post_variables.zip_code,
            post_variables.street,
            post_variables.house_number, 
            post_variables.roles
        )
        return { "status": "user created"}

    def get_bearer_token(self, post_variables: GetBearerTokenRequest):
        token = self.user_service.get_bearer_token(post_variables.username, post_variables.password)
        return {"token": token}

    def deactivate_user(
            self, 
            post_variables: ActivateUserRequest,
            token: str = Header(...)
        ):

        if not token.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid or missing Authorization header")

        self.user_service.deactivate_user(token, post_variables.username)
        return { "status": f"user '{post_variables.username}' has been deactivated"}

    def activate_user(
            self, 
            post_variables: ActivateUserRequest,
            token: str = Header(...)
        ):
        if not token.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid or missing Authorization header")

        self.user_service.activate_user(token, post_variables.username)
        return { "status": f"user '{post_variables.username}' has been reactivated"}

    ## GET endpoints
    def get_user_status(
            self, 
            username: str,
            token: str = Header(...)
    ):
        if not token.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid or missing Authorization header")

        is_active = self.user_service.get_user_status(token, username)
        return {"username": username, "active": is_active}

    def get_user_address(
            self, 
            username: str,
            token: str = Header(...)
    ):
        if not token.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid or missing Authorization header")
        
        address_data = self.user_service.get_user_address(token, username)
        return address_data