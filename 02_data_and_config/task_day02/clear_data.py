from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bgp_models import Router, Interface, BGP, Neighbor, Network

database_url = "postgresql+psycopg://aiops:aiops123@127.0.0.1:15435/aiops"
engine = create_engine(database_url)
Session = sessionmaker(bind=engine)

with Session() as session:
    session.query(Neighbor).delete()
    session.query(Network).delete()
    session.query(BGP).delete()
    session.query(Interface).delete()
    session.query(Router).delete()

    session.commit()
    print("All data deleted successfully")