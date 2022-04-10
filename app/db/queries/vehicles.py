from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models import (
    Vehicle,
    VehicleComponents,
    VehicleFeatures,
    VehicleFunctions
)
from db.queries.exceptions import NotFound


async def get_vehicle(session: AsyncSession, vehicle_id: int) -> Vehicle:
    try:
        statement = select(Vehicle).where(Vehicle.id == vehicle_id).options(
                joinedload(
                    Vehicle.vehicle_features
                ).joinedload(
                    VehicleFeatures.feature
                ),
                joinedload(
                    Vehicle.vehicle_features
                ).
                joinedload(
                    VehicleFeatures.vehicle_functions
                ).joinedload(
                    VehicleFunctions.function
                ),
                joinedload(
                    Vehicle.vehicle_features
                ).
                joinedload(
                    VehicleFeatures.vehicle_functions
                ).
                joinedload(VehicleFunctions.vehicle_components).joinedload(VehicleComponents.component)
        )
        request = await session.execute(statement)
        result = request.scalar_one()
        return result

    except NoResultFound as e:
        raise NotFound(e)
