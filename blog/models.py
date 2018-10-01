from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .search import PolicyIndex
from django.db.models.signals import post_save
from django.dispatch import receiver

class Policy(models.Model):

    POSSIBLE_TAGS = (
        ('diversity', 'Diversity'),
        ('admissions', 'Admissions'),
        ('enrollment', 'Enrollment'),
        ('faculty', 'Faculty'),
        ('student affairs', 'Student Affairs'),
        ('administrative', 'Administrative'),
        ('fees', 'Fees'),
        ('data measures', 'Data Measures'),
        ('international students', 'International Students'),
        ('academic standards', 'Academic Standards'),
        ('athletics', 'Athletics'),
        ('title ix', 'Title IX'),
        ('accreditation', 'Accreditation')
    )

    title = models.TextField(blank=True)
    school = models.CharField(max_length=255)
    department = models.TextField(blank=True)
    administrator = models.TextField(blank=True)
    author = models.TextField(blank=True)
    state = models.TextField(blank=True)
    city = models.TextField(blank=True)
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    link = models.TextField(blank=True)
    published_date = models.DateField(blank=True, null=True)
    tags = models.CharField(choices=POSSIBLE_TAGS, max_length=255)
    abstract = models.TextField(blank=True)
    text = models.TextField(blank=True)

    # Add indexing method to Policy
    def indexing(self):
        obj = PolicyIndex(
            meta={'id': self.id},
            title = self.title,
            school = self.school,
            department = self.department,
            administrator = self.administrator,
            author = self.author,
            state = self.state,
            city = self.city,
            latitude = self.latitude,
            longitude = self.longitude,
            link = self.link,
            published_date = self.published_date,
            tags = self.tags,
            abstract = self.abstract,
            text = self.text
        )
        obj.save(index='policy-index')
        return obj.to_dict(include_meta=True)

    def publish(self):
        self.save()

    def __str__(self):
        return self.title
