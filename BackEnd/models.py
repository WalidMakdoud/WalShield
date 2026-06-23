from sqlalchemy import Column, Integer, String
from database import Base


class ArpScan(Base):
	
	__tablename__ = "arp_scans"
	

	id = Column(Integer, primary_key=True, index=True)
	

	ip = Column(String)
	mac = Column(String)


class PortScan(Base):
	
	__tablename__ = "port_scans"

	id = Column(Integer, primary_key=True, index=True)

	ip = Column(String)
	ports_scanned = Column(String)

class DeauthScan(Base):

	__tablename__ = "deauth_scans"

	id = Column(Integer, primary_key=True, index=True)

	ip = Column(String)


