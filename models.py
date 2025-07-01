from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Связующая таблица для связи клиентов и сегментов
client_segment_association = Table(
    'client_segment', Base.metadata,
    Column('client_id', Integer, ForeignKey('clients.id')),
    Column('segment_id', Integer, ForeignKey('segments.id'))
)

class Tag(BaseModel):
    id: int
    name: str
    color: str
    text: str
    emoji: str

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    segments = relationship("Segment", secondary=client_segment_association, back_populates="clients")

class Segment(Base):
    __tablename__ = 'segments'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    tags = relationship("Tag", back_populates="segment")
    clients = relationship("Client", secondary=client_segment_association, back_populates="segments")

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    color = Column(String)
    text = Column(String)
    emoji = Column(String)
    segment_id = Column(Integer, ForeignKey('segments.id'))
    segment = relationship("Segment", back_populates="tags")

class AddTagsRequest(BaseModel):
    tag_ids: List[int]