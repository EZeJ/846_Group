"""
Order Processing Service - Problem B
Complex method that needs decomposition for proper testing
Contains intentional bugs that will be revealed through decomposition
"""

from datetime import datetime, date
from typing import Dict, List, Optional
from enum import Enum
import json

class PaymentStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class OrderStatus(Enum):
    DRAFT = "draft"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class Order:
    def __init__(self, order_id: str, customer_id: str, items: List[Dict], 
                 payment_method: str, shipping_address: Dict):
        self.order_id = order_id
        self.customer_id = customer_id
        self.items = items  # [{"product_id": str, "quantity": int, "price": float}]
        self.payment_method = payment_method
        self.shipping_address = shipping_address
        self.status = OrderStatus.DRAFT
        self.payment_status = PaymentStatus.PENDING
        self.total_amount = 0.0
        self.discount_amount = 0.0
        self.tax_amount = 0.0
        self.created_at = datetime.now()

class OrderProcessor:
    def __init__(self):
        self.tax_rate = 0.08  # 8% tax
        self.shipping_cost = 9.99
        
    def process_order(self, order: Order, discount_code: Optional[str] = None) -> Dict:
        """
        Complex method that processes an order through multiple steps.
        This method does TOO MANY things and needs decomposition for proper testing!
        
        Steps:
        1. Validate order data
        2. Calculate item totals
        3. Apply discounts
        4. Calculate taxes
        5. Process payment
        6. Update inventory
        7. Generate confirmation
        8. Send notifications
        
        Args:
            order (Order): Order to process
            discount_code (str, optional): Discount code to apply
            
        Returns:
            Dict: Processing result with status and details
            
        Intentional Bugs: Multiple bugs hidden in the complex logic
        """
        try:
            # Step 1: Validate order
            if not order.order_id:
                raise ValueError("Order ID required")
            # Bug 1: Doesn't validate customer_id, items, payment_method
            
            # Step 2: Calculate totals )
            subtotal = 0
            for item in order.items:
                # Bug 2: Doesn't check for negative quantities or prices
                item_total = item['quantity'] * item['price']
                subtotal += item_total
            
            # Step 3: Apply discounts
            discount_amount = 0
            if discount_code:
                if discount_code == "SAVE10":
                    discount_amount = subtotal * 0.10
                elif discount_code == "SAVE20":
                    discount_amount = subtotal * 0.20
                elif discount_code == "FREEBIE":
                    # Bug 3: Could make total negative
                    discount_amount = subtotal
                # Bug 4: Invalid discount codes not handled
            
            # Step 4: Calculate tax 
            # Bug 5: Tax calculated on full amount instead of after discount
            tax_amount = subtotal * self.tax_rate
            
            # Step 5: Final total 
            total_after_discount = subtotal - discount_amount
            final_total = total_after_discount + tax_amount
            
            # Bug 6: Free shipping not applied correctly for orders over $100
            if total_after_discount > 100:
                shipping_cost = self.shipping_cost  # Should be 0
            else:
                shipping_cost = self.shipping_cost
            
            final_total += shipping_cost
            
            # Step 6: Payment processing
            # Bug 7: Assumes payment always succeeds
            payment_result = self._process_payment(order, final_total)
            
            # Step 7: Update order
            order.total_amount = final_total
            order.discount_amount = discount_amount
            order.tax_amount = tax_amount
            order.status = OrderStatus.PROCESSING
            order.payment_status = PaymentStatus.COMPLETED
            
            # Step 8: Generate result
            return {
                "success": True,
                "order_id": order.order_id,
                "total": final_total,
                "message": "Order processed successfully"
            }
            
        except Exception as e:
            # Bug 8: Generic error handling loses important details
            return {
                "success": False,
                "error": "Processing failed"
            }
    
    def _process_payment(self, order: Order, amount: float) -> Dict:
        """Simulate payment processing"""
        # Bug 9: No amount validation
        if order.payment_method == "credit_card":
            return {"status": "success", "transaction_id": "tx_123"}
        elif order.payment_method == "paypal":
            return {"status": "success", "transaction_id": "pp_456"}
        else:
            # Bug 10: Unknown payment methods not handled properly
            return {"status": "success", "transaction_id": "unknown"}