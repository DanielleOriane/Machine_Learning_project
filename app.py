from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
import numpy as np
import joblib
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

data = pd.read_csv('cleaned_table.csv')
model = joblib.load('saved_model/gbr_model.pkl')

@app.get("/", response_class= HTMLResponse)
async def index(request: Request):
    
    sex=sorted(data['sex'].unique())
    smoker=sorted(data['smoker'].unique())
    region=sorted(data['region'].unique())

    return templates.TemplateResponse("index.html", {"request": request, "sex": sex, "smoker": smoker, "region": region })


@app.post("/predict", response_class= HTMLResponse)
async def predict(request: Request):

    resp = await request.form()
   
    print (resp)

    prediction=model.predict(pd.DataFrame(columns=['age', 'sex', 'bmi', 'children', 'smoker', 'region'],
                            data=np.array([resp.get('age'),resp.get('sex'),resp.get('bmi'),resp.get('children'),resp.get('smoker'), resp.get('region') ]).reshape(1, 6)))
    
   
    return str(round(prediction[0],2))
