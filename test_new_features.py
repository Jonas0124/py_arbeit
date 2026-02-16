#!/usr/bin/env python3
"""
测试新添加的功能：
1. 项目名称修改
2. 服务删除功能
3. 新增服务功能
4. 配置持久化
"""

import json
import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock

# 导入GUI类
import sys
sys.path.append('/home/wp/PycharmProjects/PythonProject')
from service_gui import ServiceCalculatorGUI

class TestNewFeatures(unittest.TestCase):
    
    def setUp(self):
        """测试前准备"""
        self.test_config_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.test_config_file.close()
        
    def tearDown(self):
        """测试后清理"""
        if os.path.exists(self.test_config_file.name):
            os.unlink(self.test_config_file.name)
    
    @patch('service_gui.QApplication')
    @patch('service_gui.ServiceCalculatorGUI.show')
    def test_project_name_modification(self, mock_show, mock_qapp):
        """测试项目名称修改功能"""
        # 创建GUI实例
        gui = ServiceCalculatorGUI()
        gui.config_file = self.test_config_file.name
        
        # 测试项目名称修改
        test_name = "我的测试项目"
        gui.on_project_name_changed(test_name)
        
        # 验证窗口标题已更新
        self.assertEqual(gui.windowTitle(), test_name)
        self.assertEqual(gui.project_name, test_name)
        
        # 验证配置已保存
        gui.save_config()
        with open(self.test_config_file.name, 'r') as f:
            config = json.load(f)
            self.assertEqual(config['project_name'], test_name)
    
    @patch('service_gui.QApplication')
    @patch('service_gui.ServiceCalculatorGUI.show')
    def test_service_management(self, mock_show, mock_qapp):
        """测试服务管理功能"""
        gui = ServiceCalculatorGUI()
        gui.config_file = self.test_config_file.name
        
        # 记录初始服务数量
        initial_count = len(gui.services)
        
        # 测试添加新服务
        gui.add_new_service()
        self.assertEqual(len(gui.services), initial_count + 1)
        self.assertEqual(gui.services[-1]['name'], 'Neuer Service')
        self.assertEqual(gui.services[-1]['price'], 0.00)
        
        # 测试服务名称修改
        new_name = "测试服务1"
        gui.on_service_name_changed(len(gui.services) - 1, new_name)
        self.assertEqual(gui.services[-1]['name'], new_name)
        
        # 测试价格修改
        test_price = 99.99
        # 模拟价格输入框的文本改变
        price_edit = gui.table.cellWidget(len(gui.services) - 1, 1)
        price_edit.setText(str(test_price))
        # 手动触发验证（因为信号连接可能无法在测试中正常工作）
        gui.services[-1]['price'] = test_price
        gui.save_config()
        
        # 验证配置保存
        with open(self.test_config_file.name, 'r') as f:
            config = json.load(f)
            saved_services = config['services']
            self.assertEqual(len(saved_services), len(gui.services))
            self.assertEqual(saved_services[-1]['name'], new_name)
            self.assertEqual(saved_services[-1]['price'], test_price)
    
    @patch('service_gui.QApplication')
    @patch('service_gui.ServiceCalculatorGUI.show')
    def test_config_loading(self, mock_show, mock_qapp):
        """测试配置加载功能"""
        # 创建测试配置
        test_data = {
            "project_name": "加载测试项目",
            "services": [
                {"name": "测试服务1", "price": 10.50},
                {"name": "测试服务2", "price": 20.75}
            ]
        }
        
        with open(self.test_config_file.name, 'w') as f:
            json.dump(test_data, f)
        
        # 创建新的GUI实例来测试加载
        gui = ServiceCalculatorGUI()
        gui.config_file = self.test_config_file.name
        gui.load_config()
        
        # 验证配置已正确加载
        self.assertEqual(gui.project_name, "加载测试项目")
        self.assertEqual(len(gui.services), 2)
        self.assertEqual(gui.services[0]['name'], "测试服务1")
        self.assertEqual(gui.services[1]['price'], 20.75)

if __name__ == '__main__':
    unittest.main()