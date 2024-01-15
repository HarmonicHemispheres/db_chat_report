import jwt
from idsdata.config import Config

class VerifyToken():
    """Does all the token verification using PyJWT"""

    def __init__(self, token, config):
        self.token = token
        self.config = Config()
        self.config = config

        # This gets the JWKS from a given URL and does processing so you can
        # use any of the keys available
        jwks_url = f'{self.config.issuer}/.well-known/openid-configuration/jwks'
        self.jwks_client = jwt.PyJWKClient(jwks_url)

    def verify(self):
        # This gets the 'kid' from the passed token
        try:
            self.signing_key = self.jwks_client.get_signing_key_from_jwt(
                self.token
            ).key
        except jwt.exceptions.PyJWKClientError as error:
            return {"status": "jwk error", "msg": error.__str__()}
        except jwt.exceptions.DecodeError as error:
            return {"status": "decode error", "msg": error.__str__()}

        try:
            payload = jwt.decode(
                self.token,
                self.signing_key,
                algorithms=self.config.algorithms,
                audience=self.config.audience,
                issuer=self.config.issuer,
            )
        except Exception as e:
            return {"status": "error", "message": str(e)}

        return payload