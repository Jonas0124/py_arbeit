#!/usr/bin/env python3
"""
测试贪心算法 + 最小服务微调方案
"""

import sys
sys.path.append('/home/wp/PycharmProjects/PythonProject')

from service_calculator import ServiceCalculator
import tkinter as tk

def test_greedy_approach():
    """测试贪心算法方法"""
    
    # 创建计算器实例
    root = tk.Tk()
    root.withdraw()  # 隐藏窗口
    calc = ServiceCalculator(root)
    
    print("=== 测试贪心算法 + 最小服务微调方案 ===\n")
    
    # 获取实际的服务价格
    prices = [service["price"] for service in calc.services]
    service_names = [service["name"] for service in calc.services]
    
    print("可用服务列表:")
    for i, (name, price) in enumerate(zip(service_names, prices)):
        print(f"  {i:2d}. {name:>8s}: {price:6.2f}")
    
    print(f"\n总服务数: {len(prices)}")
    print(f"最小价格: {min([p for p in prices if p > 0]):.2f}")
    print(f"最大价格: {max(prices):.2f}")
    
    # 测试用例1: 目标金额500
    print("\n" + "="*50)
    print("测试用例1: 目标金额 500.00")
    print("="*50)
    
    target_amount = 500.00
    # 设置所有服务的库存为足够大
    current_quantities = [1000] * len(prices)  # 每个服务都有1000个库存
    
    combination, total, difference = calc.find_best_combination(
        prices, current_quantities, target_amount
    )
    
    print(f"\n结果分析:")
    print(f"目标金额: {target_amount:.2f}")
    print(f"计算金额: {total:.2f}")
    print(f"差异: {difference:.2f} ({difference/target_amount*100:.4f}%)")
    
    print(f"\n详细组合:")
    used_services = []
    for i, qty in enumerate(combination):
        if qty > 0:
            subtotal = prices[i] * qty
            print(f"  {service_names[i]:>8s}: {qty:3d} × {prices[i]:6.2f} = {subtotal:8.2f}")
            used_services.append((i, qty, prices[i], subtotal))
    
    print(f"\n总计: {sum(qty*price for _, qty, price, _ in used_services):.2f}")
    print(f"使用服务种类: {len(used_services)}")
    
    # 测试用例2: 更大的目标金额
    print("\n" + "="*50)
    print("测试用例2: 目标金额 1500.98")
    print("="*50)
    
    target_amount2 = 1500.98
    combination2, total2, difference2 = calc.find_best_combination(
        prices, current_quantities, target_amount2
    )
    
    print(f"\n结果分析:")
    print(f"目标金额: {target_amount2:.2f}")
    print(f"计算金额: {total2:.2f}")
    print(f"差异: {difference2:.2f} ({difference2/target_amount2*100:.4f}%)")
    
    print(f"\n详细组合:")
    used_services2 = []
    for i, qty in enumerate(combination2):
        if qty > 0:
            subtotal = prices[i] * qty
            print(f"  {service_names[i]:>8s}: {qty:3d} × {prices[i]:6.2f} = {subtotal:8.2f}")
            used_services2.append((i, qty, prices[i], subtotal))
    
    print(f"\n总计: {sum(qty*price for _, qty, price, _ in used_services2):.2f}")
    print(f"使用服务种类: {len(used_services2)}")
    
    # 测试约束条件
    print("\n" + "="*50)
    print("测试约束条件验证")
    print("="*50)
    
    # 设置有限的库存
    limited_quantities = [5, 3, 2, 1, 0] + [10] * (len(prices) - 5)  # 前几个服务限制库存
    
    print("设置有限库存:")
    for i in range(min(5, len(prices))):
        print(f"  {service_names[i]:>8s}: {limited_quantities[i]} 个")
    
    target_amount3 = 200.00
    combination3, total3, difference3 = calc.find_best_combination(
        prices, limited_quantities, target_amount3
    )
    
    print(f"\n结果分析 (有限库存):")
    print(f"目标金额: {target_amount3:.2f}")
    print(f"计算金额: {total3:.2f}")
    print(f"差异: {difference3:.2f}")
    
    print(f"\n验证约束条件:")
    constraint_violated = False
    for i, qty in enumerate(combination3):
        if qty > limited_quantities[i]:
            print(f"❌ 违反约束: {service_names[i]} 使用了 {qty} 个，但限制为 {limited_quantities[i]} 个")
            constraint_violated = True
    
    if not constraint_violated:
        print("✅ 所有数量都在约束范围内")
    
    # 清理
    root.destroy()

def demonstrate_step_by_step():
    """演示逐步计算过程"""
    print("\n" + "="*60)
    print("逐步演示计算过程")
    print("="*60)
    
    # 简化的示例
    prices = [100, 50, 20, 10, 5, 1]  # 从大到小排列的价格
    quantities = [10, 10, 10, 10, 10, 10]  # 每个服务都有10个库存
    target = 173  # 目标金额
    
    print(f"示例配置:")
    print(f"服务价格: {prices}")
    print(f"服务库存: {quantities}")
    print(f"目标金额: {target}")
    
    # 模拟算法步骤
    print(f"\n步骤1 - 用大服务快速接近:")
    remaining = target
    used = [0] * len(prices)
    
    # 除了最小的服务
    for i in range(len(prices)-1):
        price = prices[i]
        max_allowed = quantities[i]
        needed = int(remaining / price)
        actual = min(needed, max_allowed)
        
        if actual > 0:
            used[i] = actual
            remaining -= price * actual
            print(f"  使用 {actual} 个价格为 {price} 的服务，剩余: {remaining}")
    
    print(f"\n步骤2 - 用最小服务精确调整:")
    if remaining > 0:
        min_price = prices[-1]
        min_allowed = quantities[-1]
        needed_min = int(remaining / min_price)
        if needed_min * min_price < remaining:
            needed_min += 1
        
        actual_min = min(needed_min, min_allowed)
        used[-1] = actual_min
        remaining -= min_price * actual_min
        print(f"  使用 {actual_min} 个价格为 {min_price} 的服务，剩余: {remaining}")
    
    total = sum(prices[i] * used[i] for i in range(len(prices)))
    difference = abs(total - target)
    
    print(f"\n最终结果:")
    print(f"组合: {used}")
    print(f"总金额: {total}")
    print(f"差异: {difference}")

if __name__ == "__main__":
    test_greedy_approach()
    demonstrate_step_by_step()
    print("\n测试完成!")