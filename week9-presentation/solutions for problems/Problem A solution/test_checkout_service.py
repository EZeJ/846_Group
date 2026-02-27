import pytest
from unittest.mock import MagicMock
from checkout_service import (
    CheckoutService, Cart, CartItem, Customer,
    InventoryService, PaymentGateway, CheckoutError, CustomerTier
)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def make_service(in_stock=True, payment_success=True, payment_reason="declined"):
    inventory = MagicMock(spec=InventoryService)
    inventory.check_stock.return_value = in_stock
    payment = MagicMock(spec=PaymentGateway)
    if payment_success:
        payment.charge.return_value = {"success": True}
    else:
        payment.charge.return_value = {"success": False, "reason": payment_reason}
    return CheckoutService(inventory, payment)


def make_cart(*items):
    """items: tuples of (price, qty) or (price, qty, flash_sale)"""
    cart = Cart()
    for i, spec in enumerate(items):
        price, qty = spec[0], spec[1]
        flash = spec[2] if len(spec) > 2 else False
        cart.add_item(CartItem(f"p{i}", f"Item{i}", price, qty, flash_sale=flash))
    return cart


# ─── Bug 1: Empty cart not validated ─────────────────────────────────────────

@pytest.mark.parametrize("cart_obj", [Cart(), None])
def test_empty_cart_raises(cart_obj):
    service = make_service()
    customer = Customer("c1", "Alice")
    with pytest.raises(CheckoutError):
        service.process_checkout(cart_obj, customer)


# ─── Bug 2: Stock check logic inverted ────────────────────────────────────────

def test_in_stock_item_proceeds():
    """When inventory reports in-stock (True), checkout should succeed."""
    service = make_service(in_stock=True)
    cart = make_cart((50.0, 1))
    customer = Customer("c1", "Alice")
    result = service.process_checkout(cart, customer)
    assert result["status"] == "success"


def test_out_of_stock_item_raises():
    """When inventory reports out-of-stock (False), checkout should raise."""
    service = make_service(in_stock=False)
    cart = make_cart((50.0, 1))
    customer = Customer("c1", "Alice")
    with pytest.raises(CheckoutError):
        service.process_checkout(cart, customer)


# ─── Bug 3: Bundle discount threshold off-by-one ──────────────────────────────

@pytest.mark.parametrize("qty,expect_discount", [(2, False), (3, True), (4, True)])
def test_bundle_discount_threshold(qty, expect_discount):
    """Bundle 5% discount must apply at quantity >= 3, not just > 3."""
    service = make_service()
    cart = make_cart((20.0, qty))
    customer = Customer("c1", "Alice")
    result = service.process_checkout(cart, customer)
    subtotal = 20.0 * qty
    if expect_discount:
        assert result["discount"] >= pytest.approx(0.05 * subtotal, abs=0.01)
    else:
        assert result["discount"] == 0


# ─── Bug 4: SUMMER20 cap inverted (max vs min) ────────────────────────────────

@pytest.mark.parametrize("price,min_spend_met", [(74.99, False), (75.0, True)])
def test_summer20_minimum_spend(price, min_spend_met):
    service = make_service()
    cart = make_cart((price, 1))
    customer = Customer("c1", "Alice")
    if not min_spend_met:
        with pytest.raises(CheckoutError):
            service.process_checkout(cart, customer, coupon_code="SUMMER20")
    else:
        result = service.process_checkout(cart, customer, coupon_code="SUMMER20")
        assert result["discount"] == pytest.approx(min(0.20 * price, 30.0), abs=0.01)


def test_summer20_capped_at_30():
    """When 20% of subtotal exceeds $30, the discount must be capped at $30."""
    # 20% of $200 = $40 > $30, so discount should be capped at $30, not $40
    service = make_service()
    cart = make_cart((200.0, 1))
    customer = Customer("c1", "Alice")
    result = service.process_checkout(cart, customer, coupon_code="SUMMER20")
    assert result["discount"] == pytest.approx(30.0, abs=0.01)


# ─── Bug 5: FLASH5 + VIP combination not blocked ──────────────────────────────

def test_flash5_with_vip_raises():
    """VIP customer using FLASH5 should raise CheckoutError."""
    service = make_service()
    cart = make_cart((100.0, 1, True))  # flash_sale=True
    customer = Customer("c1", "Alice", tier=CustomerTier.VIP)
    with pytest.raises(CheckoutError):
        service.process_checkout(cart, customer, coupon_code="FLASH5")


@pytest.mark.parametrize("coupon", ["SAVE10", "SUMMER20"])
def test_coupon_with_vip_raises(coupon):
    service = make_service()
    cart = make_cart((200.0, 1))
    customer = Customer("c1", "Alice", tier=CustomerTier.VIP)
    with pytest.raises(CheckoutError):
        service.process_checkout(cart, customer, coupon_code=coupon)


