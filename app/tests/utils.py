import random
from typing import TypeVar, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from faker import Faker

from db.models import Vehicle, Component, Group, Feature, Function, FunctionComponent, VehicleFeatures, \
    VehicleFunctions, VehicleComponents, VehicleFunctionComponents, Base


TModel = TypeVar('TModel', bound=Base)


_fake = Faker()


async def save(session: AsyncSession, item: TModel) -> TModel:
    session.add(item)
    await session.flush()
    return item


def with_save(function):  # type: ignore
    async def wrapper(session: AsyncSession, *args, **kwargs) -> TModel:  # type: ignore
        result: TModel = await function(session, *args, **kwargs)
        return await save(session, result)
    return wrapper


@with_save
async def create_component(session: AsyncSession) -> Component:
    return Component(name=_fake.name(), cad_model_url=_fake.image_url())


@with_save
async def create_group(session: AsyncSession) -> Group:
    return Group(name=_fake.name())


@with_save
async def create_feature(session: AsyncSession, group_id: Optional[int]) -> Feature:
    return Feature(name=_fake.name(), group_id=group_id)


@with_save
async def create_function(session: AsyncSession, feature_id: Optional[int]) -> Function:
    return Function(name=_fake.name(), feature_id=feature_id)


@with_save
async def bind_function_component(
        session: AsyncSession, function_id: Optional[int], component_id: Optional[int]
) -> FunctionComponent:
    return FunctionComponent(function_id=function_id, component_id=component_id)


@with_save
async def create_vehicle(session: AsyncSession) -> Vehicle:
    return Vehicle(name=_fake.name())


@with_save
async def bind_vehicle_feature(
        session: AsyncSession, vehicle_id: Optional[int], feature_id: Optional[int]
) -> VehicleFeatures:
    return VehicleFeatures(vehicle_id=vehicle_id, feature_id=feature_id)


@with_save
async def bind_vehicle_function(
        session: AsyncSession, function_id: Optional[int], vehicle_feature_id: Optional[int]
) -> VehicleFunctions:
    return VehicleFunctions(function_id=function_id, vehicle_feature_id=vehicle_feature_id)


@with_save
async def bind_vehicle_component(
        session: AsyncSession, vehicle_id: Optional[int], component_id: Optional[int]
) -> VehicleComponents:
    amount = random.randrange(1, 10)
    return VehicleComponents(vehicle_id=vehicle_id, component_id=component_id, component_amount=amount)


@with_save
async def bind_vehicle_function_component(
        session: AsyncSession,
        vehicle_function_id: Optional[int],
        vehicle_component_id: Optional[int]
) -> VehicleFunctionComponents:
    return VehicleFunctionComponents(
        vehicle_function_id=vehicle_function_id,
        vehicle_component_id=vehicle_component_id
    )


async def build_vehicle(session: AsyncSession) -> Vehicle:
    component = await create_component(session)
    group = await create_group(session)
    feature = await create_feature(session, group.id)
    function = await create_function(session, feature.id)
    await bind_function_component(session, function.id, component.id)

    vehicle = await create_vehicle(session)
    vehicle_feature = await bind_vehicle_feature(session, vehicle.id, feature.id)
    vehicle_function = await bind_vehicle_function(session, function.id, vehicle_feature.id)
    vehicle_component = await bind_vehicle_component(session, vehicle.id, component.id)
    await bind_vehicle_function_component(
        session, vehicle_function.id, vehicle_component.id
    )

    return vehicle
