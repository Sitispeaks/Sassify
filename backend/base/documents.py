# talks/documents.py
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Product
from django.contrib.auth.models import User

# PRODUCT_INDEX= Index('products')
# PRODUCT_INDEX.settings(number_of_shards=1, number_of_replicas=1)




@registry.register_document
class ProductDocument(Document):


    class Index:
        # Name of the Elasticsearch index
        name = 'product_index3'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 1}

    # name = fields.TextField(attr='get_absolute_name')

    class Django:
        model = Product
        # related_model = [User]
        fields = [
                'id',
                'name',
                'image',
                'brand',
                'category',
                'description',
                'rating',
                'numReviews',
                'countInStock',
                'price'
        ]

      
       