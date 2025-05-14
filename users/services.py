import stripe
from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_product_in_stripe(instance):
    """Создаёт продукт в Stripe API."""
    title_product = (
        f"{instance.paid_course}" if instance.paid_course else f"{instance.paid_lesson}"
    )
    stripe_product = stripe.Product.create(name=f"{title_product}")
    return stripe_product.get("id")


def create_price_in_stripe(stripe_product_id, amount):
    """Создаёт цену в Stripe API."""
    return stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product = stripe_product_id,
    )


def create_session_in_stripe(price):
    """Создаёт сессию на оплату в Stripe API."""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/users/payments/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")

    # session = stripe.checkout.Session.create(
    #     success_url="https://example.com/success",
    #     line_items=[{"price": "price_1MotwRLkdIwHu7ixYcPLm5uZ", "quantity": 2}],
    #     mode="payment",
    # )
