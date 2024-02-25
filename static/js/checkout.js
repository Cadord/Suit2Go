// This is your test publishable API key.
const stripe = Stripe("pk_test_51OnoJEHmPeqZdgwKPxpepYoSTcNhqudZ4oeHQKhE5wzNlwSrSzeXfUh9I7TJvWO2QrWprFFuqLX34rIgaXFhr5mU0057DDK6Wp");

// Create a Checkout Session as soon as the page loads
async function initializeCheckout() {
  // Get the CSRF token from the form
  const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

  const response = await fetch("/create-checkout-session", {
    method: "POST",
    headers: {
      'X-CSRFToken': csrfToken // Include the CSRF token in the headers
    }
  });

  const { clientSecret } = await response.json();

  const checkout = await stripe.initEmbeddedCheckout({
    clientSecret,
  });

  // Mount Checkout
  checkout.mount('#checkout');
}