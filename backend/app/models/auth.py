from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class AegisMessageRequest(BaseModel):
    message: str = Field(min_length=1)