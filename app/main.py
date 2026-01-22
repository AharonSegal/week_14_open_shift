from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import numpy as np
import io

from app.db import init_db, insert_weapons

app = FastAPI(title="Weapon Warehouse Intelligence System")


@app.on_event("startup")
def on_startup():
    # initialize db on startup
    init_db()


@app.post("/upload")
def upload_file(file: UploadFile = File(...)):

    df = pd.read_csv(file.file)

    # categorize range_km to level_risk
    bins = [-np.inf, 20, 100, 300, np.inf]
    labels = ["low", "medium", "high", "extreme"]

    df["level_risk"] = pd.cut(
        df["range_km"],
        bins=bins,
        labels=labels,
    )
    # fill NULL with "Unknown"
    df["manufacturer"] = df["manufacturer"].replace("", pd.NA)
    df["manufacturer"] = df["manufacturer"].fillna("Unknown")

    df_dict_list = df.to_dict(orient="records")

    # df_dict_list to db
    inserted_count = insert_weapons(df_dict_list)

    return JSONResponse(
        content={"status": "success", "inserted_records": inserted_count}
    )
