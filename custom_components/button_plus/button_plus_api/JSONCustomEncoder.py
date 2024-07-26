import json


# Python MAGIC to be able to use NORMAL serialisation (-:
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "to_dict"):
            return obj.to_dict()
        return super().default(obj)
