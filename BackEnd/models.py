from sqlalchemy import Column, Integer, String
from database import Base


class Device(Base):
	
	__tablename__ = "devices"
	

	id = Column(Integer, primary_key=True, index=True)
	

	ip = Column(String)
	mac = Column(String)



