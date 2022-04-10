from __future__ import annotations

from typing import List, TYPE_CHECKING

from db.models.base import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relation

from . import Group, Set

if TYPE_CHECKING:
    from .functions import Function


class Feature(BaseModel):
    __tablename__ = 'features'

    name = Column(String(128), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=True)
    group: Group = relation(Group, uselist=False)

    set_id = Column(Integer, ForeignKey('sets.id'), nullable=True)
    set: Set = relation(Set, uselist=False)

    functions: List[Function] = relation('Function')
