from typing import List

from db.models.base import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relation

from . import Component, Feature


class FunctionComponent(BaseModel):
    __tablename__ = 'function_components'

    function_id = Column(Integer, ForeignKey('functions.id'), nullable=False)
    component_id = Column(Integer, ForeignKey('components.id'), nullable=False)


class Function(BaseModel):
    __tablename__ = 'functions'

    name = Column(String(128), nullable=False)
    feature_id = Column(Integer, ForeignKey('features.id'), nullable=False)
    feature: Feature = relation(Feature)
    components: List[Component] = relation(
        Component,
        secondary=FunctionComponent.__tablename__,
        uselist=True
    )
