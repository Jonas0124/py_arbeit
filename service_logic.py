#!/usr/bin/env python3
"""
Vereinfachte Testversion ohne GUI-Abhängigkeiten
"""

import json
import os
from typing import List, Tuple

class ServiceCalculatorLogic:
    """Geschäftslogik des Service-Rechners ohne GUI"""
    
    def __init__(self):
        self.config_file = ".service_config.json"
        self.services = [
            {"name": "Service A", "price": 10},
            {"name": "Service B", "price": 15},
            {"name": "Service C", "price": 20},
            {"name": "Service D", "price": 25},
            {"name": "Service E", "price": 30}
        ]
        self.load_config()
    
    def load_config(self):
        """Lade gespeicherte Service-Preise"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    saved_prices = json.load(f)
                    for i, service in enumerate(self.services):
                        if str(i) in saved_prices:
                            self.services[i]["price"] = saved_prices[str(i)]
            except Exception as e:
                print(f"Fehler beim Laden: {e}")
    
    def save_config(self):
        """Speichere aktuelle Service-Preise"""
        try:
            prices_to_save = {str(i): service["price"] for i, service in enumerate(self.services)}
            with open(self.config_file, 'w') as f:
                json.dump(prices_to_save, f)
        except Exception as e:
            print(f"Fehler beim Speichern: {e}")
    
    def validate_price(self, price_str: str) -> int:
        """Validiere und konvertiere Preis-Eingabe"""
        try:
            price = int(price_str)
            if price > 0:
                return price
            else:
                raise ValueError("Preis muss größer als 0 sein")
        except ValueError:
            raise ValueError("Ungültiger Preis")
    
    def validate_quantity(self, qty_str: str) -> int:
        """Validiere und konvertiere Mengen-Eingabe"""
        qty_str = qty_str.strip().lower()
        if qty_str == "" or qty_str == "null":
            return 0
        try:
            qty = int(qty_str)
            return max(0, qty)
        except ValueError:
            return 0
    
    def find_best_combination(self, prices: List[int], current_quantities: List[int], target: float) -> Tuple[List[int], float, float]:
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
                print(f"步骤1 - 使用 {actual_qty} 个 {self.services[idx]['name']} (单价{price}), 剩余目标: {remaining_target:.2f}")
        
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
                print(f"步骤2 - 使用 {actual_min_qty} 个 {self.services[min_idx]['name']} (单价{min_price}), 剩余目标: {remaining_target:.2f}")
        
        # 第三步：确保结果在输入约束内
        # 验证所有数量都不超过输入限制
        for i in range(n):
            combo[i] = min(combo[i], current_quantities[i])
        
        # 计算最终结果
        total = sum(prices[i] * combo[i] for i in range(n))
        difference = abs(total - target)
        
        print(f"\n最终结果 - 总金额: {total:.2f}, 目标: {target:.2f}, 差异: {difference:.2f}")
        
        return combo, total, difference

def demo_calculation():
    """Demo der Berechnungsfunktion"""
    calc = ServiceCalculatorLogic()
    
    print("=== Service-Rechner Demo ===")
    print("\nVerfügbare Services:")
    for i, service in enumerate(calc.services):
        print(f"{service['name']}: {service['price']}€")
    
    # Beispiel-Berechnung
    prices = [service["price"] for service in calc.services]
    current_quantities = [0, 0, 0, 0, 0]  # Alle auf 0
    target_amount = 65.0
    
    print(f"\nSuche optimale Kombination für {target_amount}€")
    
    combination, total, difference = calc.find_best_combination(
        prices, current_quantities, target_amount
    )
    
    print(f"\nErgebnis:")
    print(f"Berechneter Betrag: {total}€")
    print(f"Differenz: {difference}€")
    print("\nKombination:")
    for i, (service, qty) in enumerate(zip(calc.services, combination)):
        if qty > 0:
            subtotal = service["price"] * qty
            print(f"  {service['name']}: {qty} × {service['price']}€ = {subtotal}€")

if __name__ == "__main__":
    demo_calculation()