from django.contrib.auth.backends import BaseBackend

from .models import CustomUser
from .tokenizer import findSpecificToken


class TokenCheckBackend(BaseBackend):
    def authenticate(self, request, fullhash=None):
        token = findSpecificToken(fullhash)
        
        if token is not None:
            expirCheck = token.checkExpiration()
            activCheck = token.is_active
            
            if expirCheck and activCheck:
                token.is_active = False
                token.save()
                return token.owner
            
        return None
        
        
    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            pass
        return None