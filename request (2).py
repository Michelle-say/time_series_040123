from class_sql import sncf
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

def get_object_with_date(session, first, last):
    return(session.query(sncf).filter(
            sncf.FULL_DATE>=first, sncf.FULL_DATE<last).all())

def moyenne_par_mois(session):
    return(session.query(sncf.__getattribute__).all())

if __name__=="__main__":
    engine = create_engine("sqlite:///./data/sncf.db")
    Session = sessionmaker(bind=engine)
    with Session() as session:
        print(moyenne_par_mois(session))