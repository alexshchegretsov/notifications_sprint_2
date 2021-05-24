import jwt
from aiohttp import web
from py_auth_header_parser import parse_auth_header

from settings import PUBLIC_KEY, JWT_ALGORITHM


def jwt_auth(coroutine):
    async def inner(request, *args):
        auth_header = request.headers.get('authorization', None)

        if not auth_header:
            return web.HTTPBadRequest()

        parsed_auth_header = parse_auth_header(auth_header)
        jwt_token = parsed_auth_header['access_token']

        try:
            payload = jwt.decode(jwt_token, PUBLIC_KEY, algorithms=[JWT_ALGORITHM])
            request.token_payload = payload
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            raise web.HTTPBadRequest(text='Token is missing or invalid')

        res = await coroutine(request, *args)
        return res

    return inner
