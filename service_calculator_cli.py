#!/usr/bin/env python3
"""
服务计算器 - 命令行版本（无需 tkinter）
"""

from service_logic import ServiceCalculatorLogic
import sys

def main():
    print("=" * 60)
    print("🎯 服务计算器 - 命令行版本")
    print("=" * 60)
    
    calc = ServiceCalculatorLogic()
    
    # 显示所有服务
    print("\n📋 可用服务:")
    print("-" * 40)
    for i, service in enumerate(calc.services):
        print(f"{i+1:2d}. {service['name']:10} | {service['price']:8.2f}€")
    
    while True:
        print("\n" + "=" * 60)
        print("请输入目标金额 (输入 'quit' 退出):")
        try:
            target_input = input(">>> ").strip()
            
            if target_input.lower() == 'quit':
                print("👋 感谢使用！再见！")
                break
                
            target_amount = float(target_input)
            
            if target_amount <= 0:
                print("❌ 错误：目标金额必须大于 0")
                continue
            
            # 计算最优组合
            prices = [s['price'] for s in calc.services]
            current_quantities = [0] * len(prices)
            
            combination, total, difference = calc.find_best_combination(
                prices, current_quantities, target_amount
            )
            
            # 显示结果
            print(f"\n🔍 计算结果:")
            print(f"目标金额: {target_amount:.2f}€")
            print(f"计算金额: {total:.2f}€")
            print(f"差异: {difference:.2f}€ ({difference/target_amount*100:.2f}%)")
            
            print(f"\n✅ 最优组合:")
            print("-" * 30)
            total_services = 0
            for i, (service, qty) in enumerate(zip(calc.services, combination)):
                if qty > 0:
                    subtotal = service['price'] * qty
                    print(f"  {service['name']:10}: {qty} × {service['price']:.2f}€ = {subtotal:.2f}€")
                    total_services += qty
            
            print(f"\n📊 总计: {total_services} 个服务, {total:.2f}€")
            
            if difference == 0:
                print("🎉 完美匹配！")
            elif difference <= target_amount * 0.05:
                print("✅ 非常接近！")
            else:
                print("⚠️ 有一定差距")
                
        except ValueError:
            print("❌ 错误：请输入有效的数字")
        except KeyboardInterrupt:
            print("\n👋 退出程序")
            break
        except Exception as e:
            print(f"❌ 错误: {e}")

if __name__ == "__main__":
    main()