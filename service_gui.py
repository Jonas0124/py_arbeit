import sys
import json
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton, QTableWidget, QTableWidgetItem, QGroupBox, QTextEdit, QMessageBox, QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class ServiceCalculatorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_language = "de"  # Standard: Deutsch
        self.setWindowTitle("Service-Rechner")
        self.setGeometry(100, 100, 1200, 700)
        
        # Sprachspezifische Texte
        self.language_texts = {
            "de": {
                "title": "Service-Rechner",
                "service_list": "Service-Liste",
                "calculation_result": "Berechnungsergebnis",
                "target_amount": "Zielbetrag:",
                "calculate": "Berechnen",
                "clear": "Leeren",
                "service_name": "Service-Name",
                "price_per_unit": "Preis pro Einheit",
                "quantity": "Menge",
                "original_amount": "💰 Originalbetrag: {:.2f}",
                "target_reduction": "🎯 Zielreduktion: {:.2f}",
                "actual_reduction": "🧾 Tatsächliche Reduktion: {:.2f}",
                "remaining_amount": "📊 Verbleibender Betrag: {:.2f}",
                "error": "🔍 Fehler: {:.2f}",
                "service_changes": "📋 Service-Änderungen:",
                "please_enter_amount": "Bitte geben Sie den zu reduzierenden Betrag ein",
                "save": "Speichern",
                "add_new_service": "Neuen Service hinzufügen",
                "service_exists": "Service mit diesem Namen existiert bereits!",
                "invalid_price": "Ungültiger Preis! Bitte geben Sie eine positive Zahl ein.",
                "invalid_name": "Ungültiger Service-Name!",
                "add_button": "Hinzufügen"
            },
            "cn": {
                "title": "服务计算器",
                "service_list": "服务列表",
                "calculation_result": "计算结果",
                "target_amount": "目标金额:",
                "calculate": "计算",
                "clear": "清空",
                "service_name": "服务名称",
                "price_per_unit": "单价",
                "quantity": "数量",
                "original_amount": "💰 原始金额: {:.2f}",
                "target_reduction": "🎯 目标减少: {:.2f}",
                "actual_reduction": "🧾 实际减少: {:.2f}",
                "remaining_amount": "📊 剩余金额: {:.2f}",
                "error": "🔍 误差: {:.2f}",
                "service_changes": "📋 服务变化:",
                "please_enter_amount": "请输入要减少的金额",
                "save": "保存",
                "add_new_service": "添加新服务",
                "service_exists": "该服务名称已存在！",
                "invalid_price": "无效的价格！请输入正数。",
                "invalid_name": "无效的服务名称！",
                "add_button": "添加"
            }
        }

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
        
        # Services alphabetisch sortieren: zuerst nach Buchstaben, dann nach Groß-/Kleinschreibung
        self.services.sort(key=lambda x: (x["name"].lower(), x["name"]))

        # Lade gespeicherte Konfiguration
        self.load_config()

        # 当前选中的行
        self.selected_row = -1
        
        self.init_ui()

    def load_config(self):
        """Lade gespeicherte Service-Daten aus Konfigurationsdatei"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    saved_data = json.load(f)
                    
                    # 如果是旧格式（只有价格），则只加载价格
                    if isinstance(saved_data, dict) and all(isinstance(k, str) and k.isdigit() for k in saved_data.keys()):
                        # 旧格式：只包含价格
                        for i, service in enumerate(self.services):
                            if str(i) in saved_data:
                                self.services[i]["price"] = saved_data[str(i)]
                        print("已加载旧格式配置（仅价格）")
                    else:
                        # 新格式：包含完整服务信息
                        self.services = saved_data
                        print(f"已加载新格式配置，共 {len(self.services)} 个服务")
                        
            except Exception as e:
                print(f"Fehler beim Laden der Konfiguration: {e}")

    def save_config(self):
        """Speichere aktuelle Service-Daten in Konfigurationsdatei"""
        try:
            # 保存完整的服务数据（名称和价格）
            with open(self.config_file, 'w') as f:
                json.dump(self.services, f, indent=2)
            print(f"配置已保存，共 {len(self.services)} 个服务")
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
        self.table_group = QGroupBox(self.language_texts[self.current_language]["service_list"])
        table_layout = QVBoxLayout()
        
        # 表格 (4 Spalten: Name, Preis, Menge, Aktionen)
        self.table = QTableWidget(len(self.services), 4)
        self.table.setHorizontalHeaderLabels([
            self.language_texts[self.current_language]["service_name"],
            self.language_texts[self.current_language]["price_per_unit"],
            self.language_texts[self.current_language]["quantity"],
            ""
        ])
        self.table.setColumnWidth(0, 180)  # Name (增加宽度)
        self.table.setColumnWidth(1, 120)  # Preis (增加宽度)
        self.table.setColumnWidth(2, 100)  # Menge (增加宽度)
        self.table.setColumnWidth(3, 120)  # Aktionen-Spalte (增加宽度)
        
        table_layout.addWidget(self.table)
        self.table_group.setLayout(table_layout)
        main_layout.addWidget(self.table_group, 2)  # 2/3 des Platzes
        
        # Rechte Seite: Ergebnisanzeige
        self.result_group = QGroupBox(self.language_texts[self.current_language]["calculation_result"])
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
            self.fill_table_row(i, service)
        
        # 添加新服务行
        self.add_new_service_row()
        
        # 连接表格选择信号
        self.table.itemSelectionChanged.connect(self.on_table_selection_changed)
        
        layout.addLayout(main_layout)
        
        # 增大整体字体
        self.increase_font_size()
        
        # 目标金额区域 (unter beiden Spalten)
        target_layout = QHBoxLayout()
        self.target_label = QLabel("Zielbetrag:")
        target_layout.addWidget(self.target_label)
        self.target_edit = QLineEdit()
        self.target_edit.setAlignment(Qt.AlignRight)
        
        # 为目标金额输入添加逗号转点功能
        def on_target_text_changed(text):
            # 使用标志位避免递归调用
            if hasattr(self.target_edit, '_converting') and self.target_edit._converting:
                return
            
            if '，' in text or ',' in text:
                # 设置转换标志
                self.target_edit._converting = True
                try:
                    # 将中文逗号和英文逗号都转换为点
                    normalized_text = text.replace('，', '.').replace(',', '.')
                    self.target_edit.setText(normalized_text)
                    return
                finally:
                    # 清除转换标志
                    self.target_edit._converting = False
        
        self.target_edit.textChanged.connect(on_target_text_changed)
        target_layout.addWidget(self.target_edit)
        self.calculate_btn = QPushButton("Berechnen")
        self.calculate_btn.clicked.connect(self.calculate)
        target_layout.addWidget(self.calculate_btn)
        
        # 清空按钮
        self.clear_btn = QPushButton("Leeren")
        self.clear_btn.clicked.connect(self.clear_inputs)
        target_layout.addWidget(self.clear_btn)
        
        layout.addLayout(target_layout)

    def fill_table_row(self, row_index, service):
        """填充表格行"""
        # 服务名称输入框
        name_edit = QLineEdit(service["name"])
        name_edit.setStyleSheet("padding: 2px; border: 1px solid #ccc;")
        self.table.setCellWidget(row_index, 0, name_edit)
        
        # 连接名称编辑完成信号
        def on_name_editing_finished():
            original_name = service["name"]
            new_name = name_edit.text().strip()
            print(f"服务名称编辑完成: '{original_name}' -> '{new_name}'")
            
            if new_name and new_name != original_name:
                # 检查名称是否重复
                if any(s["name"] == new_name and s is not service for s in self.services):
                    print(f"名称冲突，恢复为原名称: {original_name}")
                    # 恢复原名称
                    name_edit.setText(original_name)
                    QMessageBox.warning(self, 
                                      self.language_texts[self.current_language]["invalid_name"],
                                      self.language_texts[self.current_language]["service_exists"])
                else:
                    # 保存修改但不重新加载表格
                    service["name"] = new_name
                    self.save_config()
                    # 只更新显示，不重新加载整个表格
                    print(f"服务名称已成功更新为: {new_name}")
            else:
                print("名称未改变或为空")
        
        name_edit.editingFinished.connect(on_name_editing_finished)
        
        # 单价输入框
        price_edit = QLineEdit(str(service["price"]))
        price_edit.setAlignment(Qt.AlignRight)
        price_edit.setStyleSheet("padding: 2px; border: 1px solid #ccc;")
        self.table.setCellWidget(row_index, 1, price_edit)
        
        # 数量输入框
        qty_edit = QLineEdit()
        qty_edit.setPlaceholderText("0")
        qty_edit.setAlignment(Qt.AlignRight)
        qty_edit.setStyleSheet("padding: 2px; border: 1px solid #ccc;")
        self.table.setCellWidget(row_index, 2, qty_edit)
        
        # 空白单元格（为新增按钮列保留空间）
        self.table.setCellWidget(row_index, 3, QLabel())

        # 连接信号
        self.setup_input_handlers(name_edit, price_edit, qty_edit, row_index, service)
    
    def setup_input_handlers(self, name_edit, price_edit, qty_edit, row_index, service):
        """设置输入处理函数"""
        # 数量输入处理
        def on_qty_text_changed(text):
            if text == "":
                return
            try:
                val = int(text)
                if val < 0:
                    qty_edit.setText("0")
            except ValueError:
                qty_edit.setText("")
                qty_edit.setPlaceholderText("0")
        
        qty_edit.textChanged.connect(on_qty_text_changed)
        
        # 价格输入处理
        def on_price_text_changed(text):
            if text == "":
                price_edit.setStyleSheet("border: 1px solid #ccc;")
                return
            
            if hasattr(price_edit, '_converting') and price_edit._converting:
                return
            
            if '，' in text or ',' in text:
                price_edit._converting = True
                try:
                    normalized_text = text.replace('，', '.').replace(',', '.')
                    price_edit.setText(normalized_text)
                    return
                finally:
                    price_edit._converting = False
            
            try:
                normalized_text = text.replace(',', '.').replace('，', '.')
                price = float(normalized_text)
                
                if price <= 0:
                    price_edit.setStyleSheet("background-color: #ffe6e6; border: 1px solid red;")
                elif price > 999999:
                    price_edit.setStyleSheet("background-color: #fff3cd; border: 1px solid orange;")
                else:
                    price_edit.setStyleSheet("background-color: #e8f5e8; border: 1px solid green;")
            except ValueError:
                price_edit.setStyleSheet("background-color: #ffe6e6; border: 1px solid red;")
        
        def on_price_editing_finished():
            try:
                text = price_edit.text().strip()
                if text:
                    normalized_text = text.replace('，', '.').replace(',', '.')
                    price = float(normalized_text)
                    if price > 0:
                        rounded_price = round(price, 2)
                        service["price"] = rounded_price
                        self.save_config()
                        if text != f"{rounded_price:.2f}":
                            price_edit.setText(f"{rounded_price:.2f}")
                        price_edit.setStyleSheet("background-color: white; border: 1px solid #ccc;")
            except ValueError:
                pass
        
        price_edit.textChanged.connect(on_price_text_changed)
        price_edit.editingFinished.connect(on_price_editing_finished)
    
    def add_new_service_row(self):
        """添加新服务输入行"""
        row_count = self.table.rowCount()
        self.table.insertRow(row_count)
        
        # 新服务名称输入
        new_name_edit = QLineEdit()
        new_name_edit.setPlaceholderText(self.language_texts[self.current_language]["add_new_service"])
        new_name_edit.setStyleSheet("padding: 2px; border: 2px dashed #ccc; font-style: italic;")
        self.table.setCellWidget(row_count, 0, new_name_edit)
        
        # 新服务价格输入
        new_price_edit = QLineEdit()
        new_price_edit.setPlaceholderText("0.00")
        new_price_edit.setAlignment(Qt.AlignRight)
        new_price_edit.setStyleSheet("padding: 2px; border: 2px dashed #ccc;")
        self.table.setCellWidget(row_count, 1, new_price_edit)
        
        # 空白单元格
        self.table.setCellWidget(row_count, 2, QLabel())
        
        # 保存按钮 - 使用翻译文本，右对齐
        save_btn = QPushButton(f"+ {self.language_texts[self.current_language]['add_button']}")
        save_btn.setFixedSize(65, 25)
        save_btn.setStyleSheet("background-color: #66cc66; color: white; font-weight: bold; border-radius: 3px;")
        
        # 使用水平布局实现右对齐
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(save_btn)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        
        btn_widget = QWidget()
        btn_widget.setLayout(btn_layout)
        self.table.setCellWidget(row_count, 3, btn_widget)
        save_btn.clicked.connect(lambda: self.add_new_service(new_name_edit, new_price_edit))
        
        # 连接回车键保存
        new_name_edit.returnPressed.connect(lambda: self.add_new_service(new_name_edit, new_price_edit))
        new_price_edit.returnPressed.connect(lambda: self.add_new_service(new_name_edit, new_price_edit))
    
    def add_new_service(self, name_edit, price_edit):
        """添加新服务"""
        name = name_edit.text().strip()
        price_text = price_edit.text().strip()
        
        if not name:
            QMessageBox.warning(self, 
                              self.language_texts[self.current_language]["invalid_name"],
                              self.language_texts[self.current_language]["invalid_name"])
            return
        
        # 检查名称是否已存在
        if any(s["name"] == name for s in self.services):
            QMessageBox.warning(self, 
                              self.language_texts[self.current_language]["invalid_name"],
                              self.language_texts[self.current_language]["service_exists"])
            return
        
        try:
            # 处理价格输入
            normalized_price = price_text.replace('，', '.').replace(',', '.')
            price = float(normalized_price)
            if price <= 0:
                raise ValueError()
        except ValueError:
            QMessageBox.warning(self, 
                              self.language_texts[self.current_language]["invalid_price"],
                              self.language_texts[self.current_language]["invalid_price"])
            return
        
        # 添加新服务
        new_service = {"name": name, "price": round(price, 2)}
        self.services.append(new_service)
        self.services.sort(key=lambda x: (x["name"].lower(), x["name"]))
        
        # 重新加载表格
        self.reload_table()
        self.save_config()
        
        # 清空输入框
        name_edit.clear()
        price_edit.clear()


    
    def update_button_texts(self):
        """更新所有按钮的文字为当前语言"""
        # 表格中不再有按钮需要更新
        pass
    
    def reload_table(self):
        """重新加载表格"""
        # 清空表格
        self.table.setRowCount(0)
        
        # 重新填充现有服务
        for i, service in enumerate(self.services):
            self.table.insertRow(i)
            self.fill_table_row(i, service)
        
        # 添加新服务行
        self.add_new_service_row()
        print(f"表格已重新加载，共 {len(self.services)} 个服务")
    
    def on_table_selection_changed(self):
        """表格选择改变事件"""
        selected_items = self.table.selectedItems()
        if selected_items:
            current_row = selected_items[0].row()
            if current_row != self.selected_row:
                self.selected_row = current_row
                self.highlight_selected_row(current_row)
    
    def highlight_selected_row(self, row):
        """高亮选中行 - 更明显的视觉效果"""
        # 先清除之前所有行的高亮
        for r in range(self.table.rowCount()):
            for c in range(self.table.columnCount()):
                item = self.table.item(r, c)
                if item:
                    if r == row:
                        item.setBackground(Qt.blue)  # 选中行蓝色背景
                        item.setForeground(Qt.white)  # 白色文字
                    else:
                        item.setBackground(Qt.white)  # 其他行白色背景
                        item.setForeground(Qt.black)  # 黑色文字
                else:
                    # 对于widget单元格的处理
                    widget = self.table.cellWidget(r, c)
                    if isinstance(widget, QLineEdit):
                        if r == row:
                            widget.setStyleSheet("padding: 2px; border: 1px solid #333; background-color: #4A90E2; color: white;")
                        else:
                            widget.setStyleSheet("padding: 2px; border: 1px solid #ccc; background-color: white; color: black;")
                    elif isinstance(widget, QPushButton):
                        # 不再有按钮需要特殊处理
                        pass
    
    def increase_font_size(self):
        """增大字体大小"""
        font = QFont()
        font.setPointSize(12)  # 增大字体
        
        # 应用到主要组件
        self.setFont(font)
        self.title_label.setFont(QFont("", 18, QFont.Bold))
        self.table.setFont(font)
        self.result_label.setFont(font)
        
        # 安全地应用到目标标签和输入框（如果存在）
        if hasattr(self, 'target_label') and self.target_label:
            self.target_label.setFont(font)
        if hasattr(self, 'target_edit') and self.target_edit:
            self.target_edit.setFont(font)
        
        # 增大表格列标题字体
        header = self.table.horizontalHeader()
        header_font = QFont()
        header_font.setPointSize(11)
        header.setFont(header_font)
    
    def clear_inputs(self):
        """清空所有数量输入框和目标金额"""
        try:
            # 清空所有服务的数量输入框
            for i in range(len(self.services)):
                qty_edit = self.table.cellWidget(i, 2)
                if qty_edit:
                    qty_edit.clear()
                    qty_edit.setPlaceholderText("0")
                    qty_edit.setStyleSheet("")  # 重置样式
            
            # 清空目标金额输入框
            self.target_edit.clear()
            self.target_edit.setStyleSheet("")
            self.target_edit.setPlaceholderText("0.00")
            
            # 清空结果显示区域
            self.result_label.setText("")
            
            # 重置所有价格输入框样式
            for i in range(len(self.services)):
                price_edit = self.table.cellWidget(i, 1)
                if price_edit:
                    price_edit.setStyleSheet("")
            
        except Exception as e:
            # 静默处理错误，避免影响用户体验
            pass

    def toggle_language(self):
        required_attrs = ['title_label', 'lang_btn', 'table_group', 'result_group',
                          'target_label', 'calculate_btn', 'clear_btn']
        for attr in required_attrs:
            if not hasattr(self, attr) or getattr(self, attr) is None:
                return

        try:
            # 切换语言状态
            self.current_language = "cn" if self.current_language == "de" else "de"
            lang = self.language_texts[self.current_language]

            # 更新标题和按钮
            self.lang_btn.setText(self.current_language.upper())
            self.title_label.setText(lang["title"])
            self.table_group.setTitle(lang["service_list"])
            self.result_group.setTitle(lang["calculation_result"])
            self.target_label.setText(lang["target_amount"])
            self.calculate_btn.setText(lang["calculate"])
            self.clear_btn.setText(lang["clear"])

            # 更新表头
            self.table.setHorizontalHeaderLabels([
                lang["service_name"],
                lang["price_per_unit"],
                lang["quantity"]
            ])

            # 更新删除 / 添加按钮
            self.update_button_texts()

            # 更新新服务输入行 placeholder
            if self.table.rowCount() > len(self.services):
                new_row = self.table.rowCount() - 1
                name_widget = self.table.cellWidget(new_row, 0)
                if name_widget:
                    name_widget.setPlaceholderText(lang["add_new_service"])

        except Exception:
            pass

    # 只展示 calculate()，其余文件保持你原来的不变
    # ===== 只需要替换你文件里的 calculate() 函数 =====

    def calculate(self):
        try:
            # ===== 读取输入 =====
            prices = []
            quantities = []
            for i in range(len(self.services)):
                # 读取单价并处理逗号
                price_text = self.table.cellWidget(i, 1).text()
                # 处理中文逗号和英文逗号
                normalized_price = price_text.replace('，', '.').replace(',', '.')
                price = float(normalized_price)
                qty_text = self.table.cellWidget(i, 2).text()
                qty = int(qty_text) if qty_text else 0
                prices.append(price)
                quantities.append(qty)

            original_total = sum(prices[i] * quantities[i] for i in range(len(prices)))

            # 输入 = 要减少的金额
            target_text = self.target_edit.text()
            # 处理中文逗号和英文逗号
            normalized_target = target_text.replace('，', '.').replace(',', '.')
            reduce_target = float(normalized_target)
            if reduce_target <= 0:
                self.result_label.setText(self.language_texts[self.current_language]["please_enter_amount"])
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

                    # 和"不微调"比较
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
            # 5️⃣ 输出 - 使用当前语言
            # =================================================
            lang = self.language_texts[self.current_language]
            result = f"{lang['original_amount'].format(original_total)}\n"
            result += f"{lang['target_reduction'].format(reduce_target)}\n"
            result += f"{lang['actual_reduction'].format(reduced_money)}\n"
            result += f"{lang['remaining_amount'].format(final_total)}\n"
            result += f"{lang['error'].format(diff)}\n\n"
            result += f"{lang['service_changes']}\n"

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
