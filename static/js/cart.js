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
  saveCart(cart);
  updateCartCount()
}

/**
 * @param {number} productId
 */
function removeFromCart(productId) {
  const cart = getCart();
  cart.items = cart.items.filter(p => p.productId !== productId);
  saveCart(cart);
  updateCartCount()
}

/**
 * @param {string} productId
 * @param {number} quantity
 */
function updateCartProductQuantity(productId, quantity) {
  const cart = getCart();
  const product = cart.items.find(p => p.productId === productId)
  if (product) {
    product.quantity += quantity;
    if (product.quantity <= 0) {
      removeFromCart(productId);
    }
    saveCart(cart);
    updateCartCount();
    return product.quantity;
  }
  return 0;
}

/**
 * @returns {Cart}
 */
function getCart() {
  try {
    const cart = JSON.parse(getCookie(CART_KEY))||{items:[]};
    return cart;
  } catch {
    return { items: [] };
  }
}

/**
 * @param {Cart} cart
 */
function saveCart(cart) {
  setCookie(CART_KEY, JSON.stringify(cart), 7);
}

function updateCartCount() {
  var cart = getCart();
  var qtd = cart.items.reduce(function (prev, current) {
    return prev + current.quantity
  }, 0);
  document.getElementById("header-cart-qtd").innerHTML = qtd
}

updateCartCount();
/**
 * @typedef Cart
 * @prop {CartItem[]} items
 */

/**
 * @typedef CartItem
 * @prop {{ number }} productId
 * @prop {{ string }} name
 * @prop {{ number }} quantity
 */


var produtos = ["123", "456"]

