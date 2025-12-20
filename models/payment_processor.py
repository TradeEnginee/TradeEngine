# payment/payment_processor.py
from abc import ABC, abstractmethod
from typing import Dict, Any
from dataclasses import dataclass
import uuid

@dataclass
class PaymentResult:
    success: bool
    transaction_id: str
    message: str
    data: Dict[str, Any] = None

class PaymentProcessor(ABC):
    """Abstract base class for payment processing - Strategy Pattern Interface"""
    
    @abstractmethod
    def process_payment(self, amount: float, payment_data: Dict[str, Any]) -> PaymentResult:
        """Process the payment and return result"""
        pass
    
    @abstractmethod
    def validate_payment_data(self, payment_data: Dict[str, Any]) -> tuple[bool, str]:
        """Validate payment-specific data"""
        pass
    
    @abstractmethod
    def get_payment_method_name(self) -> str:
        """Return the name of the payment method"""
        pass
<<<<<<< HEAD

=======
    ##dd
>>>>>>> c40f5b9 (- Modified to use SQLite database with JSON shipping address)
class CreditCardStrategy(PaymentProcessor):
    """Concrete strategy for credit card payments"""
    
    def get_payment_method_name(self) -> str:
        return "credit_card"
    
    def validate_payment_data(self, payment_data: Dict[str, Any]) -> tuple[bool, str]:
        required_fields = ["card_number", "expiry_month", "expiry_year", "cvv", "cardholder_name"]
        
        for field in required_fields:
            if field not in payment_data or not payment_data[field]:
                return False, f"Missing required field: {field}"
        
        # Validate card number
        card_number = str(payment_data["card_number"]).replace(" ", "")
        if not card_number.isdigit() or len(card_number) < 13 or len(card_number) > 19:
            return False, "Invalid card number"
        
        # Validate CVV
        cvv = str(payment_data["cvv"])
        if not cvv.isdigit() or len(cvv) < 3 or len(cvv) > 4:
            return False, "Invalid CVV"
        
        # Validate expiry
        try:
            month = int(payment_data["expiry_month"])
            year = int(payment_data["expiry_year"])
            if month < 1 or month > 12:
                return False, "Invalid expiry month"
            if year < 2024:
                return False, "Card has expired"
        except ValueError:
            return False, "Invalid expiry date"
        
        return True, "Validation successful"
    
    def process_payment(self, amount: float, payment_data: Dict[str, Any]) -> PaymentResult:
        # Validate first
        is_valid, message = self.validate_payment_data(payment_data)
        if not is_valid:
            return PaymentResult(
                success=False,
                transaction_id="",
                message=message
            )
        
        #  payment gateway integration
        
        transaction_id = f"CC-{uuid.uuid4().hex[:12].upper()}"
        
        #  processing (call payment gateway API)
        return PaymentResult(
            success=True,
            transaction_id=transaction_id,
            message="Payment processed successfully",
            data={
                "card_last_four": str(payment_data["card_number"])[-4:],
                "amount_charged": amount
            }
        )



class CashOnDeliveryStrategy(PaymentProcessor):
    """Concrete strategy for Cash on Delivery payments"""
    
    def get_payment_method_name(self) -> str:
        return "cod"
    
    def validate_payment_data(self, payment_data: Dict[str, Any]) -> tuple[bool, str]:
        # COD doesn't require payment data, just confirmation
        return True, "COD validation successful"
    
    def process_payment(self, amount: float, payment_data: Dict[str, Any]) -> PaymentResult:
        transaction_id = f"COD-{uuid.uuid4().hex[:12].upper()}"
        
        return PaymentResult(
            success=True,
            transaction_id=transaction_id,
            message="Cash on Delivery order confirmed. Payment will be collected upon delivery.",
            data={
                "amount_due": amount,
                "payment_collection": "on_delivery"
            }
        )


class PaymentContext:
    """Context class that uses a PaymentProcessor strategy"""
    
    _strategies = {
        "credit_card": CreditCardStrategy,
        
        "cod": CashOnDeliveryStrategy
    }
    
    def __init__(self, strategy: PaymentProcessor = None):
        self._strategy = strategy
    
    def set_strategy(self, payment_method: str):
        """Set strategy based on payment method string"""
        if payment_method not in self._strategies:
            raise ValueError(f"Unknown payment method: {payment_method}")
        self._strategy = self._strategies[payment_method]()
    
    def process_payment(self, amount: float, payment_data: Dict[str, Any]) -> PaymentResult:
        if not self._strategy:
            raise ValueError("Payment strategy not set")
        return self._strategy.process_payment(amount, payment_data)
    
    @classmethod
    def get_available_methods(cls) -> list:
        return list(cls._strategies.keys())
