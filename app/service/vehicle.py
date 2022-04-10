from db.models import Vehicle
from db.queries.vehicles import get_vehicle
from sqlalchemy.ext.asyncio import AsyncSession


class VehicleService:
    @classmethod
    async def get_vehicle(cls, session: AsyncSession, vehicle_id: int) -> Vehicle:
        return await get_vehicle(session, vehicle_id)
