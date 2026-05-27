from fastapi import FastAPI
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Device
from schemas import DeviceCreate

# Cree la table de la base de donnee
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/devices")
def create_device(device: DeviceCreate):

	db: Session = SessionLocal()

	#Ckeck if device in database
	existing_device = db.query(Device).filter(
		
		Device.ip == device.ip,
		Device.mac == device.mac

	).first()

	if existing_device:


		return {

			"message" : "device already existes"
		}


	new_device = Device(
		
		ip=device.ip,
		mac=device.mac
	)

	db.add(new_device)


	db.commit()
	return {

		"message" : "device saved"
	}


@app.get("/devices")
def get_devices():

	db : Session = SessionLocal()

	devices = db.query(Device).all()

	return devices
