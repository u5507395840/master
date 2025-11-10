import os
import uuid
import enum
from datetime import datetime
from sqlalchemy import create_engine, Column, String, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import func

# --- Definiciones del Modelo ---

DATABASE_URL = "sqlite:///data/stakazo.db"
Base = declarative_base()

class CampaignStatus(enum.Enum):
    PENDING = "PENDING"
    QUEUED = "QUEUED"
    GENERATING_CAPTIONS = "GENERATING_CAPTIONS"
    GENERATING_VIDEO = "GENERATING_VIDEO"
    DISTRIBUTING = "DISTRIBUTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Campaign(Base):
    __tablename__ = "campaigns"
    id = Column(String, primary_key=True, default=lambda: f"CAMP_{uuid.uuid4().hex[:10].upper()}")
    artist = Column(String, nullable=False)
    track = Column(String, nullable=False)
    video_prompt = Column(String)
    status = Column(SQLAlchemyEnum(CampaignStatus), default=CampaignStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# --- Conexión y Sesión de Base de Datos ---

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    os.makedirs("data", exist_ok=True)
    Base.metadata.create_all(bind=engine)
    print(f"✅ Database initialized: {DATABASE_URL.split('///')[1]}")

# --- Funciones de Acceso a Datos (CRUD) ---

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_all_campaigns():
    db = SessionLocal()
    campaigns = db.query(Campaign).all()
    db.close()
    return campaigns

def get_campaign_by_id(campaign_id: str):
    db = SessionLocal()
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    db.close()
    return campaign

def save_campaign(artist: str, track: str, video_prompt: str = ""):
    db = SessionLocal()
    new_campaign = Campaign(artist=artist, track=track, video_prompt=video_prompt)
    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign)
    db.close()
    return new_campaign

def update_campaign_status(campaign_id: str, status: CampaignStatus):
    db = SessionLocal()
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if campaign:
        campaign.status = status
        db.commit()
        db.close()
        return True
    db.close()
    return False

# Inicializar la base de datos al importar el módulo
init_db()
