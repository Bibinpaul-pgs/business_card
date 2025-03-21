from django.db import models
from core.models import BaseModel
from users.models import User
# Create your models here.

class CardKind(models.IntegerChoices):
    PUBLIC = 1
    PRIVATE = 2


class CardFile(BaseModel):
    file = models.FileField(upload_to="cards/file")

    def __str__(self):
        return str(self.id)


class Card(BaseModel):
    file = models.ForeignKey(CardFile, on_delete=models.CASCADE, related_name='card')
    profile_image = models.FileField(upload_to="cards/profile_image", null=True, blank=True)
    full_name = models.CharField(max_length=300, null=True, blank=True)
    designation = models.CharField(max_length=300, null=True, blank=True)
    company_name = models.CharField(max_length=500, help_text='Company/Organisation name', null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    location_details = models.TextField(null=True, blank=True)
    card_type = models.IntegerField(choices=CardKind, default=CardKind.PRIVATE)
    social_media_links = models.JSONField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='cards')

    requests = models.ManyToManyField(User, through="CardRequest")

    def __str__(self):
        return str(self.id)



class CardRequest(BaseModel):
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["requested_by", "card"], name="unique_card_request"
            )
        ]

    

class MyHolder(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_holder')
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='my_holder')

    def __str__(self):
        return str(self.id)