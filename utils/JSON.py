import json

class JSON:
    @staticmethod
    def serialize(class_):
        return json.dumps(class_, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def serialize_ast(class_):
        statements = JSON.serialize(class_)
        for statement in statements:
            print(statement.to_string())