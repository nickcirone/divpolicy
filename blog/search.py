from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Date, Search
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from . import models
import csv
from django.contrib.auth.models import User

connections.create_connection()

class PolicyIndex(DocType):
    title = Text()
    school = Text()
    department = Text()
    administrator = Text()
    author = Text()
    state = Text()
    city = Text()
    latitude = Text()
    longitude = Text()
    link = Text()
    published_date = Date()
    tags = Text()
    abstract = Text()
    text = Text()


def bulk_indexing():
    PolicyIndex.init(index='policy-index')
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing() for b in models.Policy.objects.all().iterator()))
    #code to go into the csv file of data and add it to elasticsearch
    #user_test = User.objects.create_user('Test_Usert', 'test_user@gmail.com', 'test_password')
    f = open('policy.csv', encoding="ISO-8859-1")
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        #handling of improperly formatted date entries
        row[11] = "1111-11-11"
        # handling of weird characters appearing in lat and long entries
        row[8] = float(row[8][:2])
        row[9] = float(row[9][:2])
        blog = models.Policy.objects.get_or_create(title=row[1], school=row[2], department=row[3], administrator=row[4], author=row[5], state=row[6], city=row[7], latitude=row[8], longitude=row[9], link=row[10], published_date=row[11], tags=row[12], abstract=row[13], text=row[14])[0]
        pass

def search(term):
    s = Search().filter('match_phrase', school=term)
    response = s.execute()
    return response
