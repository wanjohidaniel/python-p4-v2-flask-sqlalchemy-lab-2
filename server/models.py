from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    
    # Relationship with Review model
    reviews = relationship('Review', back_populates='customer')
    
    # Association proxy to access items through reviews
    items = association_proxy('reviews', 'item')

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'items': [item.to_dict_no_reviews() for item in self.items if item],
            'reviews': [review.to_dict_no_customer() for review in self.reviews]
        }

    def to_dict_no_reviews(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def serialize(self):
        return SerializerMixin.serialize(self, exclude=('reviews.customer', 'reviews.item.reviews', 'reviews.item.reviews.item'))

class CustomerItem(db.Model):
    __tablename__ = 'customer_items'

    customer_id = db.Column(db.Integer, ForeignKey('customers.id'), primary_key=True)
    item_id = db.Column(db.Integer, ForeignKey('items.id'), primary_key=True)
    
    customer = relationship('Customer', backref='customer_items')
    item = relationship('Item')

class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    
    # Relationship with Review model
    reviews = relationship('Review', back_populates='item')

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'reviews': [review.to_dict_no_item() for review in self.reviews]
        }

    def to_dict_no_reviews(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price
        }

    def serialize(self):
        return SerializerMixin.serialize(self, exclude=('reviews.item', 'reviews.customer.reviews', 'reviews.customer.reviews.customer'))

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    customer_id = db.Column(db.Integer, ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, ForeignKey('items.id'))
    
    # Relationship with Customer model
    customer = relationship('Customer', back_populates='reviews')
    
    # Relationship with Item model
    item = relationship('Item', back_populates='reviews')

    def __repr__(self):
        return f'<Review {self.id}, {self.comment}>'

    def to_dict(self):
        return {
            'id': self.id,
            'comment': self.comment,
            'customer': self.customer.to_dict_no_reviews(),
            'item': self.item.to_dict_no_reviews()
        }

    def to_dict_no_customer(self):
        return {
            'id': self.id,
            'comment': self.comment,
            'item_id': self.item_id
        }

    def to_dict_no_item(self):
        return {
            'id': self.id,
            'comment': self.comment,
            'customer_id': self.customer_id
        }

    def serialize(self):
        return SerializerMixin.serialize(self, exclude=('customer.reviews', 'item.reviews'))
