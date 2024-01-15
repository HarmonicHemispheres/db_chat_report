"""
Module containing IdsUserDTO class definition
"""

class IdsUserDTO():
    """[summary]

    [description]
    """
    def __init__(self):
        self.user_name = ""
        self.company_name = ""
        self.user_id_public = ""
        self.client_id_public = ""
        self.roles = list()
        self.known_client_ids = {} # holds quick lookup of integer id : client_id

    def __str__(self):
        return str.format("(IdsUserDTO) name:{0} id:{1} co:{2} client_id:{3} roles:{4}"
                          , self.user_name, self.user_id_public, self.company_name
                          , self.client_id_public, len(self.roles))

    @classmethod
    def create(cls, response_json):
        """Creates a IdsUserDTO instance based on response_json.

        Method will return an empty instance if no json is passed.
        response_json is from the response of the API call /api/User/Generic

        Arguments:
            response_json {dict} -- dict representing the json of a web response
        """
        if response_json is None or response_json == "":
            return cls() # return empty new instance

        user = cls()
        user.user_name = response_json['UserName']

        claims = response_json['Claims']
        for claim in claims:
            if claim.get('Key') == 'UserIDPublic':
                user.user_id_public = claim['Value']
            elif claim.get('Key') == 'ClientIdPublic':
                user.client_id_public = claim['Value']
            elif claim.get('Key') == 'CompanyName':
                user.company_name = claim['Value']
            elif claim.get('Key') == 'role':
                user.roles.append(claim['Value'])

        return user

    def has_any_role(self, requested_roles):
        """Evaluates if the IdsUser has any of the requested roles.

        Arguments:
            requested_roles {string} -- comma delimited string e.g. "Role1, Role2"

        Returns:
            [bool] -- True if IdsUser has any role in requested roles str.
        """
        for role in requested_roles.split(','):
            role = role.strip()
            if role in self.roles:
                return True

        return False

    def has_all_roles(self, requested_roles):
        """Evaluates if the IdsUser has all of the requested roles.

        Arguments:
            requested_roles {string} -- comma delimited string e.g. "Role1, Role2"

        Returns:
            [bool] -- True if IdsUser has all roles in requested roles str.
        """
        for role in requested_roles.split(','):
            role = role.strip()
            if role not in self.roles:
                return False

        return True
