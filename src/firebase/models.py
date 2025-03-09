# builtin
# builtins
import uuid

# django
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

# third party
from phonenumber_field.modelfields import PhoneNumberField

# local
from .managers import UserManager


class AbstractFirebaseUser(AbstractBaseUser, PermissionsMixin):
    uid = models.CharField(unique=True, default=uuid.uuid1, max_length=50)
    display_name = models.CharField(
        'full name',
        max_length=100,
        null=True,
        blank=True,
    )

    email = models.EmailField(
        'email address',
        unique=True,
        null=True,
        blank=True,
        default=None,
        error_messages={
            'unique': "A user with this email address already exists.",
        },
    )

    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text='Designates whether this user should be treated as active. '
        'Unselect this instead of deleting accounts.',
    )
    date_joined = models.DateTimeField('date joined', default=timezone.now)
    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'uid'
    REQUIRED_FIELDS = []

    class Meta:
        abstract = True

    def get_username(self):
        return f'{self.identifier}'

    def clean(self):
        self.email = self.__class__.objects.normalize_email(self.email)

    @property
    def identifier(self):
        return self.display_name or self.email or self.uid

    def save(self, *args, **kwargs):
        self._set_null_default()

        return super().save(*args, **kwargs)

    def _set_null_default(self):
        """ `EmailField` won't be set to null by default,
            we set it to null if the value is '' to avoid unique constraint
            https://docs.djangoproject.com/en/3.2/ref/models/fields/#null
        """
        self.email = None if self.email == '' else self.email


class FirebaseUser(AbstractFirebaseUser):
    """ Firebase User for Direct use  """

    class Meta(AbstractFirebaseUser.Meta):
        swappable = 'AUTH_USER_MODEL'
