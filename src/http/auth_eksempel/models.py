#models.py
from pydantic import BaseModel
from enum import Enum
from typing import List

class Role(str, Enum):
    user = "user"
    admin = "admin"
    viewer = "viewer"

class User(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    country: str
    city: str
    zip_code: str
    street: str
    house_number: str
    active: bool = True
    roles: List[Role] = []

    def toDict(self):
        return {
            "username": self.username,
            "password": self.password,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "country": self.country,
            "city": self.city,
            "zip_code": self.zip_code,
            "street": self.street,
            "house_number": self.house_number,
            "active": self.active,
            "roles": self.roles,
        }
    
