# SystemMonitor

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Lizenz](https://img.shields.io/badge/Lizenz-MIT-green)
![Status](https://img.shields.io/badge/Status-Aktiv-brightgreen)

## 📝 Überblick
`SystemMonitor` ist ein Python-basiertes Skript, das die Systemleistung deines Computers in Echtzeit überwacht. Es zeigt detaillierte Informationen zu CPU, GPU, RAM, Festplattennutzung und Netzwerkstatistiken in einem farbcodierten und tabellarischen Format an.

## ✨ Funktionen
- **Echtzeitüberwachung**: Kontinuierliche Aktualisierung der Systemmetriken.
- **Farbige Ausgabe**: Verbessert die Lesbarkeit durch die Nutzung von `colorama`.
- **GPU-Details**: Zeigt GPU-Auslastung, Temperatur, Speicher und Treiberinformationen an (mit `GPUtil`).
- **Detaillierte CPU-Daten**: Pro-Kern-Auslastung, Frequenz und Temperatur.
- **Umfassende Speicher- und Festplatteninformationen**: Statistiken zu RAM, Swap-Speicher und Festplattenpartitionen.
- **Netzwerkstatistiken**: Zeigt Datenübertragungsraten und Paketdetails an.

## 📋 Voraussetzungen
Stelle sicher, dass die folgenden Python-Pakete installiert sind:
- `psutil` (für die Systemüberwachung)
- `tabulate` (für die Tabellendarstellung)
- `colorama` (für farbige Terminalausgaben)
- `GPUtil` (für GPU-Details)

### Installation
Installiere die benötigten Pakete mit `pip`:
```bash
pip install psutil tabulate colorama gputil
