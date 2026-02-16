#!/usr/bin/env python3
"""
Test the improved algorithm for the service calculator.
"""

import sys
sys.path.append('/home/wp/PycharmProjects/PythonProject')

from service_calculator import ServiceCalculator

def test_improved_algorithm():
    """Test the improved find_best_combination algorithm"""
    
    # Create a mock calculator instance (we'll extract the logic)
    calc = ServiceCalculator(None)
    
    # Use the actual service prices from the configuration
    prices = [service["price"] for service in calc.services]
    current_quantities = [0] * len(prices)
    
    # Test case from the user's image:
    # Target amount: 1500.98
    target_amount = 1500.98
    
    print("=== Testing Improved Algorithm ===")
    print(f"Target amount: {target_amount}")
    print(f"Number of services: {len(prices)}")
    print(f"Minimum price: {min(prices):.2f}")
    print(f"Maximum price: {max(prices):.2f}")
    
    # Find best combination using the improved algorithm
    best_combination, best_total, difference = calc.find_best_combination(
        prices, current_quantities, target_amount
    )
    
    print(f"\nResults:")
    print(f"Best total: {best_total:.2f}")
    print(f"Difference: {difference:.2f} ({difference/target_amount*100:.4f}%)")
    
    # Print the combination details
    print(f"\nService combination details:")
    for i, (service, qty) in enumerate(zip(calc.services, best_combination)):
        if qty > 0:
            subtotal = service["price"] * qty
            print(f"  {service['name']}: {qty} × {service['price']:.2f} = {subtotal:.2f}")
    
    # Check specifically for L32+L33 (index 35)
    l32_l33_index = 35
    l32_l33_qty = best_combination[l32_l33_index]
    l32_l33_price = calc.services[l32_l33_index]["price"]
    l32_l33_total = l32_l33_qty * l32_l33_price
    
    print(f"\nL32+L33 details:")
    print(f"  Index: {l32_l33_index}, Price: {l32_l33_price:.2f}, Quantity: {l32_l33_qty}")
    print(f"  Total: {l32_l33_total:.2f}")
    
    # Calculate theoretical optimal for L32+L33 alone
    optimal_qty_l32_l33 = int(round(target_amount / l32_l33_price))
    optimal_total_l32_l33 = optimal_qty_l32_l33 * l32_l33_price
    optimal_diff_l32_l33 = abs(optimal_total_l32_l33 - target_amount)
    
    print(f"\nTheoretical optimal for L32+L33 alone:")
    print(f"  Optimal quantity: {optimal_qty_l32_l33}")
    print(f"  Optimal total: {optimal_total_l32_l33:.2f}")
    print(f"  Optimal difference: {optimal_diff_l32_l33:.2f}")
    
    # Compare with original algorithm's limitation
    print(f"\nOriginal algorithm limitation:")
    print(f"  max_additional was limited to: min(100, int({target_amount}/{l32_l33_price}) + 10) = min(100, {int(target_amount/l32_l33_price)+10}) = 100")
    print(f"  So original could only try up to {current_quantities[l32_l33_index] + 100} = {100} units of L32+L33")
    print(f"  But optimal needs {optimal_qty_l32_l33} units")

if __name__ == "__main__":
    test_improved_algorithm()