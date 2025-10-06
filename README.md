# CoolNet IoT Company

<p align="center">
  <img src="image.png" alt="Company logo" width="200"/>
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


## Systemarkitektur


[ Sensorer ] → [ MQTT Broker ] → [ Controller ] → [ Aktuatorer ]

- Sensorer: temperatur, luftfugtighed, strømforbrug
- Controller: central logik i Python
- Aktuatorer: blæser, køleenhed, server-throttle, alarm

#

