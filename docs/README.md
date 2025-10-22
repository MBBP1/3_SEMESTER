Detailed documentation
- pip install pytest amqtt asyncio paho-mqtt pytest-timeout fastapi uvicorn python-multipart httpx






## Test Strategier

### Test Pyramiden
Vi følger test pyramiden for at sikre en robust teststrategi:

- **Unit Tests (Bundlag)**: Test af individuelle komponenter (UDP, TCP, MQTT klienter/servere)
- **Integration Tests (Middellag)**: Test af kommunikation mellem komponenter (sensor → controller → aktuator)
- **End-to-End Tests (Toplag)**: Test af hele systemflow fra sensor til brugerinterface

### CRUD(L) Operations
Vores REST API implementerer fuld CRUD(L) funktionalitet:
- **Create**: `POST /sensors/data` - Opret sensordata
- **Read**: `GET /sensors/data/{id}` - Læs sensordata  
- **Update**: `PUT /sensors/config/{id}` - Opdater konfiguration
- **Delete**: (Implementeret via data rotation)
- **List**: `GET /sensors/data` - List alle sensorer + `GET /sensors/history` - Historik

### Test Cycle Process
Vi følger en struktureret testproces:
1. **Test Planning**: Definer testscenarier baseret på use cases
2. **Test Development**: Udvikl automated tests i PyTest
3. **Test Execution**: Kør tests lokalt og i CI/CD
4. **Result Analysis**: Analyser resultater og fejl
5. **Bug Reporting**: Dokumenter og track fejl
6. **Retesting**: Verificer fixes

### CI/CD Integration
Vores teststrategi integreres i CI/CD pipeline:
- **Automatiserede tests** ved hver commit
- **Code coverage** rapportering
- **Integration tests** med eksterne services
- **Performance tests** for at sikre SLA overholdelse

### Test Types Implementeret
- **Unit Tests**: Enhedstest af individuelle klasser og metoder
- **Integration Tests**: Test af protokol kommunikation (UDP/TCP/MQTT)
- **API Tests**: REST endpoint validation
- **Error Handling**: Test af fejlsituationer (404, 400, network loss)
- **Performance Tests**: Test under network stress (Clumsy 10% packet loss)

### Test Data Management
- **Synthetic Data**: Genereret testdata der matcher produktion
- **Data Isolation**: Tests kører med isolerede datasets
- **Cleanup**: Automatisk oprydning efter testkørsel