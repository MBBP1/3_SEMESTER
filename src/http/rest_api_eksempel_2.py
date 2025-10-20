from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

app = FastAPI()

class Person(BaseModel):
    navn: str
    alder: int

@app.get("/person", response_class=HTMLResponse)
def echo(navn: str, alder: int):
    return f"""
<!DOCTYPE html>
<html lang="da">
<head>
  <meta charset="UTF-8">
  <title>Som HTML</title>
</head>
<body>
  <h2>Modtaget Data</h2>
  <ul>
    <li><strong>Navn:</strong> {navn}</li>
    <li><strong>Alder:</strong> {alder}</li>
  </ul>

  <h2>Status</h2>
  <ul>
    <li><strong>Code:</strong> 200</li>
    <li><strong>Message:</strong> ok</li>
  </ul>
</body>
</html>
    """
# Kør i terminal/console med: 
# uvicorn src.http.rest_api_eksempel_2:app --reload
#
# Kør i browser:
# Website: http://127.0.0.1:8000/ 
# Test: http://127.0.0.1:8000/person?navn=Jens&alder=22
#
# Forventet resultat i HTML:
# Modtaget Data
# * Navn: Jens
# * Alder: 22
# Status
# * Code: 200
# * Message: ok

# Documentation: http://127.0.0.1:8000/docs
