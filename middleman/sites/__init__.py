from tortoise import fields
from tortoise.models import Model


class Site(Model):
    id = fields.IntField(pk=True)
    url = fields.CharField(253)
    owner = fields.ForeignKeyField('models.User', related_name='sites')

    def get_base_url(self):
        return self.url


class ApiHit(Model):
    id = fields.IntField(pk=True)
    site = fields.ForeignKeyField('models.Site', related_name='api_hits')
    method = fields.CharField(20, null=True)
    request_data = fields.data.TextField(null=True)
    response_data = fields.data.TextField(null=True)
    request_headers = fields.data.TextField(null=True)
    response_headers = fields.data.TextField(null=True)

    def get_base_url(self):
        return self.url