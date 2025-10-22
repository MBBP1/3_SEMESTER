# CoolNet IoT Company

<p align="center">
  <img src="images/companylogo.png" alt="Company logo" width="200"/>
</p>

#
   -  Hvorfor:
    Formålet med vores virksomhed er at hjælpe virksomheder med at reducere energiforbrug og driftsomkostninger i deres serverrum og datacentre. Overophedning og ineffektiv køling fører ofte til nedbrud og spild af strøm.

   -  Hvordan:
    Vi udvikler IoT-enheder, der måler temperatur, luftfugtighed og strømforbrug i realtid. Data sendes til et centralt system, som sammenligner med forventet temperatur, luftfugtighed og strømforbrug. Hvis værdierne overskrider sikre grænser reguleres kølesystemet yderligere samt server performans begrænses og tekniker alarmeres

   -  Hvad:
    Vores virksomhed hedder CoolNet IoT og opererer inden for grøn IT og datacenter-teknologi. Logoet viser en serverrack med et blå-grønt signalikon, som symboliserer kombinationen af køling, energioptimering og netværksforbindelse.
#

## Protokolvalg
### **Protokol: MQTT (Message Queuing Telemetry Transport)**

**Begrundelse:**
- Designet specifikt til **IoT og M2M-kommunikation**.  
- Understøtter **pålidelig levering (QoS)** trods netværksfejl eller pakketab.  
- Letvægts og energieffektiv → passer til grøn IT.  
- Skalerbar – kan håndtere hundreder af sensorer og aktuatorer.  
- Understøtter **to-vejs kommunikation** (styring af aktuatorer baseret på sensorinput).  

**Underliggende transportlag:** TCP (for stabilitet og fejlretning).

---

### TCP til Aktuatorstyring

Vi bruger TCP til kontrol af aktuatorer fordi:

- **100% pålidelighed** er kritisk når vi styrer kølesystemer og serverperformance
- **Kontrolkommandoer** skal eksekveres præcis én gang - ikke mistes eller duplikeres  
- **Fejlsikring** ved netværksproblemer er afgørende for systemstabilitet

### Aktuatorkommandoer:
- `SET_COOLING` - Justerer kølesystemets effekt
- `SET_PERFORMANCE` - Begrænser server performance ved overophedning
- `ALERT_TECH` - Alarmerer tekniker ved kritiske situationer

Testen beviser at TCP leverer **100% af beskederne** selv med Clumsy sat til 10% pakketab.

![alt text](images/tcp_test01.png)
```
SET_COOLING = 80.0 at Main Cooling
{
  "company": "CoolNet IoT",
  "type": "actuator_command",
  "command": "SET_COOLING",
  "value": 80,
  "location": "Main Cooling",
  "timestamp": "2025-10-22T17:24:46.670932"
}
```
### Test med Clumsy
Vores test beviser at TCP leverer **100% af beskederne** selv når Clumsy er sat til 10% pakketab. Dette demonstrerer at vores kontrolsystem er robust nok til produktionsbrug.


### UDP
![alt text](images/udp_test01.png)
```
{
  "company": "CoolNet IoT",
  "sensor_id": "Sensor_807",
  "timestamp": "2025-10-22T16:43:14.855655",
  "temperature": 26.4,
  "humidity": 36.88,
  "power_consumption": 24.35,
  "type": "server_room_monitoring"
}
```
Vi bruger UDP til at sende sensordata fra vores IoT-enheder i serverrum til vores overvågningssystem.

Hvorfor UDP passer perfekt til os:

    Hastighed over perfekt pålidelighed: Det er vigtigere at få den seneste temperaturmåling (f.eks. 35°C) end at vente på en gammel, tabt pakke (f.eks. 32°C)

    Realtids respons: Vores system skal kunne reagere med det samme ved overophedning - ikke vente på pakkeretransmission

    Tæt datastream: Sensorerne sender data hvert sekund, så et enkelt tabt datapunkt erstattes hurtigt af den næste måling

    Lav overhead: Simpel protokol der passer til vens enkle IoT-enheder

For at demonstrere systemets robusthed testede vi med Clumsy network emulator sat til 10% pakketab. Som stadig modtager over 80% af beskederne selv under netværksforstyrrelser





## Systemarkitektur

[ Sensorer ] → [ MQTT Broker ] → [ Controller ] → [ Aktuatorer ]

- Sensorer: temperatur, luftfugtighed, strømforbrug
- Controller: central logik i Python
- Aktuatorer: blæser, køleenhed, server-throttle, alarm

#

#### How REST API is Used

```
{
  "sensor_id": "temp-001",
  "temperatur": 24.6,
  "luftfugtighed": 56,
  "strøm": 1438,
  "timestamp": "2025-10-21T08:48:56.096079"
}
```

![alt text](images/restapi01.png)

