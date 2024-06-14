# Setup

## 1. Settings.py:
- Add ```cottonLogger``` to ```INSTALLED APPS```.
- Add ```AUTH_USER_MODEL = "cottonLogger.CustomUser"``` to use the custom login system:
    ```
    AUTH_USER_MODEL = "cottonLogger.CustomUser"
    ```
- Add ```'cottonLogger.authentication.TokenCheckBackend'``` to ```AUTHENTICATION_BACKENDS``` for hash based login:
    ```
    AUTHENTICATION_BACKENDS = [
        'django.contrib.auth.backends.ModelBackend',
        'cottonLogger.authentication.TokenCheckBackend',
    ]
    ```
- If you want to close user sessions at Browser Close add:
    ```
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True
    ```

## 2. Run:
- ```$ python manage.py makemigrations```
- ```$ python manage.py migrate```
- ```$ python manage.py createsuperuser``` to create a new superuser with the custom model.

<br> <br> <br>

# Usage

## Models
- ```CustomUser```: replacement for the default user using email as username.
- ```AccessToken```: token for user login.

## Settings
- ```SHORT_HASH_LEN```: How many characters will be saved in the database (for searching)
- ```DEFAULT_TOKEN_EXPIRATION_TIME```: How many time has the user to log in with a token. Can be override on token creation.
- ```TOKEN_CREATION_DELAY_TIME```: Time between token creation (used in ```checkCreationLimit```).

## Functions
From ```tokenizer.py```:

- ```findSpecificToken```:
    Find the specific owner of the hash. <br>
    **Args**: fullhash (str) <br>
    **Returns**:
        AccessToken | None: The access token, None if not found.

- ```findUser```:
    Find user by email. <br>
    **Args**: email (str) <br>
    **Returns**: CustomUser | None: The user, None if not found.

- ```findValidToken```:
    Find the actual valid token for a user <br>
    **Args**: user (CustomUser) <br>
    **Returns**: AccessToken | None: The access token, None if not found.

- ```checkCreationLimit```:
    Checks actual token against TOKEN_CREATION_DELAY_TIME. <br>
    **Args**: user (CustomUser) <br>
    **Returns**: bool: true if the user should be allowed to create a new token.

<br> <br> <br>

> (c) CottonSP 2023

