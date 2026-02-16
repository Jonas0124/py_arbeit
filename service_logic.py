#!/usr/bin/env python3
"""
Vereinfachte Testversion ohne GUI-Abhängigkeiten
"""

import json
import os
from typing import List, Tuple

class ServiceCalculatorLogic:
    """Geschäftslogik des Service-Rechners ohne GUI"""
    
    def __init__(self):
        self.config_file = ".service_config.json"
        self.services = [
            {"name": "Service A", "price": 10},
            {"name": "Service B", "price": 15},
            {"name": "Service C", "price": 20},
            {"name": "Service D", "price": 25},
            {"name": "Service E", "price": 30}
        ]
        self.load_config()
    
    def load_config(self):
        """Lade gespeicherte Service-Preise"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    saved_prices = json.load(f)
                    for i, service in enumerate(self.services):
                        if str(i) in saved_prices:
                            self.services[i]["price"] = saved_prices[str(i)]
            except Exception as e:
                print(f"Fehler beim Laden: {e}")
    
    def save_config(self):
        """Speichere aktuelle Service-Preise"""
        try:
            prices_to_save = {str(i): service["price"] for i, service in enumerate(self.services)}
            with open(self.config_file, 'w') as f:
                json.dump(prices_to_save, f)
        except Exception as e:
            print(f"Fehler beim Speichern: {e}")
    
    def validate_price(self, price_str: str) -> int:
        """Validiere und konvertiere Preis-Eingabe"""
        try:
            price = int(price_str)
            if price > 0:
                return price
            else:
                raise ValueError("Preis muss größer als 0 sein")
        except ValueError:
            raise ValueError("Ungültiger Preis")
    
    def validate_quantity(self, qty_str: str) -> int:
        """Validiere und konvertiere Mengen-Eingabe"""
        qty_str = qty_str.strip().lower()
        if qty_str == "" or qty_str == "null":
            return 0
        try:
            qty = int(qty_str)
            return max(0, qty)
        except ValueError:
            return 0
    
    def find_best_combination(self, prices: List[int], current_quantities: List[int], target: float) -> Tuple[List[int], float, float]:
        """
        Finde die beste Kombination von Services für den Zielbetrag
        """
        n = len(prices)
        if n == 0:
            return [], 0, target
        
        best_combination = current_quantities[:]
        best_total = sum(prices[i] * current_quantities[i] for i in range(n))
        best_difference = abs(best_total - target)
        
        # Suchbegrenzung für Performance
        max_additional = min(50, int(target / min(prices)) + 5) if prices else 0
        
        def search(current_combo: List[int], index: int):
            nonlocal best_combination, best_total, best_difference
            
            if index == n:
                total = sum(prices[i] * current_combo[i] for i in range(n))
                diff = abs(total - target)
                
                if diff < best_difference:
                    best_difference = diff
                    best_total = total
                    best_combination = current_combo[:]
                elif diff == best_difference and total > best_total:
                    best_total = total
                    best_combination = current_combo[:]
                return
            
            min_qty = current_quantities[index]
            max_qty = min_qty + max_additional
            
            for qty in range(min_qty, max_qty + 1):
                current_combo[index] = qty
                search(current_combo, index + 1)
        
        initial_combo = [0] * n
        search(initial_combo, 0)
        
        return best_combination, best_total, best_difference

def demo_calculation():
    """Demo der Berechnungsfunktion"""
    calc = ServiceCalculatorLogic()
    
    print("=== Service-Rechner Demo ===")
    print("\nVerfügbare Services:")
    for i, service in enumerate(calc.services):
        print(f"{service['name']}: {service['price']}€")
    
    # Beispiel-Berechnung
    prices = [service["price"] for service in calc.services]
    current_quantities = [0, 0, 0, 0, 0]  # Alle auf 0
    target_amount = 65.0
    
    print(f"\nSuche optimale Kombination für {target_amount}€")
    
    combination, total, difference = calc.find_best_combination(
        prices, current_quantities, target_amount
    )
    
    print(f"\nErgebnis:")
    print(f"Berechneter Betrag: {total}€")
    print(f"Differenz: {difference}€")
    print("\nKombination:")
    for i, (service, qty) in enumerate(zip(calc.services, combination)):
        if qty > 0:
            subtotal = service["price"] * qty
            print(f"  {service['name']}: {qty} × {service['price']}€ = {subtotal}€")

if __name__ == "__main__":
    demo_calculation()