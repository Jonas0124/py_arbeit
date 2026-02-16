import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from typing import Dict, List, Tuple

class ServiceCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Service-Rechner")
        self.root.geometry("800x600")
        
        # Konfigurationsdatei für persistente Daten
        self.config_file = ".service_config.json"
        
        # Service-Daten mit Standardwerten
        self.services = [
            {"name": "LO1", "price": 27.85},
            {"name": "LO2", "price": 14.91},
            {"name": "LO3", "price": 6.80},
            {"name": "LO4", "price": 6.80},
            {"name": "LO5", "price": 17.00},
            {"name": "LO6", "price": 6.80},
            {"name": "LO7", "price": 6.80},
            {"name": "LO8", "price": 12.20},
            {"name": "LO9", "price": 23.50},
            {"name": "L10", "price": 3.92},
            {"name": "L11", "price": 9.81},
            {"name": "L12", "price": 9.81},
            {"name": "L13", "price": 35.31},
            {"name": "L14", "price": 23.54},
            {"name": "L15", "price": 3.98},
            {"name": "L15a", "price": 6.93},
            {"name": "L16", "price": 104.61},
            {"name": "L17", "price": 88.26},
            {"name": "L17a", "price": 0.00},
            {"name": "L17b", "price": 0.00},
            {"name": "L16a", "price": 0.00},
            {"name": "L18", "price": 41.39},
            {"name": "L19", "price": 30.53},
            {"name": "L20", "price": 30.53},
            {"name": "L21", "price": 19.68},
            {"name": "L22", "price": 49.69},
            {"name": "L23", "price": 35.31},
            {"name": "L24", "price": 50.21},
            {"name": "L25", "price": 23.73},
            {"name": "L26", "price": 39.36},
            {"name": "L27", "price": 6.80},
            {"name": "L28", "price": 6.80},
            {"name": "L29", "price": 11.51},
            {"name": "L30", "price": 5.23},
            {"name": "L31", "price": 0.68},
            {"name": "L32+L33", "price": 0.68}
        ]
        
        # Lade gespeicherte Konfiguration
        self.load_config()
        
        # GUI-Elemente speichern
        self.quantity_vars = []
        self.price_entries = []
        self.result_label = None
        
        # GUI erstellen
        self.create_widgets()
        
    def load_config(self):
        """Lade gespeicherte Service-Preise aus Konfigurationsdatei"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    saved_prices = json.load(f)
                    for i, service in enumerate(self.services):
                        if str(i) in saved_prices:
                            self.services[i]["price"] = saved_prices[str(i)]
            except Exception as e:
                print(f"Fehler beim Laden der Konfiguration: {e}")
    
    def save_config(self):
        """Speichere aktuelle Service-Preise in Konfigurationsdatei"""
        try:
            prices_to_save = {str(i): service["price"] for i, service in enumerate(self.services)}
            with open(self.config_file, 'w') as f:
                json.dump(prices_to_save, f)
        except Exception as e:
            print(f"Fehler beim Speichern der Konfiguration: {e}")
    
    def create_widgets(self):
        """Erstelle die GUI-Elemente"""
        # Hauptframe
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Titel
        title_label = ttk.Label(main_frame, text="Service-Rechner", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 20))
        
        # Spaltenüberschriften
        headers = ["Service Name", "Preis pro Einheit", "Menge", "Gesamtpreis"]
        for col, header in enumerate(headers):
            header_label = ttk.Label(main_frame, text=header, font=("Arial", 10, "bold"))
            header_label.grid(row=1, column=col, padx=5, pady=5, sticky=tk.W)
        
        # Service-Zeilen erstellen
        for i, service in enumerate(self.services):
            self.create_service_row(main_frame, i, service)
        
        # Trennlinie
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.grid(row=len(self.services) + 2, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=10)
        
        # Zielbetrag-Eingabe
        target_frame = ttk.Frame(main_frame)
        target_frame.grid(row=len(self.services) + 3, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(target_frame, text="Zielbetrag:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
        self.target_var = tk.StringVar(value="")
        target_entry = ttk.Entry(target_frame, textvariable=self.target_var, width=15)
        target_entry.grid(row=0, column=1, padx=5)
        
        # Berechnen-Button
        calculate_btn = ttk.Button(target_frame, text="Berechnen", command=self.calculate_optimal_combination)
        calculate_btn.grid(row=0, column=2, padx=10)
        
        # Ergebnisbereich
        result_frame = ttk.LabelFrame(main_frame, text="Ergebnis", padding="10")
        result_frame.grid(row=len(self.services) + 4, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=10)
        
        self.result_text = tk.Text(result_frame, height=8, width=70, state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Grid-Konfiguration
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(3, weight=1)
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
    
    def create_service_row(self, parent, row_index, service):
        """Erstelle eine Zeile für einen Service"""
        # Service Name (nicht änderbar)
        name_label = ttk.Label(parent, text=service["name"])
        name_label.grid(row=row_index + 2, column=0, padx=5, pady=2, sticky=tk.W)
        
        # Preis (änderbar, muss > 0 sein)
        price_var = tk.StringVar(value=str(service["price"]))
        price_entry = ttk.Entry(parent, textvariable=price_var, width=10)
        price_entry.grid(row=row_index + 2, column=1, padx=5, pady=2)
        
        # Preis-Validierung und Speicherung
        def on_price_change(*args):
            try:
                new_price = int(price_var.get())
                if new_price > 0:
                    self.services[row_index]["price"] = new_price
                    self.save_config()
                else:
                    price_var.set(str(self.services[row_index]["price"]))
            except ValueError:
                price_var.set(str(self.services[row_index]["price"]))
        
        price_var.trace('w', on_price_change)
        self.price_entries.append(price_entry)
        
        # Menge (kann leer sein, wird als 0 behandelt)
        quantity_var = tk.StringVar(value="0")
        quantity_entry = ttk.Entry(parent, textvariable=quantity_var, width=10)
        quantity_entry.grid(row=row_index + 2, column=2, padx=5, pady=2)
        
        # Menge-Validierung
        def on_quantity_change(*args):
            try:
                qty = quantity_var.get().strip()
                if qty == "" or qty.lower() == "null":
                    quantity_var.set("0")
                else:
                    qty_int = int(qty)
                    if qty_int >= 0:
                        quantity_var.set(str(qty_int))
                    else:
                        quantity_var.set("0")
            except ValueError:
                quantity_var.set("0")
        
        quantity_var.trace('w', on_quantity_change)
        self.quantity_vars.append(quantity_var)
        
        # Gesamtpreis (berechnet)
        total_label = ttk.Label(parent, text="0")
        total_label.grid(row=row_index + 2, column=3, padx=5, pady=2, sticky=tk.W)
        
        # Gesamtpreis aktualisieren
        def update_total(*args):
            try:
                price = int(price_var.get())
                quantity = int(quantity_var.get())
                total = price * quantity
                total_label.config(text=str(total))
            except (ValueError, tk.TclError):
                total_label.config(text="0")
        
        price_var.trace('w', update_total)
        quantity_var.trace('w', update_total)
    
    def calculate_optimal_combination(self):
        """Berechne die optimale Kombination von Services"""
        try:
            # Zielbetrag validieren
            target_str = self.target_var.get().strip()
            if not target_str:
                messagebox.showerror("Fehler", "Bitte geben Sie einen Zielbetrag ein.")
                return
            
            target_amount = float(target_str)
            if target_amount <= 0:
                messagebox.showerror("Fehler", "Der Zielbetrag muss größer als 0 sein.")
                return
            
            # Aktuelle Mengen sammeln
            current_quantities = []
            service_prices = []
            
            for i, quantity_var in enumerate(self.quantity_vars):
                try:
                    qty = int(quantity_var.get())
                    current_quantities.append(max(0, qty))  # Negative Werte auf 0 setzen
                    service_prices.append(self.services[i]["price"])
                except (ValueError, tk.TclError):
                    current_quantities.append(0)
                    service_prices.append(self.services[i]["price"])
            
            # Optimale Kombination berechnen
            best_combination, best_total, difference = self.find_best_combination(
                service_prices, current_quantities, target_amount
            )
            
            # Ergebnis anzeigen
            self.display_result(best_combination, best_total, difference, target_amount)
            
        except ValueError:
            messagebox.showerror("Fehler", "Ungültiger Zielbetrag. Bitte geben Sie eine gültige Zahl ein.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {str(e)}")
    
    def find_best_combination(self, prices: List[int], current_quantities: List[int], target: float) -> Tuple[List[int], float, float]:
        """
        Finde die beste Kombination von Services, die dem Zielbetrag am nächsten kommt.
        Jede Menge muss >= 0 sein und mindestens die aktuelle Menge.
        """
        n = len(prices)
        best_combination = current_quantities[:]
        best_total = sum(prices[i] * current_quantities[i] for i in range(n))
        best_difference = abs(best_total - target)
        
        # Begrenze die Suche für Performance
        max_additional = min(100, int(target / min(prices)) + 10) if prices else 0
        
        # Brute-Force-Suche mit Beschränkungen
        def search(current_combo: List[int], index: int):
            nonlocal best_combination, best_total, best_difference
            
            if index == n:
                total = sum(prices[i] * current_combo[i] for i in range(n))
                diff = abs(total - target)
                
                # Verbesserung prüfen
                if diff < best_difference:
                    best_difference = diff
                    best_total = total
                    best_combination = current_combo[:]
                elif diff == best_difference and total > best_total:
                    # Bei gleicher Differenz: höhere Summe bevorzugen
                    best_total = total
                    best_combination = current_combo[:]
                return
            
            # Aktuelle Menge als Minimum verwenden
            min_qty = current_quantities[index]
            
            # Maximale Menge begrenzen
            max_qty = min_qty + max_additional
            
            # Alle möglichen Mengen durchprobieren
            for qty in range(min_qty, max_qty + 1):
                current_combo[index] = qty
                search(current_combo, index + 1)
        
        # Suche starten
        initial_combo = [0] * n
        search(initial_combo, 0)
        
        return best_combination, best_total, best_difference
    
    def display_result(self, combination: List[int], total: float, difference: float, target: float):
        """Zeige das Berechnungsergebnis an"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        
        result = f"Berechnungsergebnis:\n"
        result += "=" * 50 + "\n\n"
        result += f"Zielbetrag: {target:.2f}\n"
        result += f"Berechneter Betrag: {total:.2f}\n"
        result += f"Differenz: {difference:.2f}\n\n"
        result += "Optimale Service-Kombination:\n"
        result += "-" * 30 + "\n"
        
        total_services = 0
        for i, (service, qty) in enumerate(zip(self.services, combination)):
            if qty > 0:
                service_total = service["price"] * qty
                result += f"{service['name']}: {qty} Einheiten × {service['price']} = {service_total}\n"
                total_services += qty
        
        result += f"\nGesamtanzahl Services: {total_services}\n"
        result += f"Gesamtbetrag: {total:.2f}\n"
        
        if difference == 0:
            result += "\n🎯 Perfekte Übereinstimmung!"
        elif difference <= target * 0.01:  # Innerhalb von 1%
            result += f"\n✅ Sehr gute Annäherung (Abweichung: {difference/target*100:.2f}%)"
        else:
            result += f"\n⚠️ Abweichung: {difference/target*100:.2f}%"
        
        self.result_text.insert(tk.END, result)
        self.result_text.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = ServiceCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()