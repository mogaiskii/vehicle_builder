__all__ = ('VehicleView',)

from aiohttp import web
from aiohttp.web_exceptions import HTTPNotFound
from aiohttp_pydantic.oas.typing import r200  # type: ignore

from api.application import RequestHandler
from api.models.vehicle import VehicleResponseModel
from db.queries.exceptions import NotFound
from service.vehicle import VehicleService


class VehicleView(RequestHandler):
    async def get(self, vehicle_id: int, /) -> r200[VehicleResponseModel]:
        async with self.get_session() as session:
            try:
                vehicle = await VehicleService.get_vehicle(session, vehicle_id)
            except NotFound:
                raise HTTPNotFound
            vehicle_response = VehicleResponseModel.from_orm(vehicle)
            return web.json_response(vehicle_response.dict())
