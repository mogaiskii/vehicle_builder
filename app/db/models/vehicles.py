from __future__ import annotations

from typing import List

from db.models import Component, Feature, Function
from db.models.base import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import relation


class VehicleFeatures(BaseModel):
    __tablename__ = 'vehicle_features'

    vehicle_id = Column(Integer, ForeignKey('vehicles.id'), nullable=False)
    feature_id = Column(Integer, ForeignKey('features.id'), nullable=False)
    feature: Feature = relation(Feature, uselist=False)

    vehicle_functions: List[VehicleFunctions] = relation('VehicleFunctions')


class VehicleFunctions(BaseModel):
    __tablename__ = 'vehicle_functions'

    vehicle_feature_id = Column(Integer, ForeignKey('vehicle_features.id'), nullable=False)
    function_id = Column(Integer, ForeignKey('functions.id'), nullable=False)
    function: Function = relation(Function, uselist=False)

    vehicle_components: List[VehicleComponents] = relation(
        'VehicleComponents',
        secondary='vehicle_function_components'
    )


class VehicleFunctionComponents(BaseModel):
    __tablename__ = 'vehicle_function_components'

    vehicle_function_id = Column(Integer, ForeignKey('vehicle_functions.id'), nullable=False)
    vehicle_component_id = Column(Integer, ForeignKey('vehicle_components.id'), nullable=False)


class VehicleComponents(BaseModel):
    __tablename__ = 'vehicle_components'

    vehicle_id = Column(Integer, ForeignKey('vehicles.id'), nullable=False)
    component_id = Column(Integer, ForeignKey('components.id'), nullable=False)
    component: Component = relation(Component, uselist=False)
    component_amount = Column(Integer, nullable=False)


class Vehicle(BaseModel):
    __tablename__ = 'vehicles'

    name = Column(String(128), nullable=False)
    meta_data = Column(JSON)

    vehicle_features: List[VehicleFeatures] = relation(VehicleFeatures, uselist=True)
