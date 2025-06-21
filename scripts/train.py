import os
import urllib.request
import pandas as pd
import numpy as np
import joblib
from sklearn.linear_model import LinearRegression
import mlflow
import mlflow.sklearn

DATAPATH = "data"
DOWNLOAD_ROOT = "https://raw.githubusercontent.com/ageron/handson-ml2/master/"

def download_data(datapath):
    os.makedirs(datapath, exist_ok=True)
    for file in ["oecd_bli_2015.csv", "gdp_per_capita.csv"]:
        url = f"{DOWNLOAD_ROOT}datasets/lifesat/{file}"
        urllib.request.urlretrieve(url, os.path.join(datapath, file))

def load_data():
    oecd = pd.read_csv(os.path.join(DATAPATH, "oecd_bli_2015.csv"), thousands=',')
    gdp = pd.read_csv(os.path.join(DATAPATH, "gdp_per_capita.csv"), thousands=',', delimiter='\t', encoding='latin1', na_values="n/a")
    return oecd, gdp

def prepare_data(oecd_bli, gdp_per_capita):
    df1 = oecd_bli[oecd_bli["INEQUALITY"] == "TOT"]
    df1 = df1.pivot(index="Country", columns="Indicator", values="Value")
    df2 = gdp_per_capita.rename(columns={"2015": "GDP per capita"})
    df2.set_index("Country", inplace=True)
    df = pd.merge(df1, df2, left_index=True, right_index=True)
    df = df[["GDP per capita", "Life satisfaction"]].dropna()
    return df

def train_model(X, y):
    model = LinearRegression()
    model.fit(X, y)
    return model

if __name__ == "__main__":
    download_data(DATAPATH)
    oecd, gdp = load_data()
    data = prepare_data(oecd, gdp)
    X = np.c_[data["GDP per capita"]]
    y = np.c_[data["Life satisfaction"]]

    with mlflow.start_run():
        mlflow.log_param("modelo", "LinearRegression")
        mlflow.log_param("features", "GDP per capita")

        model = train_model(X, y)
        score = model.score(X, y)
        mlflow.log_metric("R2_train", score)

        os.makedirs("models", exist_ok=True)
        model_path = "models/life_satisfaction_model.pkl"
        joblib.dump(model, model_path)
        mlflow.log_artifact(model_path, artifact_path="model")

        print(f"✅ Modelo treinado com R²={score:.3f} e logado no MLflow")
