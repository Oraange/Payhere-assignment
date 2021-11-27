from dataclasses import dataclass


@dataclass
class SignUpInputDTO:
    nick_name: str
    email: str
    password: str


@dataclass
class SignInInputDTO:
    email: str
    password: str


@dataclass
class TokenDTO:
    access_token: str
