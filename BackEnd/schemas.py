from pydantic import BaseModel


class ArpScanCreate(BaseModel):

	ip: str
	mac: str

class PortScanCreate(BaseModel):

	ip : str
	ports : str

class DeauthScanCreate(BaseModel):

	ip : str

