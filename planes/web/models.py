import uuid
from django.contrib.postgres.search import (SearchQuery, SearchRank,
    SearchVector)
from django.db import models

class PoliticalOrganization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
        editable=False)
    code = models.CharField(max_length=20)
    name = models.TextField()

    def __str__(self):
        return self.name

class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
        editable=False)
    author = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    pages = models.PositiveSmallIntegerField(null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    tokens = models.JSONField(null=True, blank=True)
    political_organization = models.ForeignKey(PoliticalOrganization,
        on_delete=models.CASCADE, related_name='documents')

    def __str__(self):
        return f"{self.political_organization} - {self.name}"

class SentenceManager(models.Manager):
    def search(self, words):
        vector = SearchVector('text')
        query = SearchQuery(words[0])
        for word in words[1:]:
            query = query | SearchQuery(word)
        rank = SearchRank(vector, query)
        return self.annotate(rank=rank).filter(rank__gt=0.0).order_by('-rank')

class Sentence(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
        editable=False)
    number = models.PositiveSmallIntegerField()
    text = models.TextField(null=True, blank=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE,
        related_name='paragraphs')

    objects = SentenceManager()

    def __str__(self):
        return f"{self.document} - {self.number}"