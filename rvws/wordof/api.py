__author__ = 'gardenm'

from tastypie import fields
from tastypie.resources import ModelResource
from wordof.models import *


class ArtistResource(ModelResource):
    class Meta:
        queryset = Artist.objects.all()
        resource_name = 'artist'


class ArtifactResource(ModelResource):
    artist = fields.ForeignKey(ArtistResource, 'artist')

    class Meta:
        queryset = Artifact.objects.all()
        resource_name = 'artifact'


class CriticResource(ModelResource):
    class Meta:
        queryset = Critic.objects.all()
        resource_name = 'critic'


class CategoryResource(ModelResource):
    critic = fields.ForeignKey(CriticResource, 'critic')

    class Meta:
        queryset = Category.objects.all()
        resource_name = 'category'


class ReviewResource(ModelResource):
    artifact = fields.ForeignKey(ArtifactResource, 'artifact')
    source = fields.ForeignKey(CategoryResource, 'source')

    class Meta:
        queryset = Review.objects.all()
        resource_name = 'review'

