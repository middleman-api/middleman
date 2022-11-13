from passlib.hash import bcrypt
from tortoise import fields

from middleman.utilities.models import TimestampedModel


class User(TimestampedModel):
    id = fields.IntField(pk=True)
    username = fields.CharField(50, unique=True)
    password_hash = fields.CharField(128)

    class Meta:
        ordering = ["-id"]

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)

    class PydanticMeta:
        exclude = ("created_at", "updated_at")
