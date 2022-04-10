from __future__ import annotations

from typing import List, TYPE_CHECKING

from db.models.base import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relation

if TYPE_CHECKING:
    from .features import Feature
    from .sets import Set


class Group(BaseModel):
    __tablename__ = 'groups'

    name = Column(String(128), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'))

    subgroups: List[Group] = relation('Group')
    sets: List[Set] = relation('Set')
    features: List[Feature] = relation('Feature')
