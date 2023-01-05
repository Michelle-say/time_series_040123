from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
import pandas as pd
import requests
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
dataframe_objects = pd.DataFrame()
for i in ["2016", "2017","2018","2019", "2020", "2021", "2022"]:
    data_objects = requests.get(f'https://ressources.data.sncf.com/api/records/1.0/search/?dataset=objets-trouves-restitution&q=&rows=10000&sort=date&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&refine.gc_obo_gare_origine_r_name=Lille+Europe&refine.date={i}').json()
    df_objects = pd.DataFrame(data_objects['records'])
    try:
        df_objects = pd.DataFrame(list(df_objects['fields']))
    except:
        pass
        
dataframe_objects.rename(columns={'gc_obo_gare_origine_r_code_uic_c': "code",
                        "gc_obo_date_heure_restitution_c": "restitution_date",
                        'gc_obo_gare_origine_r_name':"gare",
                        'gc_obo_nature_c':"nature",
                        'gc_obo_type_c':"type",
                        'gc_obo_nom_recordtype_sc_c':"nom"}, inplace=True)

dataframe_objects.to_csv('csv/sncf.csv', index=False)