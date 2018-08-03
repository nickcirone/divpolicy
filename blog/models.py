from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


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

    title = models.CharField(max_length=300)
    school = models.CharField(max_length=300)
    department = models.CharField(max_length=300, blank=True)
    administrator = models.CharField(max_length=300, blank=True)
    author = models.CharField(max_length=300, blank=True)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()
    link = models.URLField()
    published_date = models.DateField(blank=True)
    tags = models.CharField(choices=POSSIBLE_TAGS)
    abstract = models.TextField(blank=True)
    text = models.TextField()

    def publish(self):
        self.save()

    def __str__(self):
        return self.title
