from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bgp_models import Base, Router, Interface, BGP, Neighbor, Network
import json
from pathlib import Path


json_path =Path(__file__).resolve().parent / "bgp_plan.json"
with json_path.open("r", encoding = "utf-8") as f:
    data = json.load(f)


with session_factory() as session:

        for device in data:
            router = session.query(Router).filter_by(
                name = device["name"]
            ).first()

            if router is None:
                router = Router(
                    name = device["name"],
                    host = device["host"]
                )         
                session.add(router)
            else:
                print(f"{device["name"]}已存在,跳过")
            

            if not router.interfaces:
                for inter in device["interfaces"]:
                    interface = Interface(
                        name = inter["name"], 
                        address = inter["address"], 
                        mask = inter["mask"], 
                        description =inter["description"]
                    )
                    router.interfaces.append(interface)  # 将新加入的int关联到router
            if not router.bgp:
                bgp = BGP(
                    local_as = device["local_as"],
                    router_id_value = device["router_id"]
                )
                router.bgp = bgp
            if not router.bgp.neighbors:
                for nei in device["neighbors"]:
                    
                    neighbor = Neighbor(
                        peer_ip = nei["peer_ip"],
                        remote_as = nei["remote_as"]
                    )
                    router.bgp.neighbors.append(neighbor)
            if not router.bgp.networks:
                for net in device["networks"]:
                    network = Network(
                        prefix = net["prefix"],
                        mask = net["mask"]
                    )
                    router.bgp.networks.append(network)
         
        session.commit()
        print(f"Router={session.query(Router).count()}")
        print(f"Interface={session.query(Interface).count()}")
        print(f"BGP={session.query(BGP).count()}")
        print(f"Neighbor={session.query(Neighbor).count()}")
        print(f"Network={session.query(Network).count()}")


