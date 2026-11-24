from sqlalchemy import Integer, String, ForeignKey, Column, create_engine
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship, sessionmaker

Base = declarative_base()
database_url = "postgresql+psycopg://aiops:aiops123@127.0.0.1:15435/aiops"
engine = create_engine(database_url)
Base.metadata.create_all(engine)
Session = sessionmaker(bind = engine)

def session_factory():
    return Session()


class Router(Base):
    __tablename__ = "aiops_router"
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String, unique=True)
    host : Mapped[str] = mapped_column(String)
    interfaces = relationship("Interface", back_populates="router") # 一对多 router.interface 返回所有int对象的列表
    bgp = relationship("BGP", back_populates="router", uselist=False)# 一对一 不返回列表

class Interface(Base):
    __tablename__ = "aiops_interface"
    id = Column(Integer, primary_key = True, autoincrement = True)
    router_id = Column(Integer, ForeignKey("aiops_router.id"))
    name = Column(String)
    address = Column(String)
    mask = Column(String)
    description = Column(String)
    router = relationship("Router", back_populates="interfaces")

class BGP(Base):
    __tablename__ = "aiops_bgp"
    id = Column(Integer, primary_key = True, autoincrement = True)
    router_id = Column(Integer, ForeignKey("aiops_router.id"), unique = True)
    local_as = Column(Integer)
    router_id_value = Column(String)
    router = relationship("Router", back_populates="bgp")
    neighbors = relationship("Neighbor", back_populates="bgp")
    networks = relationship("Network", back_populates="bgp")


class Neighbor(Base):
    __tablename__ = "aiops_neighbor"
    id = Column(Integer, primary_key = True, autoincrement = True)
    bgp_id = Column(Integer, ForeignKey("aiops_bgp.id"))
    peer_ip = Column(String)
    remote_as = Column(Integer)
    bgp = relationship("BGP", back_populates="neighbors")

class Network(Base):
    __tablename__="aiops_network"
    id = Column(Integer, primary_key = True, autoincrement = True)
    bgp_id = Column(Integer, ForeignKey("aiops_bgp.id"))
    prefix = Column(String)
    mask = Column(String)
    bgp = relationship("BGP", back_populates = "networks")