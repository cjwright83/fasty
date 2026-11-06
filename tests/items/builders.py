from faker import Faker

from fasty.items.sql_models import Item

fake = Faker()


def build_item(**attrs) -> Item:
    return Item(
        name=attrs.get("name", fake.name()),
        description=attrs.get("description", fake.text()),
        price=attrs.get("price", fake.pyfloat()),
        is_offer=attrs.get("is_offer", fake.boolean()),
    )
