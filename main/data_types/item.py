class Item():

    def __init__(self, data=None):
        self.price = None
        self.view_price = None
        self.is_second_hand = None
        self.creation_date = None
        self.is_deleted = None
        self.deletion_date = None
        self.title = None
        self.link = None
        self.owner_details = None
        self.name = None
        self.description = None

        if data:
            attr_dict = dict(self.__dict__)
            for attr_key in attr_dict:
                if attr_key in data:
                    self.__dict__[attr_key] = data[attr_key]
                    # setattr(self, attr_key, data[attr_key])

    def to_json(self):
        json_data = {}
        attr_dict = dict(self.__dict__)
        for attr_key, attr_value in attr_dict.items():
            json_data[attr_key] = attr_value

        return json_data

    def __str__(self):
        return str(self.to_json())


if __name__ == '__main__':
    i = Item()
    print i.to_json()