import json


class UpdateStruct(object):
    def __init__(self, name, data):
        self._ = name
        self.__dict__.update(data)

    def __str__(self):
        return self.jsonify()

    def jsonify(self, indent=None):
        return json.dumps(self.__dict__, indent=indent,
                          ensure_ascii=False,
                          default=lambda x: str(x))

    def __getattr__(self, key):
        try:
            return super(UpdateStruct, self).__getattribute__(key)
        except AttributeError:
            return None

    def __getattribute__(self, key=None, value=None):
        if isinstance(key, str):
            if key.startswith('__') and key.endswith('__'):
                raise AttributeError

            value = super(UpdateStruct, self).__getattribute__(key)
        if isinstance(value, list):
            result = []
            for item in value:
                if isinstance(item, dict):
                    result.append(UpdateStruct(self._, item))

                elif isinstance(item, list):
                    result.append(self.__getattribute__(value=item))
                else:
                    result.append(item)

            return result

        elif isinstance(value, dict):
            value = UpdateStruct(key, value)

        return value

    def __getitem__(self, item):
        return self.__dict__.get(item)