#auth_rest_api_models.py
from pydantic import BaseModel
from typing import List

from src.http.auth_eksempel.models import User, Role

class RegisterUserRequest(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    country: str
    city: str
    zip_code: str
    street: str
    house_number: str
    roles: List[Role]

class GetBearerTokenRequest(BaseModel):
    username: str
    password: str

class ActivateUserRequest(BaseModel):
    username: str

