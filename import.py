import requests
import logging
import json
import pandas as pd
from datetime import datetime

API_URL="https://ressources.data.sncf.com/api/records/1.0/search/?dataset=objets-trouves-restitution&q=&rows=10000&sort=date&facet=date&facet=gc_obo_type_c&refine.gc_obo_gare_origine_r_name=Lille+Europe&refine.date="
DOWNLOAD_YEAR=["2017","2018","2019","2020","2021","2022","2023"]

if __name__=="__main__":
    logging.basicConfig(filename="log/log_debug.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    df = pd.DataFrame()
    first = True
    for date in DOWNLOAD_YEAR:
        logger.info("Download url :" + API_URL +date)
        try:
            req = requests.get(API_URL + date).text
            req_json = json.loads(req)
            tab = []
            for element in req_json["records"]:
                tab.append(element["fields"])
            if first:
                first = False
                df = pd.DataFrame(tab)
                logging.info(len(df))
            else:
                df1 = pd.DataFrame(tab)
                logging.info(len(df1))
                df = pd.concat([df, df1])
                logging.info(df)
        except Exception as e:
            logger.error("ERROR : " + str(e))
    df = df[["gc_obo_nature_c", "date"]].rename(columns = {'gc_obo_nature_c':'OBJECT', 'date':"DATE"})
    df["FULL_DATE"]=df["DATE"].apply(lambda date: datetime.strptime(date,"%Y-%m-%dT%H:%M:%S%z").strftime("%Y-%m-%d %H:%M:%S"))
    df["YEAR"]=df["DATE"].apply(lambda date: datetime.strptime(date,"%Y-%m-%dT%H:%M:%S%z").strftime("%Y"))
    df["MONTH"]=df["DATE"].apply(lambda date: datetime.strptime(date,"%Y-%m-%dT%H:%M:%S%z").strftime("%m"))
    df["DATE"]=df["FULL_DATE"].apply(lambda date: date.split(" ")[0])
    df["TIME"]=df["FULL_DATE"].apply(lambda date: date.split(" ")[1])
    df.to_csv("data/sncf.csv", index=False)
