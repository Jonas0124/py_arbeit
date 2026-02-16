import sys
import json
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton, QTableWidget, QTableWidgetItem, QGroupBox, QTextEdit
from PyQt5.QtCore import Qt


class ServiceCalculatorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_language = "de"  # Standard: Deutsch
        self.setWindowTitle("Service-Rechner")
        self.setGeometry(100, 100, 1200, 700)

        # Konfigurationsdatei für persistente Daten
        self.config_file = ".service_config.json"

        # 服务数据（您的表格数据）
        self.services = [
            {"name": "L01", "price": 27.85}, {"name": "L02", "price": 14.91}, {"name": "L03", "price": 6.80},
            {"name": "L04", "price": 6.80}, {"name": "L05", "price": 17.00}, {"name": "L06", "price": 6.80},
            {"name": "L07", "price": 6.80}, {"name": "L08", "price": 12.23}, {"name": "L09", "price": 23.54},
            {"name": "L10", "price": 3.92}, {"name": "L11", "price": 9.81}, {"name": "L12", "price": 9.81},
            {"name": "L13", "price": 35.31}, {"name": "L14", "price": 23.54}, {"name": "L15", "price": 3.98},
            {"name": "L15a", "price": 6.93}, {"name": "L16", "price": 104.61}, {"name": "L17", "price": 88.26},
            {"name": "L17a", "price": 0.00}, {"name": "L17b", "price": 0.00}, {"name": "L16a", "price": 0.00},
            {"name": "L18", "price": 41.39}, {"name": "L19", "price": 30.53}, {"name": "L20", "price": 30.53},
            {"name": "L21", "price": 19.68}, {"name": "L22", "price": 49.69}, {"name": "L23", "price": 35.31},
            {"name": "L24", "price": 50.21}, {"name": "L25", "price": 23.73}, {"name": "L26", "price": 39.36},
            {"name": "L27", "price": 6.80}, {"name": "L28", "price": 6.80}, {"name": "L29", "price": 11.51},
            {"name": "L30", "price": 5.23}, {"name": "L31", "price": 0.68}, {"name": "L32+L33", "price": 0.68}
        ]

        # Lade gespeicherte Konfiguration
        self.load_config()

        self.init_ui()

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

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Titel und Sprachauswahl
        title_layout = QHBoxLayout()
        
        # Titel
        self.title_label = QLabel("Service-Rechner")
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.title_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(self.title_label)
        
        # Sprachauswahl-Button
        self.lang_btn = QPushButton("DE")
        self.lang_btn.setFixedSize(40, 25)
        self.lang_btn.clicked.connect(self.toggle_language)
        title_layout.addStretch()
        title_layout.addWidget(self.lang_btn)
        
        layout.addLayout(title_layout)
        
        # Hauptlayout: Horizontal teilen in Tabelle und Ergebnis
        main_layout = QHBoxLayout()
        
        # Linke Seite: Servicetabelle
        self.table_group = QGroupBox("Service-Liste")
        table_layout = QVBoxLayout()
        
        # 表格 (3 Spalten: Name, Preis, Menge)
        self.table = QTableWidget(len(self.services), 3)
        self.table.setHorizontalHeaderLabels(["Service-Name", "Preis pro Einheit", "Menge"])
        self.table.setColumnWidth(0, 120)  # Name
        self.table.setColumnWidth(1, 80)   # Preis
        self.table.setColumnWidth(2, 60)   # Menge (kleiner)
        
        table_layout.addWidget(self.table)
        self.table_group.setLayout(table_layout)
        main_layout.addWidget(self.table_group, 2)  # 2/3 des Platzes
        
        # Rechte Seite: Ergebnisanzeige
        self.result_group = QGroupBox("Berechnungsergebnis")
        result_layout = QVBoxLayout()
        self.result_label = QLabel("")
        self.result_label.setWordWrap(True)
        self.result_label.setStyleSheet("background-color: #f0f0f0; padding: 10px; border: 1px solid #ccc;")
        self.result_label.setMinimumWidth(300)
        result_layout.addWidget(self.result_label)
        self.result_group.setLayout(result_layout)
        main_layout.addWidget(self.result_group, 1)  # 1/3 des Platzes
        
        # 填充表格
        for i, service in enumerate(self.services):
            self.table.setItem(i, 0, QTableWidgetItem(service["name"]))
            
            # 单价输入框
            price_edit = QLineEdit(str(service["price"]))
            price_edit.setAlignment(Qt.AlignRight)
            self.table.setCellWidget(i, 1, price_edit)
            
            # 数量输入框 - stabile Implementierung ohne Event-Probleme
            qty_edit = QLineEdit()
            qty_edit.setPlaceholderText("0")
            qty_edit.setAlignment(Qt.AlignRight)
            self.table.setCellWidget(i, 2, qty_edit)
            
            # Einfache Signal-basierte Lösung (stabil unter Wayland)
            def on_text_changed(text):
                # Bei leerem Text den Placeholder anzeigen
                if text == "":
                    qty_edit.setPlaceholderText("0")
            
            qty_edit.textChanged.connect(on_text_changed)
            
            # Preis-Validierung und Speicherung
            def make_validator(edit_widget, service_index):
                def validator():
                    try:
                        price_text = edit_widget.text().strip()
                        if not price_text:
                            edit_widget.setText(f"{self.services[service_index]['price']:.2f}")
                            return

                        price = float(price_text)
                        if price <= 0:
                            edit_widget.setText(f"{self.services[service_index]['price']:.2f}")
                            return

                        # Preis aktualisieren und speichern
                        self.services[service_index]["price"] = price
                        self.save_config()
                        
                    except ValueError:
                        edit_widget.setText(f"{self.services[service_index]['price']:.2f}")

                return validator

            price_edit.textChanged.connect(make_validator(price_edit, i))
        
        layout.addLayout(main_layout)
        
        # 目标金额区域 (unter beiden Spalten)
        target_layout = QHBoxLayout()
        self.target_label = QLabel("Zielbetrag:")
        target_layout.addWidget(self.target_label)
        self.target_edit = QLineEdit()
        self.target_edit.setAlignment(Qt.AlignRight)
        target_layout.addWidget(self.target_edit)
        self.calculate_btn = QPushButton("Berechnen")
        self.calculate_btn.clicked.connect(self.calculate)
        target_layout.addWidget(self.calculate_btn)
        layout.addLayout(target_layout)

    def toggle_language(self):
        # Sicherheitsprüfung: Prüfe ob alle GUI-Elemente existieren
        required_attrs = ['title_label', 'lang_btn', 'table_group', 'result_group', 'target_label', 'calculate_btn']
        for attr in required_attrs:
            if not hasattr(self, attr) or getattr(self, attr) is None:
                return
        
        try:
            if self.current_language == "de":
                self.current_language = "cn"
                self.lang_btn.setText("CN")
                self.title_label.setText("服务计算器")
                self.table_group.setTitle("服务列表")
                self.result_group.setTitle("计算结果")
                self.target_label.setText("目标金额:")
                self.calculate_btn.setText("计算")
            else:
                self.current_language = "de"
                self.lang_btn.setText("DE")
                self.title_label.setText("Service-Rechner")
                self.table_group.setTitle("Service-Liste")
                self.result_group.setTitle("Berechnungsergebnis")
                self.target_label.setText("Zielbetrag:")
                self.calculate_btn.setText("Berechnen")
        except Exception as e:
            # Bei Fehlern einfach ignorieren
            pass

    def calculate(self):
        try:
            # Berechne Originaltotal
            original_total = 0
            for i in range(len(self.services)):
                price_text = self.table.cellWidget(i, 1).text()
                qty_text = self.table.cellWidget(i, 2).text()
                price = float(price_text) if price_text else 0
                qty = int(qty_text) if qty_text and qty_text.strip() not in ["", "null"] else 0
                original_total += price * qty

            target_text = self.target_edit.text().strip()
            if not target_text:
                if self.current_language == "de":
                    self.result_label.setText("Bitte geben Sie einen Zielbetrag ein")
                else:
                    self.result_label.setText("请输入目标金额")
                return

            # Ersetze Komma durch Punkt für Dezimalzahlen
            target_text_clean = target_text.replace(',', '.')
            target_amount = float(target_text_clean)
            if target_amount <= 0:
                if self.current_language == "de":
                    self.result_label.setText("Der Zielbetrag muss größer als 0 sein")
                else:
                    self.result_label.setText("目标金额必须大于0")
                return

            # 获取当前 Daten und filtere Services mit quantity > 0
            prices = []
            quantities = []
            service_indices = []
            for i, service in enumerate(self.services):
                price_text = self.table.cellWidget(i, 1).text()
                qty_text = self.table.cellWidget(i, 2).text()

                price = float(price_text) if price_text else 0
                qty = int(qty_text) if qty_text and qty_text.strip() not in ["", "null"] else 0

                # Nur Services mit qty > 0 berücksichtigen
                if self.services[i]["price"] > 0 and qty > 0:
                    prices.append(price)
                    quantities.append(qty)
                    service_indices.append(i)

            if not prices:
                if self.current_language == "de":
                    self.result_label.setText("Keine Services mit Menge > 0 ausgewählt")
                else:
                    self.result_label.setText("Keine Services mit Menge > 0 ausgewählt")
                return

            # Optimierter Algorithmus: Prüfe jede einzelne Service-Art + kleine Kombinationen
            best_total = 0
            min_diff = float('inf')
            best_combo = [0] * len(self.services)

            # Option 1: Jede einzelne Service-Art für sich
            for j in range(len(prices)):
                max_qty = min(quantities[j] - 1, int(target_amount / prices[j]) + 1)
                if max_qty > 0:
                    total = prices[j] * max_qty
                    diff = abs(total - target_amount)
                    if diff < min_diff:
                        min_diff = diff
                        best_total = total
                        best_combo = [0] * len(self.services)
                        best_combo[service_indices[j]] = max_qty

            # Option 2: Kleine Kombinationen (max 3 Services)
            from itertools import combinations
            for r in range(2, min(4, len(prices) + 1)):  # 2 oder 3 Services
                for combo_indices in combinations(range(len(prices)), r):
                    # Für diese Kombination: greedy mit begrenzter Suche
                    total = 0
                    combo = [0] * len(prices)

                    # Sortiere nach Preis (aufsteigend) für bessere Heuristik
                    sorted_idx = sorted(combo_indices, key=lambda x: prices[x])

                    remaining = target_amount
                    for idx in sorted_idx:
                        max_qty = min(quantities[idx] - 1, int(remaining / prices[idx]) + 1)
                        if max_qty > 0:
                            qty = max_qty
                            subtotal = prices[idx] * qty
                            total += subtotal
                            combo[idx] = qty
                            remaining -= subtotal
                            if remaining <= 0:
                                break

                    diff = abs(total - target_amount)
                    if diff < min_diff:
                        min_diff = diff
                        best_total = total
                        best_combo = [0] * len(self.services)
                        for j, idx in enumerate(sorted_idx):
                            best_combo[service_indices[idx]] = combo[idx]

            # Ergebnis als einfacher Text (ohne HTML)
            if self.current_language == "de":
                result = f"🎯 Zielbetrag: {target_amount:.2f}\n"
                result += f"💰 Originalbetrag: {original_total:.2f} (Ihre Eingabe: Menge × Preis)\n"
                result += f"🔴 Gesamtdifferenz: {original_total - best_total:.2f} (Originalbetrag - Berechneter Betrag)\n"
                result += f"✅ Berechneter Betrag: {best_total:.2f}\n"
                result += f"🔍 Gesamtdifferenz: {min_diff:.2f} ({min_diff / target_amount * 100:.2f}%)\n\n"
                result += "📋 Service-Änderungsdetails:\n"
                for i, service in enumerate(self.services):
                    qty_input_text = self.table.cellWidget(i, 2).text()
                    qty_input = int(qty_input_text) if qty_input_text and qty_input_text.strip() not in ["", "null"] else 0
                    qty_calc = best_combo[i]

                    if qty_input > 0:
                        if qty_calc == 0:
                            result += f"  {service['name']}: Eingabemenge: {qty_input}\n"
                        elif qty_calc < qty_input:
                            diff_qty = qty_input - qty_calc
                            result += f"  {service['name']}: Differenz: {diff_qty} (Eingabe: {qty_input} → Berechnung: {qty_calc})\n"
                        else:
                            result += f"  {service['name']}: Keine Änderung: {qty_input}\n"
                result += "\n💡 Hinweis: Berechnete Menge < Eingabemenge (streng kleiner)"
            else:
                result = f"🎯 目标金额: {target_amount:.2f}\n"
                result += f"💰 原始总金额: {original_total:.2f} (您输入的数量 × 单价)\n"
                result += f"🔴 总差额: {original_total - best_total:.2f} (原始总金额 - 计算金额)\n"
                result += f"✅ 计算金额: {best_total:.2f}\n"
                result += f"🔍 总差异: {min_diff:.2f} ({min_diff / target_amount * 100:.2f}%)\n\n"
                result += "📋 服务变更详情:\n"
                for i, service in enumerate(self.services):
                    qty_input_text = self.table.cellWidget(i, 2).text()
                    qty_input = int(qty_input_text) if qty_input_text and qty_input_text.strip() not in ["", "null"] else 0
                    qty_calc = best_combo[i]

                    if qty_input > 0:
                        if qty_calc == 0:
                            result += f"  {service['name']}: 输入量: {qty_input}\n"
                        elif qty_calc < qty_input:
                            diff_qty = qty_input - qty_calc
                            result += f"  {service['name']}: 差值: {diff_qty} (输入{qty_input}→计算{qty_calc})\n"
                        else:
                            result += f"  {service['name']}: 无变化: {qty_input}\n"
                result += "\n💡 说明: 计算量 < 输入量 (严格小于)"

            self.result_label.setText(result)

        except Exception as e:
            if self.current_language == "de":
                self.result_label.setText(f"Fehler: {str(e)}")
            else:
                self.result_label.setText(f"计算错误: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = ServiceCalculatorGUI()
    calculator.show()
    sys.exit(app.exec_())
