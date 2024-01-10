from marshmallow import Schema, fields, validates_schema, ValidationError


# Schéma chanson de sortie (renvoyé au front)

class SongSchema(Schema):

    id = fields.String(description="UUID")
    title = fields.String(description="Title")
    artist = fields.String(description="Artist")
    filename = fields.String(description="Filename")
    published = fields.String(description="Published")

    @staticmethod
    def is_empty(obj):
        return (not obj.get("id") or obj.get("id") == "") and \
               (not obj.get("title") or obj.get("title") == "") and \
               (not obj.get("artist") or obj.get("artist") == "") and \
               (not obj.get("filename") or obj.get("filename") == "") and \
               (not obj.get("published") or obj.get("published") == "")
    

class BaseSongSchema(Schema):
    title = fields.String(description="Title")
    artist = fields.String(description="Artist")
    filename = fields.String(description="Filename")
    published = fields.String(description="Published")


# Schéma chanson de modification (title, artist, filename, published)
class SongUpdateSchema(BaseSongSchema):
    # permet de définir dans quelles conditions le schéma est validé ou nom
    @validates_schema
    def validates_schemas(self, data, **kwargs):
        if not (("title" in data and data["title"] != "") or
                ("artist" in data and data["artist"] != "") or
                ("filename" in data and data["filename"] != "") or
                ("published" in data and data["published"] != "")):
            raise ValidationError("at least one of ['title','artist','filename','published'] must be specified")


    