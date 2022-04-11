from __future__ import annotations

from typing import List, Set, Optional

from pydantic import BaseModel

from db.models import Vehicle, VehicleFeatures


class BaseResponseModel(BaseModel):
    id: int
    name: str


class ComponentResponseModel(BaseResponseModel):
    component_amount: int

    class Config:
        orm_mode = True


class FunctionResponseModel(BaseResponseModel):
    components_ids: List[int]


class FeatureResponseModel(BaseResponseModel):
    components: List[ComponentResponseModel]
    functions: List[FunctionResponseModel]

    @classmethod
    def from_orm(cls, obj: VehicleFeatures) -> FeatureResponseModel:
        components: List[ComponentResponseModel] = []
        added_components: Set[Optional[int]] = set()
        functions: List[FunctionResponseModel] = []

        for vehicle_function in obj.vehicle_functions:
            function_component_ids: List[Optional[int]] = []

            for vehicle_component in vehicle_function.vehicle_components:
                function_component_ids.append(vehicle_component.component.id)

                if vehicle_component.component.id not in added_components:
                    components.append(
                        ComponentResponseModel(
                            id=vehicle_component.component.id,
                            name=vehicle_component.component.name,
                            component_amount=vehicle_component.component_amount
                        )
                    )

            functions.append(
                FunctionResponseModel(
                    id=vehicle_function.function.id,
                    name=vehicle_function.function.name,
                    components_ids=function_component_ids
                )
            )

        return cls(id=obj.feature.id, name=obj.feature.name, components=components, functions=functions)

    class Config:
        orm_mode = True


class VehicleResponseModel(BaseResponseModel):
    features: List[FeatureResponseModel]

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, obj: Vehicle) -> VehicleResponseModel:
        return VehicleResponseModel(
            id=obj.id, name=obj.name, features=[
                FeatureResponseModel.from_orm(feature) for feature in obj.vehicle_features
            ]
        )
