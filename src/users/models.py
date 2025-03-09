from firebase.models import AbstractFirebaseUser


class User(AbstractFirebaseUser):
    
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'