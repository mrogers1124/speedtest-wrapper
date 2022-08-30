# SQLAlchemy Data Model
from sqlalchemy import Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.types import Boolean, DateTime, Integer, Float, Text


Base = declarative_base()


# Interface class
class Interface(Base):
    __tablename__ = 'interface'

    interface_uid = Column(Integer, primary_key=True)
    internalIp = Column(Text)
    name = Column(Text)
    macAddr = Column(Text)
    isVpn = Column(Boolean)
    externalIp = Column(Text)

    results = relationship('Result', back_populates='interface')

    def __repr__(self):
        return f'<Interface {self.interface_uid}>'


# Server class
class Server(Base):
    __tablename__ = 'server'

    server_uid = Column(Integer, primary_key=True)
    id = Column(Integer)
    host = Column(Text)
    port = Column(Integer)
    name = Column(Text)
    location = Column(Text)
    country = Column(Text)
    ip = Column(Text)

    results = relationship('Result', back_populates='interface')

    def __repr__(self):
        return f'<Server {self.server_uid}>'


# Result class
class Result(Base):
    __tablename__ = 'result'

    result_uid = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)

    # Ping results
    ping_jitter = Column(Float)
    ping_latency = Column(Float)
    ping_low = Column(Float)
    ping_high = Column(Float)

    # Download results
    download_bandwidth = Column(Integer)
    download_bytes = Column(Integer)
    download_elapsed = Column(Integer)
    download_latency_iqm = Column(Float)
    download_latency_low = Column(Float)
    download_latency_high = Column(Float)
    download_latency_jitter = Column(Float)

    # Upload results
    upload_bandwidth = Column(Integer)
    upload_bytes = Column(Integer)
    upload_elapsed = Column(Integer)
    upload_latency_iqm = Column(Float)
    upload_latency_low = Column(Float)
    upload_latency_high = Column(Float)
    upload_latency_jitter = Column(Float)

    packetLoss = Column(Integer)
    isp = Column(Text)

    # Interface and Server links
    interface_uid = Column(Integer, ForeignKey('interface.interface_uid'))
    server_uid = Column(Integer, ForeignKey('server.server_uid'))
    interface = relationship('Interface', back_populates='results')
    server = relationship('Server', back_populates='results')

    result_id = Column(Text)
    result_url = Column(Text)
    result_persisted = Column(Boolean)

    def __repr__(self):
        return f'<Result {self.result_uid}>'
