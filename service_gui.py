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
        
        # 清空按钮
        self.clear_btn = QPushButton("Leeren")
        self.clear_btn.clicked.connect(self.clear_inputs)
        target_layout.addWidget(self.clear_btn)
        
        layout.addLayout(target_layout)

    def clear_inputs(self):
        """清空所有数量输入框和目标金额"""
        try:
            # 清空所有服务的数量输入框
            for i in range(len(self.services)):
                qty_edit = self.table.cellWidget(i, 2)
                if qty_edit:
                    qty_edit.clear()
                    qty_edit.setPlaceholderText("0")
            
            # 清空目标金额输入框
            self.target_edit.clear()
            
            # 清空结果显示区域
            self.result_label.setText("")
            
        except Exception as e:
            # 静默处理错误，避免影响用户体验
            pass
    
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

    # 只展示 calculate()，其余文件保持你原来的不变
    # ===== 只需要替换你文件里的 calculate() 函数 =====

    def calculate(self):
        try:
            # ===== 读取输入 =====
            prices = []
            quantities = []
            for i in range(len(self.services)):
                price = float(self.table.cellWidget(i, 1).text())
                qty_text = self.table.cellWidget(i, 2).text()
                qty = int(qty_text) if qty_text else 0
                prices.append(price)
                quantities.append(qty)

            original_total = sum(prices[i] * quantities[i] for i in range(len(prices)))

            # 输入 = 要减少的金额
            reduce_target = float(self.target_edit.text().replace(',', '.'))
            if reduce_target <= 0:
                self.result_label.setText("请输入要减少的金额")
                return

            # =================================================
            # 1️⃣ 可减少服务池（最多减少 qty-1）
            # =================================================
            items = []
            for i in range(len(self.services)):
                qty = quantities[i]
                price = prices[i]
                if qty >= 2 and price > 0:
                    items.append((price, qty - 1, i))  # 必须保留1个

            items.sort(reverse=True)

            reduction = [0] * len(self.services)
            remaining = reduce_target

            # =================================================
            # 2️⃣ Greedy 删除大金额
            # =================================================
            for price, max_reduce, idx in items:
                if remaining <= 0:
                    break

                max_possible = int(remaining // price)
                use = min(max_possible, max_reduce)

                if use <= 0:
                    continue

                reduction[idx] = use
                remaining -= use * price

            # 当前已减少金额
            current_reduced = reduce_target - remaining

            # =================================================
            # 3️⃣ 最小服务微调（三方案比较 ⭐最终版）
            # =================================================
            best_reduction = reduction[:]
            best_diff = abs(current_reduced - reduce_target)

            if remaining > 0 and items:
                min_price, max_reduce, idx = items[-1]
                left = max_reduce - reduction[idx]

                if left > 0:
                    floor_need = int(remaining // min_price)
                    ceil_need = floor_need + 1

                    candidates = []

                    # floor 方案（不超）
                    if 1 <= floor_need <= left:
                        reduced_money = current_reduced + floor_need * min_price
                        diff = abs(reduced_money - reduce_target)
                        candidates.append((diff, floor_need))

                    # ceil 方案（可能超）
                    if 1 <= ceil_need <= left:
                        reduced_money = current_reduced + ceil_need * min_price
                        diff = abs(reduced_money - reduce_target)
                        candidates.append((diff, ceil_need))

                    # 和“不微调”比较
                    if candidates:
                        best_candidate = min(candidates, key=lambda x: x[0])
                        if best_candidate[0] < best_diff:
                            reduction[idx] += best_candidate[1]
                            remaining -= best_candidate[1] * min_price

            # =================================================
            # 4️⃣ 最终数量与金额
            # =================================================
            final_qty = [quantities[i] - reduction[i] for i in range(len(quantities))]
            final_total = sum(prices[i] * final_qty[i] for i in range(len(prices)))

            reduced_money = original_total - final_total
            diff = abs(reduced_money - reduce_target)

            # =================================================
            # 5️⃣ 输出
            # =================================================
            result = f"💰 原始金额: {original_total:.2f}\n"
            result += f"🎯 目标减少: {reduce_target:.2f}\n"
            result += f"🧾 实际减少: {reduced_money:.2f}\n"
            result += f"📊 剩余金额: {final_total:.2f}\n"
            result += f"🔍 误差: {diff:.2f}\n\n"
            result += "📋 服务变化:\n"

            for i, service in enumerate(self.services):
                if quantities[i] > 0:
                    result += f"{service['name']}: {quantities[i]} → {final_qty[i]}\n"

            self.result_label.setText(result)

        except Exception as e:
            self.result_label.setText(str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = ServiceCalculatorGUI()
    calculator.show()
    sys.exit(app.exec_())
