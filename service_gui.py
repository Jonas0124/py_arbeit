import sys
import json
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton, QTableWidget, QTableWidgetItem, QGroupBox, QTextEdit, QMessageBox, QDialog, QFormLayout
from PyQt5.QtCore import Qt


class ServiceCalculatorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_language = "de"  # Standard: Deutsch
        self.project_name = "Service-Rechner"  # 默认项目名称
        self.setWindowTitle(self.project_name)
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
        """Lade gespeicherte Konfiguration (Projektname und Service-Preise)"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config_data = json.load(f)
                    
                    # 加载项目名称
                    if "project_name" in config_data:
                        self.project_name = config_data["project_name"]
                        self.setWindowTitle(self.project_name)
                    
                    # 加载服务数据
                    if "services" in config_data:
                        self.services = config_data["services"]
                    elif "prices" in config_data:  # 兼容旧格式
                        saved_prices = config_data["prices"]
                        for i, service in enumerate(self.services):
                            if str(i) in saved_prices:
                                self.services[i]["price"] = saved_prices[str(i)]
            except Exception as e:
                print(f"Fehler beim Laden der Konfiguration: {e}")

    def save_config(self):
        """Speichere aktuelle Konfiguration (Projektname und Services)"""
        try:
            config_data = {
                "project_name": self.project_name,
                "services": self.services
            }
            with open(self.config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
        except Exception as e:
            print(f"Fehler beim Speichern der Konfiguration: {e}")

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
            
        # Sprachauswahl-Button (顶部右侧)
        lang_layout = QHBoxLayout()
        lang_layout.addStretch()
        self.lang_btn = QPushButton("DE")
        self.lang_btn.setFixedSize(40, 25)
        self.lang_btn.clicked.connect(self.toggle_language)
        lang_layout.addWidget(self.lang_btn)
        layout.addLayout(lang_layout)
        
        # Hauptlayout: Horizontal teilen in Tabelle und Ergebnis
        main_layout = QHBoxLayout()
        
        # Linke Seite: Servicetabelle
        self.table_group = QGroupBox("Service-Liste")
        table_layout = QVBoxLayout()
        
        # 表格 (4 Spalten: Name, Preis, Menge, Löschen) + 1额外行用于新增
        self.table = QTableWidget(len(self.services) + 1, 4)
        self.table.setHorizontalHeaderLabels(["Service-Name", "Preis pro Einheit", "Menge", "Löschen"])
        self.table.setColumnWidth(0, 120)  # Name
        self.table.setColumnWidth(1, 80)   # Preis
        self.table.setColumnWidth(2, 60)   # Menge (kleiner)
        self.table.setColumnWidth(3, 60)   # Löschen Button
        
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
        
        # 填充现有服务行
        for i, service in enumerate(self.services):
            # 服务名称输入框
            name_edit = QLineEdit(service["name"])
            name_edit.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(i, 0, name_edit)
            name_edit.textChanged.connect(lambda text, idx=i: self.on_service_name_changed(idx, text))
            
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
            def make_price_validator(edit_widget, service_index):
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

            price_edit.textChanged.connect(make_price_validator(price_edit, i))
            
            # 删除按钮
            delete_btn = QPushButton("-")
            delete_btn.setFixedSize(25, 25)
            delete_btn.clicked.connect(lambda checked, idx=i: self.delete_service(idx))
            self.table.setCellWidget(i, 3, delete_btn)
        
        # 添加新增服务行
        self.setup_add_new_row()
        
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

    def toggle_language(self):
        # Sicherheitsprüfung: Prüfe ob alle GUI-Elemente existieren
        required_attrs = ['project_name_edit', 'lang_btn', 'table_group', 'result_group', 'target_label', 'calculate_btn']
        for attr in required_attrs:
            if not hasattr(self, attr) or getattr(self, attr) is None:
                return
        
        try:
            if self.current_language == "de":
                self.current_language = "cn"
                self.lang_btn.setText("CN")
                self.project_name_edit.setPlaceholderText("服务计算器")
                self.table_group.setTitle("服务列表")
                self.result_group.setTitle("计算结果")
                self.target_label.setText("目标金额:")
                self.calculate_btn.setText("计算")
                # 更新表格列标题
                self.table.setHorizontalHeaderLabels(["服务名称", "单价", "数量", "删除"])
                # 更新新增行提示文本
                if hasattr(self, 'new_name_edit'):
                    self.new_name_edit.setPlaceholderText("新服务名称")
            else:
                self.current_language = "de"
                self.lang_btn.setText("DE")
                self.project_name_edit.setPlaceholderText("Service-Rechner")
                self.table_group.setTitle("Service-Liste")
                self.result_group.setTitle("Berechnungsergebnis")
                self.target_label.setText("Zielbetrag:")
                self.calculate_btn.setText("Berechnen")
                # 更新表格列标题
                self.table.setHorizontalHeaderLabels(["Service-Name", "Preis pro Einheit", "Menge", "Löschen"])
                # 更新新增行提示文本
                if hasattr(self, 'new_name_edit'):
                    self.new_name_edit.setPlaceholderText("Neuer Service-Name")
        except Exception as e:
            # Bei Fehlern einfach ignorieren
            pass

    # 只展示 calculate()，其余文件保持你原来的不变
    # ===== 只需要替换你文件里的 calculate() 函数 =====

    def on_project_name_changed(self, text):
        """项目名称改变时的处理"""
        self.project_name = text
        self.setWindowTitle(text)
        self.save_config()
    
    def on_service_name_changed(self, index, text):
        """服务名称改变时的处理"""
        if index < len(self.services):
            self.services[index]["name"] = text
            self.save_config()
    
    def delete_service(self, index):
        """删除指定索引的服务"""
        if index >= len(self.services):
            return
            
        service_name = self.services[index]["name"]
        
        # 二次确认对话框
        reply = QMessageBox.question(
            self, 
            'Bestätigung' if self.current_language == 'de' else '确认',
            f'Service "{service_name}" wirklich löschen?' if self.current_language == 'de' 
            else f'确定要删除服务 "{service_name}" 吗?',
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # 从数据中删除
            del self.services[index]
            # 重新构建表格
            self.rebuild_table()
            # 保存配置
            self.save_config()
    
    def setup_add_new_row(self):
        """设置新增服务行"""
        add_row = len(self.services)  # 新增行索引
        
        # 服务名称输入框
        self.new_name_edit = QLineEdit()
        self.new_name_edit.setPlaceholderText("新服务名称" if self.current_language == "cn" else "Neuer Service-Name")
        self.new_name_edit.setAlignment(Qt.AlignCenter)
        self.table.setCellWidget(add_row, 0, self.new_name_edit)
        
        # 单价输入框
        self.new_price_edit = QLineEdit()
        self.new_price_edit.setPlaceholderText("0.00")
        self.new_price_edit.setAlignment(Qt.AlignRight)
        self.table.setCellWidget(add_row, 1, self.new_price_edit)
        
        # 数量输入框（只读，显示提示）
        qty_label = QLabel("新增")
        qty_label.setAlignment(Qt.AlignCenter)
        qty_label.setStyleSheet("color: gray; font-style: italic;")
        self.table.setCellWidget(add_row, 2, qty_label)
        
        # 保存按钮
        save_btn = QPushButton("✓")  # 使用勾号表示保存
        save_btn.setFixedSize(25, 25)
        save_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        save_btn.clicked.connect(self.save_new_service)
        self.table.setCellWidget(add_row, 3, save_btn)
        
        # 价格验证
        def validate_price():
            try:
                price_text = self.new_price_edit.text().strip()
                if not price_text:
                    return
                price = float(price_text)
                if price < 0:
                    self.new_price_edit.setText("0.00")
            except ValueError:
                self.new_price_edit.setText("0.00")
        
        self.new_price_edit.textChanged.connect(validate_price)
    
    def save_new_service(self):
        """保存新增服务"""
        name = self.new_name_edit.text().strip()
        price_text = self.new_price_edit.text().strip()
        
        # 验证输入
        if not name:
            # 如果没有输入名称，给出提示
            self.new_name_edit.setPlaceholderText("请输入服务名称" if self.current_language == "cn" else "Bitte Service-Name eingeben")
            self.new_name_edit.setFocus()
            return
        
        try:
            price = float(price_text) if price_text else 0.00
            if price < 0:
                price = 0.00
        except ValueError:
            price = 0.00
        
        # 添加新服务
        new_service = {"name": name, "price": price}
        self.services.append(new_service)
        
        # 保存配置
        self.save_config()
        
        # 重新构建表格（包括新的新增行）
        self.rebuild_table()
        
        # 给用户反馈
        print(f"新服务已添加: {name} - {price:.2f}€")
    
    def rebuild_table(self):
        """重新构建整个表格"""
        # 清空现有表格
        self.table.setRowCount(len(self.services) + 1)  # +1 for add new row
        
        # 重新填充现有服务
        for i, service in enumerate(self.services):
            # 服务名称输入框
            name_edit = QLineEdit(service["name"])
            name_edit.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(i, 0, name_edit)
            name_edit.textChanged.connect(lambda text, idx=i: self.on_service_name_changed(idx, text))
            
            # 单价输入框
            price_edit = QLineEdit(str(service["price"]))
            price_edit.setAlignment(Qt.AlignRight)
            self.table.setCellWidget(i, 1, price_edit)
            
            # 数量输入框
            qty_edit = QLineEdit()
            qty_edit.setPlaceholderText("0")
            qty_edit.setAlignment(Qt.AlignRight)
            self.table.setCellWidget(i, 2, qty_edit)
            
            def on_text_changed(text, edit_widget=qty_edit):
                if text == "":
                    edit_widget.setPlaceholderText("0")
            
            qty_edit.textChanged.connect(on_text_changed)
            
            # Preis-Validierung
            def make_price_validator(edit_widget, service_index):
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
                        self.services[service_index]["price"] = price
                        self.save_config()
                    except ValueError:
                        edit_widget.setText(f"{self.services[service_index]['price']:.2f}")
                return validator
            
            price_edit.textChanged.connect(make_price_validator(price_edit, i))
            
            # 删除按钮
            delete_btn = QPushButton("-")
            delete_btn.setFixedSize(25, 25)
            delete_btn.clicked.connect(lambda checked, idx=i: self.delete_service(idx))
            self.table.setCellWidget(i, 3, delete_btn)
        
        # 重新设置新增行
        self.setup_add_new_row()
    
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

            # 原始金额
            original_total = sum(prices[i] * quantities[i] for i in range(len(prices)))

            # ⭐ 输入 = 要减少的金额
            reduce_target = float(self.target_edit.text().replace(',', '.'))

            if reduce_target <= 0:
                self.result_label.setText("请输入要减少的金额")
                return

            # =================================================
            # 1️⃣ 生成可减少服务池（每个服务最多减少 qty-1）
            # =================================================
            items = []
            for i in range(len(self.services)):
                qty = quantities[i]
                price = prices[i]

                if qty >= 2 and price > 0:
                    reducible = qty - 1  # ⭐必须保留1个
                    items.append((price, reducible, i))

            # 按价格从大到小 → 优先减少贵的
            items.sort(reverse=True)

            # ===== reduction 数组（删除数量）=====
            reduction = [0] * len(self.services)
            remaining = reduce_target

            # =================================================
            # 2️⃣ Greedy 删除大金额服务
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

            # =================================================
            # 3️⃣ 用最便宜服务微调（允许略超）
            # =================================================
            if remaining > 0 and items:
                min_price, max_reduce, idx = items[-1]
                left = max_reduce - reduction[idx]

                if left > 0:
                    need = int(round(remaining / min_price))
                    need = max(1, min(need, left))
                    reduction[idx] += need
                    remaining -= need * min_price

            # =================================================
            # 4️⃣ 计算最终数量与金额
            # =================================================
            final_qty = [quantities[i] - reduction[i] for i in range(len(quantities))]
            final_total = sum(prices[i] * final_qty[i] for i in range(len(prices)))

            reduced_money = original_total - final_total
            diff = abs(reduced_money - reduce_target)

            # =================================================
            # 5️⃣ 输出结果（全部服务显示）
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
