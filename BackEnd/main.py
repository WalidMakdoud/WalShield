from fastapi import FastAPI
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import ArpScan, PortScan, DeauthScan, DosScan
from schemas import ArpScanCreate, PortScanCreate, DeauthScanCreate, DosScanCreate
from fastapi.middleware.cors import CORSMiddleware

# Cree la table de la base de donnee
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/arp")
def create_arp(device: ArpScanCreate):

	db: Session = SessionLocal()

	#Ckeck if device in database
	existing_device = db.query(ArpScan).filter(
		
		ArpScan.ip == device.ip,
		ArpScan.mac == device.mac

	).first()

	if existing_device:


		return {

			"message" : "device already existes"
		}


	new_device = ArpScan(
		
		ip=device.ip,
		mac=device.mac
	)

	db.add(new_device)


	db.commit()
	return {

		"message" : "device saved"
	}


@app.post("/portscan")
def create_portscan(device: PortScanCreate):

        db: Session = SessionLocal()

        #Ckeck if device in database
        existing_device = db.query(PortScan).filter(

                PortScan.ip == device.ip,
                PortScan.ports_scanned == ports_scanned

        ).first()

        if existing_device:


                return {

                        "message" : "device already existes"
                }


        new_device = PortScan(

                ip=device.ip,
                ports_scanned=device.ports_scanned
        )

        db.add(new_device)


        db.commit()
        return {

                "message" : "device saved"
        }

@app.post("/deauth")
def create_deauthscan(device: DeauthScanCreate):

        db: Session = SessionLocal()

        #Ckeck if device in database
        existing_device = db.query(DeauthScan).filter(

                DeauthScan.mac == device.mac,

        ).first()

        if existing_device:


                return {

                        "message" : "device already existes"
                }


        new_device = DeauthScan(

                mac=device.mac,
        )

        db.add(new_device)


        db.commit()
        return {

                "message" : "device saved"
        }




@app.post("/dos")
def create_deauthscan(device: DosScanCreate):

        db: Session = SessionLocal()

        #Ckeck if device in database
        existing_device = db.query(DosScan).filter(

                DosScan.ip == device.ip,

        ).first()

        if existing_device:


                return {

                        "message" : "device already existes"
                }


        new_device = DosScan(

                ip=device.ip,
        )

        db.add(new_device)


        db.commit()
        return {

                "message" : "device saved"
        }





@app.get("/arp")
def get_arp():

	db : Session = SessionLocal()

	devices = db.query(ArpScan).all()

	return devices


@app.get("/portscan")
def get_portscan():

        db : Session = SessionLocal()

        devices = db.query(PortScan).all()

        return devices



@app.get("/deauth")
def get_deauthscan():

        db : Session = SessionLocal()

        devices = db.query(DeauthScan).all()

        return devices


@app.get("/dos")
def get_deauthscan():

        db : Session = SessionLocal()

        devices = db.query(DosScan).all()

        return devices
