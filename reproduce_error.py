#!/usr/bin/env python3
"""
重现图片中的错误场景
"""

def find_best_combination(prices, current_quantities, target):
    """
    当前算法实现
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

# 图片中的数据
prices = [
    27.85, 14.91, 6.80, 6.80, 17.00, 6.80, 6.80, 12.20, 23.50,
    3.92, 9.81, 9.81, 35.31, 23.54, 3.98, 6.93, 104.61, 88.26,
    0.00, 0.00, 0.00, 41.39, 30.53, 30.53, 19.68, 49.69, 35.31,
    50.21, 23.73, 39.36, 6.80, 6.80, 11.51, 5.23, 0.68, 0.68
]

# 根据图片推断的输入量
current_quantities = [
    35,  # L01
    1,   # L04 (假设L04对应索引3)
    55,  # L11
    2,   # L14
    608  # L32+L33 (索引35)
]

# 但需要完整的36个服务的输入量
full_quantities = [0] * len(prices)
full_quantities[0] = 35   # L01
full_quantities[3] = 1    # L04
full_quantities[10] = 55  # L11
full_quantities[13] = 2   # L14  
full_quantities[35] = 608 # L32+L33

target = 1500.98

print("=== 重现图片中的场景 ===")
print(f"目标金额: {target}")
print(f"服务数量: {len(prices)}")

combo, total, difference = find_best_combination(prices, full_quantities, target)

print(f"计算金额: {total:.2f}")
print(f"差异: {difference:.2f}")

# 计算原始总金额
original_total = sum(prices[i] * full_quantities[i] for i in range(len(prices)))
print(f"原始总金额: {original_total:.2f}")

# 显示使用的服务
used_services = []
for i, qty in enumerate(combo):
    if qty > 0:
        used_services.append((i, qty, prices[i], qty * prices[i]))

print(f"\n使用的服务:")
for idx, qty, price, subtotal in used_services:
    print(f"  服务{idx}: {qty} × {price} = {subtotal:.2f}")

print(f"\n总计: {sum(subtotal for _, _, _, subtotal in used_services):.2f}")