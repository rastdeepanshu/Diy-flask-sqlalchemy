from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import sessionmaker

Base = declarative_base()

engine = create_engine('sqlite:////Users/drastogi/restaurant.db', echo=True)

Session = sessionmaker(bind=engine)

restaurant_owner = Table('restaurant_owner', Base.metadata,
                         Column('restaurant_id', Integer, ForeignKey('restaurant.id')),
                         Column('owner_id', Integer, ForeignKey('owner.id'))
                         )


def delete_restaurant(id):
    return "delete from restaurant_owner where restaurant_id="+id


def delete_owner(id):
    return "delete from restaurant_owner where owner_id="+id


class Restaurant(Base):
    __tablename__ = 'restaurant'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    address = Column(String)
    owners = relationship("Owner", secondary=restaurant_owner)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'owners': self.serialize_owners
        }

    @property
    def serialize_owners(self):
        return [owner.serialize for owner in self.owners]


class Owner(Base):
    __tablename__ = 'owner'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender


    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }


if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)