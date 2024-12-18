from enum import Enum as PyEnum


class SearchType(PyEnum):

    """
    Enum representing search types.
    """
    USERNAME = "username"
    EMAIL = "email"
    ROLE = "role"