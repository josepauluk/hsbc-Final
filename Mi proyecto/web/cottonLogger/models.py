from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.db.models.signals import post_init
from hashlib import sha512
from uuid import uuid4

from .managers import CustomUserManager
from .settings import SHORT_HASH_LEN, DEFAULT_TOKEN_EXPIRATION_TIME


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("email address", unique=True)
    first_name = models.CharField(max_length=86, default='')
    last_name = models.CharField(max_length=86, default='')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class AccessToken(models.Model):
    token = models.UUIDField(primary_key=True, default=uuid4)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False)
    is_active = models.BooleanField(default=True, null=False)
    shortcut_hash = models.CharField(max_length=SHORT_HASH_LEN, null=False, default='')
    created_on = models.DateTimeField(default=timezone.now)
    expires_on = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"[{'ACTIVE' if self.is_active else '      '}] {self.shortcut_hash}... <{self.owner}>"

    def getHash(self) -> str:
        """
        Returns:
            str: fullhash
        """
        base = (self.owner.email + self.token.hex).encode()
        return str(sha512(base, usedforsecurity=True).hexdigest())
    
    def checkHash(self, fullhash: str) -> bool:
        """
        Args:
            fullhash (str)
    
        Returns:
            bool: true if fullhash is correct
        """
        return self.getHash() == fullhash
    
    def checkExpiration(self) -> bool:
        """
        Returns:
            bool: true if the token has not expired
        """
        return ( self.expires_on > timezone.now() )
    
def AccessCreation(**kwargs):
    instance = kwargs.get('instance')
    if instance.shortcut_hash == '':
        # update other tokens
        for tkn in AccessToken.objects.filter(owner=instance.owner):
            if tkn.token != instance.token:
                tkn.is_active = False
                tkn.save()
        # create shortcut
        instance.shortcut_hash = instance.getHash()[:SHORT_HASH_LEN]
        # expiration
        instance.expires_on += DEFAULT_TOKEN_EXPIRATION_TIME

post_init.connect(AccessCreation, AccessToken)

