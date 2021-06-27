from tortoise import fields 
from tortoise.models import Model

from ..utilities.models import TimestampedModel

class Site(TimestampedModel):
    id = fields.IntField(pk=True)
    url = fields.CharField(253)
    owner = fields.ForeignKeyField('models.User', related_name='sites')

    def get_base_url(self):
        return self.url

    class Meta:
        ordering = ["-id"]

class ApiHit(TimestampedModel):
    id = fields.IntField(pk=True)
    site = fields.ForeignKeyField('models.Site', related_name='api_hits')
    method = fields.CharField(20, null=True)
    request_data = fields.data.TextField(null=True)
    response_data = fields.data.TextField(null=True)
    
    class Meta:
        ordering = ["-id"]
    
    def get_base_url(self):
        return self.url