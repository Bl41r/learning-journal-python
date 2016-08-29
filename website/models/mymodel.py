from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
)

from .meta import Base


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    body = Column(Text)
    creation_date = Column(Text)


Index('my_index', MyModel.id, unique=True, mysql_length=255)
