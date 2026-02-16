# Service-Rechner

Eine Python GUI-Anwendung zur Berechnung optimaler Service-Kombinationen basierend auf einem Zielbetrag.

## Funktionen

### Hauptmerkmale:
1. **Service-Liste** - Feste Service-Namen in der ersten Spalte
2. **Editierbare Preise** - Service-Preise können geändert werden (müssen > 0 sein)
3. **Mengeneingabe** - Jeder Service kann eine Menge haben (leer/null = 0)
4. **Zielbetrag** - Eingabefeld für gewünschten Gesamtbetrag (> 0)
5. **Optimierungsalgorithmus** - Findet die beste Kombination, die dem Zielbetrag am nächsten kommt

### Technische Eigenschaften:
- **Persistenz**: Geänderte Preise werden in `.service_config.json` (versteckte Datei) gespeichert
- **Validierung**: Alle Eingaben werden auf Gültigkeit geprüft
- **Optimierung**: Algorithmus findet die beste Kombination durch systematische Suche
- **Benutzerfreundlich**: Klare GUI mit sofortigem Feedback

## Installation und Ausführung

### Voraussetzungen:
- Python 3.6 oder höher
- tkinter (normalerweise in Python enthalten)

### Starten der Anwendung:
```bash
python service_calculator.py
```

## Verwendung

1. **Preise anpassen**: Klicken Sie in die "Preis pro Einheit"-Spalte und ändern Sie die Werte
2. **Mengen eingeben**: Geben Sie in die "Menge"-Spalte die gewünschten Mengen ein
3. **Zielbetrag festlegen**: Geben Sie unten rechts den gewünschten Gesamtbetrag ein
4. **Berechnen**: Klicken Sie auf "Berechnen" um die optimale Kombination zu finden

## Algorithmus

Der Rechner verwendet einen systematischen Suchalgorithmus:
- Berücksichtigt die aktuellen Mengen als Mindestwerte
- Sucht durch verschiedene Kombinationen
- Findet die Kombination mit der kleinsten Differenz zum Zielbetrag
- Bei gleicher Differenz wird die höhere Summe bevorzugt

## Dateistruktur

```
├── service_calculator.py     # Haupt-GUI-Anwendung
├── service_logic.py          # Geschäftslogik (ohne GUI)
├── test_service_calculator.py # Unit-Tests
└── .service_config.json      # Persistente Konfiguration (wird automatisch erstellt)
```

## Beispiel

**Services:**
- Service A: 10€
- Service B: 15€
- Service C: 20€
- Service D: 25€
- Service E: 30€

**Zielbetrag:** 65€

**Ergebnis:** 
- Service C: 2 × 20€ = 40€
- Service D: 1 × 25€ = 25€
- **Gesamt: 65€** (perfekte Übereinstimmung!)

## Entwicklung

### Tests ausführen:
```bash
python test_service_calculator.py
```

### Logik testen (ohne GUI):
```bash
python service_logic.py
```

## Anforderungen gemäß Spezifikation

✅ **Linke Spalte**: Service-Namen (fest)
✅ **Zweite Spalte**: Editierbare Preise (> 0, Integer)
✅ **Dritte Spalte**: Mengeneingabe (leer/null = 0)
✅ **Rechte Spalte**: Zielbetrag-Eingabe (> 0)
✅ **Bestätigungsbutton**: "Berechnen"-Button
✅ **Algorithmus**: 
   - Summe der ausgewählten Services ≈ Zielbetrag
   - Beste Annäherung durch Kombination
   - Mengen müssen > 0 sein
   - Mengen ≥ eingetragene Mindestmengen

✅ **Persistenz**: Konfiguration in versteckter Datei im aktuellen Verzeichnis
✅ **Validierung**: Alle Eingaben werden auf Gültigkeit geprüft

## Lizenz

Freie Nutzung für alle Zwecke.