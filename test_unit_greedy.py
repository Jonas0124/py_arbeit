#!/usr/bin/env python3
"""
单元测试：验证贪心算法的核心逻辑
"""

import unittest

def find_best_combination(prices, current_quantities, target):
    """
    贪心算法 + 最小服务微调方案的核心实现
    """
    n = len(prices)
    if n == 0:
        return [], 0, target
    
    # 过滤有效服务（价格>0且有库存）
    valid_items = [(prices[i], i) for i in range(n) if prices[i] > 0 and current_quantities[i] > 0]
    if not valid_items:
        return [0] * n, 0, target
    
    # 按价格从大到小排序
    valid_items.sort(reverse=True)
    
    combo = [0] * n
    remaining_target = target
    
    # 第一步：用大服务快速接近目标（贪心）
    for price, idx in valid_items[:-1]:  # 除了最小的服务
        if remaining_target <= 0:
            break
        # 计算可以使用的最大数量（不超过库存）
        max_allowed = current_quantities[idx]
        # 计算需要的数量
        needed_qty = int(remaining_target / price)
        # 实际使用数量
        actual_qty = min(needed_qty, max_allowed)
        
        if actual_qty > 0:
            combo[idx] = actual_qty
            remaining_target -= price * actual_qty
    
    # 第二步：用最小价格服务精确调整
    if remaining_target > 0 and valid_items:
        min_price, min_idx = valid_items[-1]  # 最小价格服务
        min_max_allowed = current_quantities[min_idx]
        
        # 计算需要的最小服务数量
        if remaining_target > 0:
            needed_min_qty = int(remaining_target / min_price)
            # 允许稍微超过一点点来达到目标
            if needed_min_qty * min_price < remaining_target:
                needed_min_qty += 1
            
            # 实际使用数量（不超过库存）
            actual_min_qty = min(needed_min_qty, min_max_allowed)
            combo[min_idx] = actual_min_qty
            remaining_target -= min_price * actual_min_qty
    
    # 第三步：确保结果在输入约束内
    for i in range(n):
        combo[i] = min(combo[i], current_quantities[i])
    
    # 计算最终结果
    total = sum(prices[i] * combo[i] for i in range(n))
    difference = abs(total - target)
    
    return combo, total, difference

class TestGreedyAlgorithm(unittest.TestCase):
    
    def test_basic_case(self):
        """测试基本案例"""
        prices = [100, 50, 20, 10, 5, 1]
        quantities = [10, 10, 10, 10, 10, 10]
        target = 173
        
        combo, total, difference = find_best_combination(prices, quantities, target)
        
        # 验证结果
        self.assertEqual(total, 173)
        self.assertEqual(difference, 0)
        self.assertEqual(sum(combo), 6)  # 1+1+1+0+0+3 = 6
        
        # 验证具体组合
        expected_combo = [1, 1, 1, 0, 0, 3]
        self.assertEqual(combo, expected_combo)
    
    def test_large_target(self):
        """测试大目标金额"""
        prices = [100, 50, 25, 10, 5, 1]
        quantities = [20, 20, 20, 20, 20, 20]
        target = 1234
        
        combo, total, difference = find_best_combination(prices, quantities, target)
        
        # 验证结果在合理范围内
        self.assertLessEqual(difference, 5)  # 差异应该很小
        self.assertGreaterEqual(total, target - 5)
        self.assertLessEqual(total, target + 5)
        
        # 验证约束条件
        for i in range(len(combo)):
            self.assertLessEqual(combo[i], quantities[i])
    
    def test_constraint_respect(self):
        """测试约束条件遵守"""
        prices = [100, 50, 25, 10]
        quantities = [1, 2, 1, 5]  # 严格的库存限制
        target = 200
        
        combo, total, difference = find_best_combination(prices, quantities, target)
        
        # 验证没有违反约束
        for i in range(len(combo)):
            self.assertLessEqual(combo[i], quantities[i])
        
        # 验证使用了约束内的最大可能
        used_value = sum(prices[i] * combo[i] for i in range(len(prices)))
        self.assertGreater(used_value, 0)
    
    def test_edge_cases(self):
        """测试边界情况"""
        # 空输入
        combo, total, difference = find_best_combination([], [], 100)
        self.assertEqual(combo, [])
        self.assertEqual(total, 0)
        self.assertEqual(difference, 100)
        
        # 零目标
        combo, total, difference = find_best_combination([10], [10], 0)
        self.assertEqual(total, 0)
        self.assertEqual(difference, 0)
        
        # 无有效服务
        combo, total, difference = find_best_combination([0, -5], [10, 10], 100)
        self.assertEqual(total, 0)
        self.assertEqual(difference, 100)
    
    def test_realistic_scenario(self):
        """测试实际场景"""
        # 使用真实的服务价格数据
        prices = [27.85, 14.91, 6.80, 17.00, 12.20, 23.50, 3.92, 9.81, 35.31, 0.68]
        quantities = [5, 3, 10, 4, 6, 2, 15, 8, 3, 50]
        target = 150.00
        
        combo, total, difference = find_best_combination(prices, quantities, target)
        
        # 验证结果合理性
        self.assertLessEqual(difference, target * 0.1)  # 差异不超过10%
        
        # 验证约束遵守
        for i in range(len(combo)):
            self.assertLessEqual(combo[i], quantities[i])

def run_unit_tests():
    """运行单元测试"""
    print("运行贪心算法单元测试...")
    unittest.main(argv=[''], exit=False, verbosity=2)

if __name__ == "__main__":
    run_unit_tests()