#!/usr/bin/env python3
"""
测试贪心算法 + 最小服务微调方案 (无GUI版本)
"""

def find_best_combination(prices, current_quantities, target):
    """
    贪心算法 + 最小服务微调方案
    第一步：用大服务快速接近目标（贪心）
    第二步：用最小价格服务精确调整剩余误差
    第三步：确保结果在输入约束内
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
    
    print(f"\n开始计算 - 目标金额: {target:.2f}")
    print(f"可用服务: {[f'{prices[i]}({current_quantities[i]})' for _, i in valid_items]}")
    
    # 第一步：用大服务快速接近目标（贪心）
    print("\n步骤1 - 用大服务快速接近目标:")
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
            print(f"  使用 {actual_qty} 个价格为 {price} 的服务，剩余目标: {remaining_target:.2f}")
    
    # 第二步：用最小价格服务精确调整
    print("\n步骤2 - 用最小价格服务精确调整:")
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
            print(f"  使用 {actual_min_qty} 个价格为 {min_price} 的服务，剩余目标: {remaining_target:.2f}")
    
    # 第三步：确保结果在输入约束内
    # 验证所有数量都不超过输入限制
    for i in range(n):
        combo[i] = min(combo[i], current_quantities[i])
    
    # 计算最终结果
    total = sum(prices[i] * combo[i] for i in range(n))
    difference = abs(total - target)
    
    print(f"\n最终结果 - 总金额: {total:.2f}, 目标: {target:.2f}, 差异: {difference:.2f}")
    
    return combo, total, difference

def test_greedy_approach():
    """测试贪心算法方法"""
    
    print("=== 测试贪心算法 + 最小服务微调方案 ===\n")
    
    # 使用实际的服务数据
    services_data = [
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
    
    prices = [service["price"] for service in services_data]
    service_names = [service["name"] for service in services_data]
    
    print("可用服务列表:")
    for i, (name, price) in enumerate(zip(service_names, prices)):
        if price > 0:
            print(f"  {i:2d}. {name:>8s}: {price:6.2f}")
    
    print(f"\n总服务数: {len([p for p in prices if p > 0])}")
    print(f"最小价格: {min([p for p in prices if p > 0]):.2f}")
    print(f"最大价格: {max(prices):.2f}")
    
    # 测试用例1: 目标金额500
    print("\n" + "="*50)
    print("测试用例1: 目标金额 500.00")
    print("="*50)
    
    target_amount = 500.00
    # 设置所有服务的库存为足够大
    current_quantities = [1000 if price > 0 else 0 for price in prices]
    
    combination, total, difference = find_best_combination(
        prices, current_quantities, target_amount
    )
    
    print(f"\n结果分析:")
    print(f"目标金额: {target_amount:.2f}")
    print(f"计算金额: {total:.2f}")
    print(f"差异: {difference:.2f} ({difference/target_amount*100:.4f}%)")
    
    print(f"\n详细组合:")
    used_services = []
    for i, qty in enumerate(combination):
        if qty > 0 and prices[i] > 0:
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
    combination2, total2, difference2 = find_best_combination(
        prices, current_quantities, target_amount2
    )
    
    print(f"\n结果分析:")
    print(f"目标金额: {target_amount2:.2f}")
    print(f"计算金额: {total2:.2f}")
    print(f"差异: {difference2:.2f} ({difference2/target_amount2*100:.4f}%)")
    
    print(f"\n详细组合:")
    used_services2 = []
    for i, qty in enumerate(combination2):
        if qty > 0 and prices[i] > 0:
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
    limited_quantities = []
    for i, price in enumerate(prices):
        if price > 0:
            if i < 5:
                limited_quantities.append(min(i+1, 5))  # 前几个服务限制库存
            else:
                limited_quantities.append(10)
        else:
            limited_quantities.append(0)
    
    print("设置有限库存:")
    count = 0
    for i, (name, price) in enumerate(zip(service_names, prices)):
        if price > 0 and count < 5:
            print(f"  {name:>8s}: {limited_quantities[i]} 个")
            count += 1
    
    target_amount3 = 200.00
    combination3, total3, difference3 = find_best_combination(
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

def demonstrate_simple_example():
    """演示简化示例"""
    print("\n" + "="*60)
    print("简化示例演示")
    print("="*60)
    
    # 简化的示例
    prices = [100, 50, 20, 10, 5, 1]  # 从大到小排列的价格
    quantities = [10, 10, 10, 10, 10, 10]  # 每个服务都有10个库存
    target = 173  # 目标金额
    
    print(f"示例配置:")
    print(f"服务价格: {prices}")
    print(f"服务库存: {quantities}")
    print(f"目标金额: {target}")
    
    combination, total, difference = find_best_combination(prices, quantities, target)
    
    print(f"\n最终组合: {combination}")
    print(f"总金额: {total}")
    print(f"差异: {difference}")

if __name__ == "__main__":
    test_greedy_approach()
    demonstrate_simple_example()
    print("\n测试完成!")