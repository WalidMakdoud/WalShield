from pydantic import BaseModel


class DeviceCreate(BaseModel):

	ip: str
	mac: str