# ─── Bug 6: Tax calculated on pre-discount subtotal ──────────────────────────

def test_tax_uses_post_discount_amount():
    """Tax must be 13% of (subtotal - discount), not 13% of subtotal."""
    # $200 + SUMMER20 → $30 discount; tax base should be $170, not $200
    service = make_service()
    cart = make_cart((200.0, 1))
    customer = Customer("c1", "Alice")
    result = service.process_checkout(cart, customer, coupon_code="SUMMER20")
    taxable = result["subtotal"] - result["discount"]
    assert result["tax"] == pytest.approx(0.13 * taxable, abs=0.01)


def test_tax_uses_post_loyalty_credit_amount():
    """Tax must use post-loyalty-credit amount as the tax base."""
    service = make_service()
    cart = make_cart((100.0, 1))
    customer = Customer("c1", "Alice", loyalty_points=500)
    result = service.process_checkout(cart, customer, redeem_points=True)
    taxable = result["subtotal"] - result["discount"] - result["points_redeemed"]
    assert result["tax"] == pytest.approx(0.13 * taxable, abs=0.01)


# ─── Bug 7: Shipping threshold uses pre-discount subtotal ────────────────────

def test_shipping_uses_post_discount_subtotal():
    """
    Cart subtotal is $55 (above $50 free-shipping threshold), but after 15%
    VIP discount the discounted total is $46.75 (below $50). Shipping must
    be $10 because the relevant check is on the discounted subtotal.
    """
    service = make_service()
    cart = make_cart((55.0, 1))
    customer = Customer("c1", "Alice", tier=CustomerTier.VIP)
    result = service.process_checkout(cart, customer)
    # discounted_subtotal = 55 - 55*0.15 = 46.75 < 50 → should charge shipping
    assert result["shipping"] == pytest.approx(10.0, abs=0.01)


# ─── Bug 8: Payment failure not handled ──────────────────────────────────────

def test_payment_failure_raises():
    """If payment.charge() returns success=False, CheckoutError must be raised."""
    service = make_service(payment_success=False, payment_reason="card declined")
    cart = make_cart((100.0, 1))
    customer = Customer("c1", "Alice")
    with pytest.raises(CheckoutError):
        service.process_checkout(cart, customer)


# ─── Bug 9: Total not floored at zero ────────────────────────────────────────

def test_total_never_negative():
    """
    VIP discount + max loyalty credit on a small cart can make total go negative.
    Total must always be floored at 0.0.
    """
    # subtotal=60, VIP discount=9 → discounted=51, loyalty_credit=100 → total goes negative
    service = make_service()
    cart = make_cart((60.0, 1))
    customer = Customer("c1", "Alice", tier=CustomerTier.VIP, loyalty_points=1000)
    result = service.process_checkout(cart, customer, redeem_points=True)
    assert result["total"] >= 0


# ─── Happy-path and supporting sanity checks ─────────────────────────────────

def test_basic_checkout_no_discounts():
    service = make_service()
    cart = make_cart((100.0, 1))
    customer = Customer("c1", "Alice")
    result = service.process_checkout(cart, customer)
    assert result["status"] == "success"
    assert result["subtotal"] == pytest.approx(100.0)
    assert result["discount"] == 0
    assert result["tax"] == pytest.approx(13.0)
    assert result["shipping"] == 0       # 100 >= 50, free shipping
    assert result["total"] == pytest.approx(113.0)


def test_shipping_charged_below_threshold():
    service = make_service()
    cart = make_cart((49.99, 1))
    customer = Customer("c1", "Alice")
    result = service.process_checkout(cart, customer)
    assert result["shipping"] == pytest.approx(10.0)


def test_loyalty_points_below_threshold_not_redeemed():
    service = make_service()
    cart = make_cart((100.0, 1))
    customer = Customer("c1", "Alice", loyalty_points=499)
    result = service.process_checkout(cart, customer, redeem_points=True)
    assert result["points_redeemed"] == 0


def test_loyalty_points_at_threshold_redeemed():
    service = make_service()
    cart = make_cart((100.0, 1))
    customer = Customer("c1", "Alice", loyalty_points=500)
    result = service.process_checkout(cart, customer, redeem_points=True)
    assert result["points_redeemed"] > 0


def test_flash5_non_flash_items_no_discount():
    service = make_service()
    cart = make_cart((100.0, 1, False))  # flash_sale=False
    customer = Customer("c1", "Alice")
    result = service.process_checkout(cart, customer, coupon_code="FLASH5")
    assert result["discount"] == 0


def test_save10_minimum_spend():
    service = make_service()
    cart = make_cart((99.99, 1))
    customer = Customer("c1", "Alice")
    with pytest.raises(CheckoutError):
        service.process_checkout(cart, customer, coupon_code="SAVE10")
