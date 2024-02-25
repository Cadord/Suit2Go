from django.conf import settings
import stripe
stripe.api_key = settings.STRIPE_API_KEY

def create_stripe_payment(value):
  session = stripe.checkout.Session.create(
    ui_mode = 'embedded',
    line_items=[
      {
        'price_data': {
          'currency': 'brl',
          'product_data': {
              'name': 'Aluguel de roupas',
          },
          'unit_amount': int(value*100),
        },
        'quantity': 1,
      }
    ],
    mode='payment',
    return_url=settings.BASE_URL + '/checkout_end?session_id={CHECKOUT_SESSION_ID}'
  )
  return session

def get_session_status(sessionId):
  session = stripe.checkout.Session.retrieve(sessionId)
  return { 'status': session.status, 'customer_email': session.customer_details.email }