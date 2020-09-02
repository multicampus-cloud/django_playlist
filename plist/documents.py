from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Song

@registry.register_document
class SongDocument(Document):
    class Index:
        name = 'songs'
        settings = {'number_of_shards':1,
                    'number_of_replicas':0
                    }

    class Django:
        model = Song

        fields = [
            'song_title',
            'song_artist',
            'song_genre',
            'song_tag',
            'song_thumbnail',
            'id',
        ]
