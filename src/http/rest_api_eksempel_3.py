from fastapi import FastAPI, Form, HTTPException
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

app = FastAPI()

# "Database" i hukommelsen
db: dict[str, dict] = {}

class Person(BaseModel):
  person_id: str
  navn: str
  alder: int

# POST: Gem en person i "db"
@app.post("/person")
def create_person(person_id: str = Form(...), navn: str = Form(...), alder: int = Form(...)):
  db[person_id] = {"person_id": person_id, "navn": navn, "alder": alder}
  return {"status": "gemt", "data": db[person_id]}


# GET: Hent en person fra "db"
@app.get("/person")
def read_person():
  raise HTTPException(status_code=400, detail="path skal være /person/<person_id>")

# GET: Hent en person fra "db"
@app.get("/person/{person_id}")
def read_person(person_id: str):
  if person_id not in db:
      return {"status": "fejl", "besked": f"Person med id '{person_id}' findes ikke"}
  return {"status": "ok", "data": db[person_id]}

@app.get("/new", response_class=HTMLResponse)
def new_person_form():
  return f"""
  <!DOCTYPE html>
  <html lang="da">
  <head>
    <meta charset="UTF-8">
    <title>Opret Person</title>
  </head>
  <body>
    <h2>Opret en person</h2>
    <p><i>⚠ (normalt skal dette være på en frontend og ikke som her på en backend)</i></p>
    <form action="/person" method="post">
      <label for="person_id">ID:</label><br>
      <input type="text" id="person_id" name="person_id" required><br><br>
      
      <label for="navn">Navn:</label><br>
      <input type="text" id="navn" name="navn" required><br><br>
      
      <label for="alder">Alder:</label><br>
      <input type="number" id="alder" name="alder" required><br><br>
      
      <button type="submit">Gem</button>
    </form>
  </body>
  </html>
  """


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