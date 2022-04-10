from pydantic import BaseModel


class VehicleResponseModel(BaseModel):
    class Config:
        orm_mode = True
