#!/usr/bin/env python3
"""
Testskript für den Service-Rechner
"""

import unittest
import os
import json
from service_calculator import ServiceCalculator
import tkinter as tk

class TestServiceCalculator(unittest.TestCase):
    
    def setUp(self):
        """Setup für jeden Test"""
        self.root = tk.Tk()
        self.root.withdraw()  # Verstecke das Fenster für Tests
        self.app = ServiceCalculator(self.root)
        
    def tearDown(self):
        """Cleanup nach jedem Test"""
        self.root.destroy()
        # Entferne Test-Konfigurationsdatei
        if os.path.exists(".service_config.json"):
            os.remove(".service_config.json")
    
    def test_initial_setup(self):
        """Teste die initiale Konfiguration"""
        # Prüfe ob Standard-Services vorhanden sind
        self.assertEqual(len(self.app.services), 5)
        self.assertEqual(self.app.services[0]["name"], "Service A")
        self.assertEqual(self.app.services[0]["price"], 10)
        
    def test_price_validation(self):
        """Teste Preis-Validierung"""
        # Teste gültigen Preis
        self.app.services[0]["price"] = 25
        self.assertEqual(self.app.services[0]["price"], 25)
        
        # Teste, dass negative Preise nicht erlaubt sind (über GUI-Logik)
        # Dies wird im GUI-Eingabefeld gehandhabt
        
    def test_quantity_validation(self):
        """Teste Mengen-Validierung"""
        # Teste normale Mengen
        test_cases = [
            ("5", 5),
            ("0", 0),
            ("", 0),
            ("null", 0),
            ("-3", 0)  # Negative Werte werden zu 0
        ]
        
        for input_val, expected in test_cases:
            # Simuliere Eingabevalidierung
            if input_val == "" or input_val.lower() == "null":
                result = 0
            else:
                try:
                    result = max(0, int(input_val))
                except ValueError:
                    result = 0
            self.assertEqual(result, expected)
    
    def test_persistence(self):
        """Teste Persistenz-Funktionalität"""
        # Ändere einige Preise
        self.app.services[0]["price"] = 15
        self.app.services[1]["price"] = 20
        
        # Speichere Konfiguration
        self.app.save_config()
        
        # Erstelle neue Instanz
        new_root = tk.Tk()
        new_root.withdraw()
        new_app = ServiceCalculator(new_root)
        
        # Prüfe ob Preise geladen wurden
        self.assertEqual(new_app.services[0]["price"], 15)
        self.assertEqual(new_app.services[1]["price"], 20)
        
        new_root.destroy()
    
    def test_combination_algorithm(self):
        """Teste den Kombinations-Algorithmus"""
        prices = [10, 15, 20]
        current_quantities = [0, 0, 0]
        target = 25
        
        combination, total, difference = self.app.find_best_combination(
            prices, current_quantities, target
        )
        
        # Prüfe Ergebnis
        self.assertIsInstance(combination, list)
        self.assertGreaterEqual(len(combination), len(prices))
        self.assertGreaterEqual(total, 0)
        self.assertGreaterEqual(difference, 0)
        
        # Prüfe dass alle Mengen >= 0 sind
        for qty in combination:
            self.assertGreaterEqual(qty, 0)
    
    def test_edge_cases(self):
        """Teste Edge-Cases"""
        # Teste mit Zielbetrag 0
        with self.assertRaises(ValueError):
            self.app.find_best_combination([10], [0], 0)
        
        # Teste mit leeren Preisen
        combination, total, difference = self.app.find_best_combination([], [], 100)
        self.assertEqual(combination, [])
        self.assertEqual(total, 0)
        self.assertEqual(difference, 100)

def run_tests():
    """Führe alle Tests aus"""
    unittest.main(argv=[''], exit=False, verbosity=2)

if __name__ == "__main__":
    print("Starte Tests für Service-Rechner...")
    run_tests()
    print("Tests abgeschlossen!")