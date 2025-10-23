from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import httpx
import os


class CoolNetFrontend:
    def __init__(self, backend_url: str = "http://127.0.0.1:8000"):
        self.backend_url = backend_url
        self.app = FastAPI(title="CoolNet IoT Frontend")

        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))

        # Static files (CSS, JS, images)
        self.app.mount("/static", StaticFiles(directory=os.path.join(base_dir, "static")), name="static")

        # Simple routes
        self.app.get("/", response_class=HTMLResponse)(self.index)
        self.app.get("/view", response_class=HTMLResponse)(self.view_data)
        self.app.get("/add", response_class=HTMLResponse)(self.add_form)
        self.app.post("/add", response_class=HTMLResponse)(self.add_sensor)

    # Tilføj disse metoder for at gøre monkeypatching nemmere
    async def get_sensors_data(self):
        """Get all sensors data - for monkeypatching"""
        async with httpx.AsyncClient() as client:
            return await client.get(f"{self.backend_url}/sensors/data")

    async def get_sensor_by_id(self, sensor_id: str):
        """Get specific sensor - for monkeypatching"""
        async with httpx.AsyncClient() as client:
            return await client.get(f"{self.backend_url}/sensors/data/{sensor_id}")

    async def post_sensor_data(self, data: dict):
        """Post sensor data - for monkeypatching"""
        async with httpx.AsyncClient() as client:
            return await client.post(f"{self.backend_url}/sensors/data", data=data)

    async def index(self, request: Request):
        """Forside med oversigt"""
        try:
            response = await self.get_sensors_data()  # Brug den nye metode
            
            if response.status_code == 200:
                sensors = response.json()["body"]
                return self.templates.TemplateResponse("index.html", {"request": request, "sensors": sensors})
            else:
                return self.show_error(request, "Kunne ikke hente data", 500)
        except:
            return self.show_error(request, "Backend ikke tilgængelig", 503)

    async def view_data(self, request: Request):
        """Vis sensor data"""
        sensor_id = request.query_params.get("sensor_id", "")
        
        if sensor_id:
            try:
                response = await self.get_sensor_by_id(sensor_id)  # Brug den nye metode
                
                if response.status_code == 200:
                    sensor = response.json()["body"]
                    return self.templates.TemplateResponse("view.html", {"request": request, "sensor": sensor})
                else:
                    return self.show_error(request, f"Sensor '{sensor_id}' ikke fundet", 404)
            except:
                return self.show_error(request, "Backend fejl", 503)
        else:
            return self.show_error(request, "Angiv sensor ID", 400)

    async def add_form(self, request: Request):
        """Formular til at tilføje data"""
        return self.templates.TemplateResponse("add.html", {"request": request})

    async def add_sensor(self, request: Request,
                        sensor_id: str = Form(...),
                        temperature: float = Form(...),
                        humidity: float = Form(...),
                        power_consumption: float = Form(...),
                        location: str = Form(...)):
        """Tilføj sensor data"""
        try:
            response = await self.post_sensor_data({  # Brug den nye metode
                "sensor_id": sensor_id,
                "temperature": temperature,
                "humidity": humidity,
                "power_consumption": power_consumption,
                "location": location
            })
            
            if response.status_code == 200:
                return RedirectResponse(url="/", status_code=303)
            else:
                return self.show_error(request, "Kunne ikke tilføje data", 400)
        except:
            return self.show_error(request, "Backend fejl", 503)

    def show_error(self, request, error_message, status_code):
        # Korrekt: request som første parameter, template navn som anden
        return self.templates.TemplateResponse(
            request,  # request kommer først!
            "error.html", 
            {"error_message": error_message},
            status_code=status_code
        )