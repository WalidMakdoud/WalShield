# Cree une connection vers la base de donnee
from sqlalchemy import create_engine
# Cree une base de class pour la base de donne modele
from sqlalchemy.ext.declarative import declarative_base
# Cree une base de donnee session
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "sqlite:///./walidshield.db"


engine = create_engine(

	DATABASE_URL,
	connect_args={"check_same_thread": False}

)

SessionLocal = sessionmaker(

	autocommit=False,
	autoflush=False,
	bind=engine
)

Base = declarative_base()

