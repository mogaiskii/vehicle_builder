from aiohttp.web import Request, Response

__all__ = ('get_vehicle',)


async def get_vehicle(request: Request) -> Response:
    return Response()
