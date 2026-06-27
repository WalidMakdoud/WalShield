from pydantic import BaseModel


class ArpScanCreate(BaseModel):

	ip: str
	mac: str

class PortScanCreate(BaseModel):

	ip : str
	ports_scanned : str

class DeauthScanCreate(BaseModel):

	mac : str

class DosScanCreate(BaseModel):

        ip : str
