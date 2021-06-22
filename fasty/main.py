import json
from urllib.request import urlopen

from fastapi import Depends, FastAPI, Header, HTTPException
from jose import jwt, JWTError
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool


def get_jwt_from_auth_header(authorization: str):
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail='Authorization header not provided',
        )
    parts = authorization.split()
    if parts[0].lower() != 'bearer':
        raise HTTPException(
            status_code=401,
            detail='Authorization header malformed',
        )
    if len(parts) == 1:
        raise HTTPException(
            status_code=401,
            detail='Authorization header malformed',
        )
    if len(parts) > 2:
        raise HTTPException(
            status_code=401,
            detail='Authorization header malformed',
        )
    return parts[1]


async def requires_auth(Authorization: str = Header(...)):
    token = get_jwt_from_auth_header(Authorization)
    jsonurl = urlopen('https://twig-world.eu.auth0.com/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    try:
        unverified_header = jwt.get_unverified_header(token)
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail='Error decoding JWT headers',
        )
    rsa_key = None
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e'],
            }
            break
    if not rsa_key:
        raise HTTPException(
            status_code=401,
            detail='RSA key for JWT not found',
        )
    try:
        jwt.decode(
            token,
            rsa_key,
            algorithms=['RS256'],
            audience='https://rostering.twigscience.com/',
            issuer='https://twig-world.eu.auth0.com/',
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail='JWT signature has expired',
        )
    except jwt.JWTClaimsError:
        raise HTTPException(
            status_code=401,
            detail='Invalid claims in JWT',
        )
    except Exception:
        raise HTTPException(
            status_code=401,
            detail='Unknown error decoding JWT',
        )


@app.get('/')
def read_root():
    return {'Hello': 'World'}


@app.get('/items/{item_id}', dependencies=[Depends(requires_auth)])
def read_item(item_id: int, q: str = None):
    return {'item_id': item_id, 'q': q}


@app.put('/items/{item_id}', dependencies=[Depends(requires_auth)])
def save_item(item_id: int, item: Item):
    return {'item_name': item.name, 'item_id': item_id}
