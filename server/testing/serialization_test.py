from app import app, db
from server.models import Customer, Item, Review

class TestSerialization:
    '''Tests for models serialization'''

    def test_item_is_serializable(self):
        '''Test serialization of Item model'''
        with app.app_context():
            i = Item(name='Insulated Mug', price=9.99)
            db.session.add(i)
            db.session.commit()

            # Add a review for the item
            r = Review(comment='great!', item=i)
            db.session.add(r)
            db.session.commit()

            item_dict = i.to_dict()

            assert item_dict['id']
            assert item_dict['name'] == 'Insulated Mug'
            assert item_dict['price'] == 9.99
            assert 'reviews' in item_dict
            assert len(item_dict['reviews']) == 1
            assert 'item' not in item_dict['reviews'][0]

    