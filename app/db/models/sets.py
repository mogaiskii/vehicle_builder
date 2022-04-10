from db.models.base import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relation

from . import Group


class Set(BaseModel):
    __tablename__ = 'sets'

    name = Column(String(128), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    group: Group = relation(Group, uselist=False)
