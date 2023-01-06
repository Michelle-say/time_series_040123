from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
import pandas as pd
import requests
import json
import datetime

#Initialisation de la base de donnée
engine = create_engine("sqlite:///../sncf.db")
Base = declarative_base()

class Objects(Base):
    __tablename__ = 'Objects'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date)
    restitution_date = Column(Date)
    gare = Column(String)
    nature = Column(String)
    type = Column(String)
    nom = Column(String)

    
Base.metadata.create_all(engine)
API_URL = 'https://ressources.data.sncf.com/api/records/1.0/search/?dataset=objets-trouves-restitution&q=&rows=10000&sort=date&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&refine.gc_obo_gare_origine_r_name=Lille+Europe&refine.date='
df = pd.DataFrame()
first = True
for date in ["2016", "2017","2018","2019", "2020", "2021", "2022"]:
    try:
            req = requests.get(API_URL + date).text
            req_json = json.loads(req)
            tab = []
            for element in req_json["records"]:
                tab.append(element["fields"])
            if first:
                first = False
                df = pd.DataFrame(tab)
            else:
                df1 = pd.DataFrame(tab)
                df = pd.concat([df, df1])
    except:
        pass
df.rename(columns={'gc_obo_gare_origine_r_code_uic_c': "code",
                        "gc_obo_date_heure_restitution_c": "restitution_date",
                        'gc_obo_gare_origine_r_name':"gare",
                        'gc_obo_nature_c':"nature",
                        'gc_obo_type_c':"type",
                        'gc_obo_nom_recordtype_sc_c':"nom"}, inplace=True)
del df["code"]
df.to_csv('csv/sncf.csv', index=False)