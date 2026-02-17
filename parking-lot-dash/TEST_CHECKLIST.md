# Test Checklist ✅

## Po spuštění aplikace

### 1. Základní funkcionalita

- [ ] Aplikace běží: `http://158.196.15.41:8050`
- [ ] MQTT indikátor je **zelený** ✅
- [ ] Všechny taby se načtou (Dashboard, Osvětlení, Majáčky, Meteostanice, Kamery)
- [ ] Čas se aktualizuje každou sekundu

### 2. Test Ovládání Světel

**V aplikaci:**
- [ ] Změň slider na Stožáru 1 na 50%
- [ ] Klikni "100%" button → slider se změní na 100
- [ ] Klikni "Vypnout vše" na Dashboardu → všechny slidery na 0

**V terminálu:**
```bash
# Otevři nový terminál
mosquitto_sub -h 158.196.15.41 -t "lights/#" -v
```
- [ ] Při změně slideru vidíš zprávy v terminálu

**Testovací zpráva:**
```bash
mosquitto_pub -h 158.196.15.41 \
  -t "lights/device/0003F40B09B3/segment/0/power/set" \
  -m "25"
```
- [ ] Slider se změní na 25% (pokud je tab otevřený)

### 3. Test Majáčků

- [ ] Zapni Majáček 1 (switch)
- [ ] Vypni Majáček 1
- [ ] Klikni "Zapnout" všechny majáčky
- [ ] Klikni "Vypnout" všechny majáčky

### 4. Kontrola Logů

**Aplikační logy (terminál kde běží app):**
```
Connecting to MQTT broker...
✓ Connected to MQTT broker

Starting Dash server on 0.0.0.0:8050
Dash is running on http://0.0.0.0:8050/
```

**MQTT broker logy:**
```bash
sudo tail -f /var/log/mosquitto/mosquitto.log
```
- [ ] Vidíš "New client connected" zprávy
- [ ] Vidíš publish/subscribe aktivity

### 5. Responzivita

- [ ] Otevři na mobilu/tabletu
- [ ] UI se přizpůsobí (cards pod sebou na malé obrazovce)
- [ ] Všechny controls fungují

## Kamery (Po konfiguraci)

### Zjisti IP kamery:
```bash
nmap -sn 10.11.3.0/24
```

### Otestuj přístup:
```bash
# AXIS kamera
curl http://[IP]/axis-cgi/jpg/image.cgi --user admin:password -o test.jpg

# DAHUA kamera
curl http://[IP]/cgi-bin/snapshot.cgi --user admin:password -o test.jpg

# Zobraz
xdg-open test.jpg
```

- [ ] Obdržel jsi obrázek z kamery
- [ ] Přidal jsi IP do `config/devices.py`
- [ ] Implementoval jsi snapshot endpoint (viz CAMERA_INTEGRATION.md)
- [ ] V aplikaci vidíš live snímky

## Performance

- [ ] MQTT zprávy dorazí < 1s
- [ ] UI je responzivní (slider reaguje okamžitě)
- [ ] Žádné chyby v konzoli prohlížeče (F12)
- [ ] CPU usage < 10% (běží na pozadí)

## Integrace se stávajícím systémem

### Kontrola konfliktů:

```bash
# Běží původní Node-RED?
ps aux | grep node-red

# Pokud ano, zastaví na jiném portu?
netstat -tulpn | grep 1880
```

- [ ] Node-RED může běžet současně (jiný port)
- [ ] MQTT broker sdílený mezi oběma aplikacemi
- [ ] Cron skripty stále fungují (`/parkoviste/Lights/`)

### Test s existujícími skripty:

```bash
# Spusť původní Python skript
python3 /parkoviste/Lights/light_power.py 1 50

# V Dash aplikaci:
```
- [ ] Slider Stožáru 1 se aktualizoval na 50%

## Problémy?

### MQTT nepřipojeno (červený indikátor)

```bash
# 1. Zkontroluj broker
systemctl status mosquitto

# 2. Zkontroluj síť
ping 158.196.15.41

# 3. Zkontroluj tunely
ip addr show | grep tap
systemctl status openvpn@*
```

### Světla nereagují

```bash
# Test přímý MQTT
mosquitto_pub -h 158.196.15.41 \
  -t "lights/device/0003F40B09B3/segment/0/power/set" \
  -m "100"
```

- Pokud ani to nefunguje → problém s DALI/hardware
- Pokud funguje → problém v aplikaci

### Port 8050 obsazeno

```bash
# Najdi proces
netstat -tulpn | grep 8050

# Zabiť
sudo pkill -f "python.*app.py"

# Nebo změň port v .env
nano .env
# DASH_PORT=8051
```

## Výsledek

Pokud máš ✅ u všech základních testů → **aplikace funguje správně!**

Pro kamery potřebuješ ještě:
1. Zjistit IP adresy kamer
2. Přidat do konfigurace
3. Implementovat snapshot endpoint

Viz: **CAMERA_INTEGRATION.md**
