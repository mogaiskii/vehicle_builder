from db.models.base import BaseModel
from sqlalchemy import Column, JSON, String


class Component(BaseModel):
    __tablename__ = 'components'

    name = Column(String(128), nullable=False)
    cad_model_url = Column(String(128), nullable=False)
    parameters = Column(JSON)
