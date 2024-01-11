from marshmallow import Schema, fields, validates_schema, ValidationError


#shéma rating de sortie (renvoyé au front)

class RatingSchema(Schema):
    
        id = fields.String(description="UUID")
        user_id = fields.String(description="User id")
        song_id = fields.String(description="Song id")
        comment = fields.String(description="Comment")
        rating_date = fields.String(description="Date")
        rating = fields.Integer(description="Rating")
    
        @staticmethod
        def is_empty(obj):
            return (not obj.get("id") or obj.get("id") == "") and \
                (not obj.get("user_id") or obj.get("user_id") == "") and \
                (not obj.get("song_id") or obj.get("song_id") == "") and \
                (not obj.get("comment") or obj.get("comment") == "") and \
                (not obj.get("rating_date") or obj.get("rating_date") == "") and \
                (not obj.get("rating") or obj.get("rating") == "")
        
class BaseRatingSchema(Schema):
    user_id = fields.String(description="User id")
    song_id = fields.String(description="Song id")
    comment = fields.String(description="Comment")
    rating_date = fields.String(description="Date")
    rating = fields.Integer(description="Rating")

# Schéma rating de modification (content, date, rating)
class RatingUpdateSchema(BaseRatingSchema):
    # permet de définir dans quelles conditions le schéma est validé ou nom
    @validates_schema
    def validates_schemas(self, data, **kwargs):
        if not (("comment" in data and data["comment"] != "") or
                ("rating_date" in data and data["rating_date"] != "") or
                ("rating" in data and data["rating"] != "")):
            raise ValidationError("at least one of ['comment','rating_date','rating'] must be specified")
        