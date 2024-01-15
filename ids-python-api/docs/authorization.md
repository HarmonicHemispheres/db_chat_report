## IDS-PYTHON-API Security

---

The example in this API uses dendencies below to authorize endpoints by verifying the JWT coming from the Interject Addin. It checks the token validity by connecting with the JWK link provided by the Identity Provider. This information belongs in a config.py/.env file for reference.

#### Auth dependencies in the `pyproject.toml`:

```
pyjwt = {extras = ["crypto"], version = "^2.7.0"}
```

---

#### <u>Customizing Security</u>

##### Endpoint Customization

Placing the HTTPBearer() function before the start of the application

```
from fastapi.security import HTTPBearer

AUTH_SCHEME = create_auth_scheme()
APP = create_ids_api()
```

alter any endpoint with the following code to secure the endpoint.

```
@APP.Post(...)
async def data(request: InterjectRequest, token: str = Depends(AUTH_SCHEME)):
    global CONFIG
    result = VerifyToken(token.credentials,CONFIG).verify()

    if result.get("status"):
```

##### JWT Customization

In this example, there are a few links needed to verify the JWT with the authoization server audience and the JWKs. There are also more that can be customized depending on the needs for verification.

```
//idsdata\utils\verify_token.py

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
            return {"status": "error", "msg": error.__str__()}
        except jwt.exceptions.DecodeError as error:
            return {"status": "error", "msg": error.__str__()}

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

```

for more information please see this [link](https://fastapi.tiangolo.com/tutorial/security/)
