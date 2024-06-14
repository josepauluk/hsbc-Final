from django.utils import timezone
from .models import CustomUser, AccessToken

from .settings import SHORT_HASH_LEN, TOKEN_CREATION_DELAY_TIME

#### ------ TOKEN  FUNCTIONS ------ ####
def findSpecificToken(fullhash: str) -> AccessToken | None:
    """
    Find the specific owner of the hash.

    Args:
        fullhash (str)

    Returns:
        AccessToken | None: The access token, None if not found.
    """
    try:
        tokens = AccessToken.objects.filter(shortcut_hash=fullhash[:SHORT_HASH_LEN])
        for tk in tokens:
            if tk.checkHash(fullhash):
                return tk
    except:
        pass
    return None


def findUser(email: str) -> CustomUser | None:
    """
    Find user by email.

    Args:
        email (str)

    Returns:
        CustomUser | None: The user, None if not found.
    """
    try:
        return CustomUser.objects.get(email=email)
    except:
        pass
    return None


def findValidToken(user: CustomUser) -> AccessToken | None:
    """
    Find the actual valid token for a user

    Args:
        user (CustomUser)

    Returns:
        AccessToken | None: The access token, None if not found.
    """
    try:
        active = AccessToken.objects.filter(owner=user).get(is_active=True)
        if active.checkExpiration():
            return active
    except:
        pass
    return None


def checkCreationLimit(user: CustomUser) -> bool:
    """
    Checks actual token against TOKEN_CREATION_DELAY_TIME.

    Args:
        user (CustomUser)

    Returns:
        bool: true if the user should be allowed to create a new token.
    """
    active = findValidToken(user)
    if active is not None:
        limit = active.created_on + TOKEN_CREATION_DELAY_TIME
        if limit > timezone.now():
            return False
    return True
#### ------------------------------ ####
