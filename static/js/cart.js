const CART_KEY = "suit2goCart"

/**
 * @param {number} productId
 * @param {string} productName
 * @param {number} quantity
 */
function addToCart(productId, productName, quantity) {
  const cart = getCart();
  const existingItem = cart.items.find(p => p.productId === productId)
  if (existingItem) {
    existingItem.quantity += quantity;
  }
  else {
    cart.items.push({ productId: productId, name: productName, quantity: quantity });
  }
  localStorage.setItem(CART_KEY, JSON.stringify(cart));
  updateCartCount()
}

/**
 * @param {number} productId
 */
function removeFromCart(productId) {
  const cart = getCart();
  cart.items = cart.items.filter(p => p.productId !== productId);
  localStorage.setItem(CART_KEY, JSON.stringify(cart));
  updateCartCount()
}

/**
 * @returns {Cart}
 */
function getCart() {
  try {
    const cart = JSON.parse(localStorage.getItem(CART_KEY));
    return cart || { items: [] }
  } catch {
    return { items: [] };
  }
}

function updateCartCount() {
  var cart = getCart();
  var qtd = cart.items.reduce(function (prev, current) {
    return prev + current.quantity
  }, 0);
  document.getElementById("header-cart-qtd").innerHTML = qtd
}

updateCartCount()
/**
 * @typedef Cart
 * @prop {CartItem[]} items
 */

/**
 * @typedef CartItem
 * @prop {{ number }} productId
 * @prop {{ string }} name
 */


var produtos = ["123", "456"]