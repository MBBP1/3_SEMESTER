from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Person(BaseModel):
    navn: str
    alder: int

@app.get("/person")
def echo(navn: str, alder: int):
    return {"modtaget_data": {"navn": navn, "alder": alder}, "status": {"code": 200, "message": "ok"}}

# Kør i terminal/console med: 
# uvicorn src.http.rest_api_eksempel_1:app --reload
#
# Kør i browser:
# Website: http://127.0.0.1:8000/ 
# Test: http://127.0.0.1:8000/person?navn=Jens&alder=22
#
# Forventet resultat i JSON:
# {
#   "modtaget_data": {
#     "navn": "Jens",
#     "alder": 22
#   },
#   "status": {
#     "code": 200,
#     "message": "ok"
#   }
# }

# Documentation: http://127.0.0.1:8000/docs
