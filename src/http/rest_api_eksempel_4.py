from fastapi import FastAPI, Form, HTTPException
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
import os, json

app = FastAPI()

DB_FILE = "db_flat_file.json"

# "Database" i hukommelsen
db: dict[str, dict] = {}

class Person(BaseModel):
  person_id: str
  navn: str
  alder: int


def load_db():
    global db
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                db = json.load(f)
        except json.JSONDecodeError:
            db = {}
    else:
        db = {}


def save_db():
    with open(DB_FILE, "w", encoding="utf-8") as fileObject:
        json.dump(db, fileObject, indent=2, ensure_ascii=False)


# Startup
@app.on_event("startup")
def startup_event():
    """Køres når API’et starter."""
    load_db()


# POST: Gem en person i "db"
@app.post("/person")
def create_person(person_id: str = Form(...), navn: str = Form(...), alder: int = Form(...)):
  db[person_id] = {"person_id": person_id, "navn": navn, "alder": alder}
  save_db()
  return {
    "header": {
      "status": "gemt",
      "code": 200,
      }, 
    "body": db[person_id]
    }


# GET: Hent en person fra "db" uden id
@app.get("/person")
def read_person():
  raise HTTPException(status_code=400, detail="path skal være /person/<person_id>")

# GET: Hent en person fra "db"
@app.get("/person/{person_id}")
def read_person(person_id: str):
  if person_id not in db:
    raise HTTPException(status_code=404, detail=f"Person med id '{person_id}' findes ikke")
  output = {
    "header": {
      "status": "ok",
      "code": 200,
      }, 
    "body": db[person_id]
    }
      
  return output




# Kør i terminal/console med: 
# uvicorn src.http.rest_api_eksempel_3:app --reload
#
# Kør i browser:
# Website: http://127.0.0.1:8000/ 
# Test: http://127.0.0.1:8000/new for at oprette en ny person med person_id '1337'
# Test: http://127.0.0.1:8000/person/1337 skal vise personen
# Test: http://127.0.0.1:8000/person/1338 skal vise en 404
# Test: http://127.0.0.1:8000/person/ skal vise en 400 at man skal bruge 'person_id'

# Documentation: http://127.0.0.1:8000/docs