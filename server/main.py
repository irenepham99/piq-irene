from typing import Union, Dict, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from simulator import run_simulation
from pydantic import BaseModel
from datetime import datetime

class Datapoint(BaseModel):
    scenario: int
    datetime: datetime
    power_MW: float

class Study(BaseModel):
    num_scenarios: int
    scenario_type: str
    start_time: datetime
    end_time: datetime

class SavedStudy(Study): 
    id: int
    results: List[Datapoint]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

studies_db: Dict[int, SavedStudy] = {}
current_id: int = 1

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/studies")
def run_study(study : Study):
    global current_id

    simulation_results = run_simulation(
        num_scenarios=study.num_scenarios,
        scenario_type=study.scenario_type,
        start=study.start_time,
        end=study.end_time
    )

    #save the study and its results to the DB
    saved_study = SavedStudy(
    **study.model_dump(),
    id=current_id,  
    results=simulation_results)

    studies_db[current_id] = saved_study 

    response = {"id" : current_id}
    current_id += 1

    return response


@app.get("/studies/{study_id}")
def get_study(study_id: int):
    study = studies_db.get(study_id)
    if not study:
        raise HTTPException(status_code=404, detail="Study not found")
    return {"id": study_id, "results": study.results, "start_time": study.start_time, "end_time": study.end_time, "scenario_type": study.scenario_type}

