from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Date, Search
from elasticsearch_dsl.query import MultiMatch, Match
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

# if bulk_indexing() doesn't work due to space, try running
# curl -XPUT -H "Content-Type: application/json" http://localhost:9200/_all/_settings -d '{"index.blocks.read_only_allow_delete": null}'

def bulk_indexing():
    PolicyIndex.init(index='policy-index')
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing() for b in models.Policy.objects.all().iterator()))
    # code to go into the csv file of data and add it to elasticsearch
    f = open('policy.csv', encoding="ISO-8859-1")
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        # handling of improperly formatted date entries
        # this assumes that dates are being entered into the database as MM/DD/YY (as the first couple thousand were)
        # and it formats them correctly in order to use Date() in elasticsearch. Since only two digits being
        # entered for year, assumes numbers <19 correspond to 21st century and rest to 20th.
        # Assigns 'None' when no date entered.
        date = row[11]
        date = date.split("/")
        try:
            if int(date[2]) < 19:
                date[2] = "20" + date[2]
            else:
                date[2] = "19" + date[2]
            date = date[2] + "-" + date[0] + "-" + date[1]
        except:
            #date = "1111-11-11"
            date = None
        row[11] = date
        # handling of weird characters appearing in lat and long entries
        try:
            row[8] = float(row[8][:2])
            row[9] = float(row[9][:2])
        except:
            row[8] = ""
            row[9] = ""
        print(row[11])
        blog = models.Policy.objects.get_or_create(title=row[1], school=row[2], department=row[3], administrator=row[4],
                                                   author=row[5], state=row[6], city=row[7], latitude=row[8],
                                                   longitude=row[9], link=row[10], published_date=row[11], tags=row[12],
                                                   abstract=row[13], text=row[14])[0]
        pass

def search(query):
    s = Search(index ='policy-index').query("multi_match", query=query,
                                           fields=["title", "school", "department", "administrator", "author", "state",
                                                   "city", "latitude", "longitude", "link", "tags", "abstract", "text"])
    response = s.execute()
    return response

# going to output a list of strings that represent suggestions based off what has been currently entered to search
# by the user -- can be used for search suggestion
# similar to search(), this method will be used in views.py or a similar file that interacts with the html

# currently returns an error
def get_search_suggestions(query):
    es = Search(index = 'policy_index')
    suggestions = es.suggest(name = 'policy-index', text = {"title": query})[0]["options"]
    suggestions = [suggest['text'] for suggest in suggestions]
    print(suggestions)
    return suggestions