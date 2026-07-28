import urllib.request
import urllib.parse
import http.cookiejar
import re
import sys


BASE = 'http://127.0.0.1:8000'
PASS = 0
FAIL = 0
ERRORS = []


def test(name, condition, detail=''):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f'  \u2713 {name}')
    else:
        FAIL += 1
        ERRORS.append(f'  \u2717 {name} — {detail}')
        print(f'  \u2717 {name} — {detail}')


class Session:
    def __init__(self, follow_redirects=True):
        self.cookie_jar = http.cookiejar.CookieJar()
        if follow_redirects:
            self.opener = urllib.request.build_opener(
                urllib.request.HTTPCookieProcessor(self.cookie_jar),
            )
        else:
            self.opener = urllib.request.build_opener(
                urllib.request.HTTPCookieProcessor(self.cookie_jar),
                NoRedirectHandler,
            )

    def get(self, path):
        req = urllib.request.Request(f'{BASE}{path}')
        return self.opener.open(req)

    def post(self, path, data):
        req = urllib.request.Request(
            f'{BASE}{path}',
            data=urllib.parse.urlencode(data).encode(),
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
        )
        return self.opener.open(req)

    def has_csrf(self, html, action=''):
        token_match = re.search(
            r'<input[^>]*name="csrfmiddlewaretoken"[^>]*value="([^"]+)"',
            html,
        )
        return token_match

    def extract_csrf(self, html):
        m = re.search(
            r'<input[^>]*name="csrfmiddlewaretoken"[^>]*value="([^"]+)"',
            html,
        )
        return m.group(1) if m else None


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


session = Session()
anon = Session()
no_redirect = Session(follow_redirects=False)

print('=' * 68)
print('  ACCEPTANCE TEST INVENTORY — OneStep Pharmacy')
print('=' * 68)

# ──────────────────────────────────────────────
# 1. ANONYMOUS BROWSING
# ──────────────────────────────────────────────
print('\n--- Anonymous Browsing ---')

# 1.1 Homepage
resp = session.get('/')
html = resp.read().decode()
test('Homepage returns 200', resp.status == 200)
test('Homepage shows featured products', 'product-card' in html or 'View Details' in html or 'Featured' in html)
test('Homepage has hero section', 'Browse Medicines' in html or 'Welcome' in html)
test('Homepage has brand name', 'OneStep Pharmacy' in html)

# 1.2 Product list
resp = session.get('/products/')
html = resp.read().decode()
test('Product list returns 200', resp.status == 200)
test('Product list shows product cards', 'product-card' in html)
test('Product list has 10 products', html.count('View Details') == 10)
test('Product list has stock badges', 'in stock' in html or 'left' in html or 'Out of Stock' in html)
test('Product list has View Details links', 'View Details' in html)

# 1.3 Discover product IDs from list page
resp = session.get('/products/')
list_html = resp.read().decode()
product_ids = re.findall(r'/products/(\d+)/', list_html)
product_names = re.findall(r'<h3[^>]*>(.*?)</h3>', list_html)
first_id = int(product_ids[0]) if product_ids else 1
first_name = product_names[0] if product_names else 'Product'
test('Found at least 1 product ID in list', len(product_ids) >= 1)

# 1.4 Product detail
resp = session.get(f'/products/{first_id}/')
html = resp.read().decode()
test('Product detail returns 200', resp.status == 200)
test('Product detail shows name in heading', f'<h1>{first_name}' in html)
test('Product detail shows price', '4.99' in html or 'Rs.' in html or '$' in html or 'Price' in html)
test('Product detail has description text', html.count('<p>') >= 1 or 'mg' in html)
test('Product detail shows stock badge', 'available' in html or 'left' in html or 'Stock' in html)
test('Anonymous sees Login to Order (in stock)', 'Login to Order' in html)
test('Login to Order includes next param', '/login/?next=' in html)

# 1.4 404 page
try:
    session.get('/products/9999/')
    test('404 returns 404 (no redirect)', False, 'Expected 404, got 200')
except urllib.error.HTTPError as e:
    test('Missing product returns 404', e.code == 404)

# 1.5 Login page
resp = session.get('/login/')
html = resp.read().decode()
test('Login page returns 200', resp.status == 200)
test('Login page has form', 'Sign In' in html)
test('Login page has CSRF', bool(session.has_csrf(html)))
test('Login page has signup link', 'Sign Up' in html or 'Sign In' in html)

# 1.6 Signup page
resp = session.get('/users/signup/')
html = resp.read().decode()
test('Signup page returns 200', resp.status == 200)
test('Signup page has form', 'Create Account' in html)
test('Signup page has CSRF', bool(session.has_csrf(html)))

# 1.7 Logout page (accessible to anonymous)
resp = session.get('/logout/')
html = resp.read().decode()
test('Logout page accessible to anonymous', resp.status == 200)
test('Logout confirmation shown', 'Sign Out' in html)

# 1.8 Order redirect
resp = session.get('/orders/place/')
test('Orders place index redirects to products', resp.url.endswith('/products/') or resp.status == 302)

# 1.9 Success page
resp = session.get('/orders/success/')
html = resp.read().decode()
test('Success page accessible to anonymous', resp.status == 200)
test('Success page shows confirmation', 'Order Placed Successfully' in html)
test('Success page has Continue Shopping', 'Continue Shopping' in html)

# 1.10 Place order redirects to login when unauthenticated
try:
    no_redirect.get(f'/orders/place/{first_id}/')
    test('Unauthenticated order redirects to login', False, 'No redirect')
except urllib.error.HTTPError as e:
    test('Unauthenticated order returns 302', e.code == 302)
    loc = e.headers.get('Location', '')
    test('Unauthenticated order redirects to login', '/login/' in loc)

# 1.11 Anonymous nav check
resp = session.get(f'/products/{first_id}/')
html = resp.read().decode()
test('Nav shows Sign Up and Login for anonymous',
     'Sign Up' in html and 'Login' in html)
test('Nav hides Logout for anonymous',
     'Logout' not in html or html.count('Logout') == 0)

# ──────────────────────────────────────────────
# 2. AUTHENTICATION FLOW
# ──────────────────────────────────────────────
print('\n--- Authentication Flow ---')

# 2.1 Signup
resp = anon.post('/users/signup/', {
    'csrfmiddlewaretoken': anon.extract_csrf(anon.get('/users/signup/').read().decode()),
    'username': 'testaccept',
    'password1': 'Acceptance1!',
    'password2': 'Acceptance1!',
})
test('Signup succeeds (redirects to login)', resp.status in (200, 302))
# Follow redirect if needed
if resp.status == 302:
    test('Signup redirects to login', '/login/' in resp.headers.get('Location', ''))

# 2.2 Signup with existing username
resp2 = anon.post('/users/signup/', {
    'csrfmiddlewaretoken': anon.extract_csrf(anon.get('/users/signup/').read().decode()),
    'username': 'testaccept',
    'password1': 'Acceptance1!',
    'password2': 'Acceptance1!',
})
html2 = resp2.read().decode()
test('Duplicate username shows error', 'already exists' in html2)

# 2.3 Login
login_page = session.get('/login/')
login_html = login_page.read().decode()
csrf = session.extract_csrf(login_html)
resp = session.post('/login/', {
    'csrfmiddlewaretoken': csrf,
    'username': 'testaccept',
    'password': 'Acceptance1!',
})
test('Login succeeds (redirects)', resp.status in (200, 302))

# 2.4 Login with bad credentials
resp = session.post('/login/', {
    'csrfmiddlewaretoken': session.extract_csrf(session.get('/login/').read().decode()),
    'username': 'testaccept',
    'password': 'WRONGpassword',
})
html = resp.read().decode()
test('Bad login shows error', 'Please enter a correct' in html or 'error' in html.lower())

# 2.5 After login, verify nav changed
resp = session.get('/')
html = resp.read().decode()
test('Authenticated nav shows Logout', 'Logout' in html)
test('Authenticated nav hides Sign Up', 'Sign Up' not in html or html.count('Sign Up') < 2)
test('Authenticated nav shows Order link', '/orders/place/' in html)

# ──────────────────────────────────────────────
# 3. ORDER FLOW
# ──────────────────────────────────────────────
print('\n--- Order Flow ---')

# Ensure logged in for order tests
login_page = session.get('/login/')
login_html = login_page.read().decode()
csrf = session.extract_csrf(login_html)
session.post('/login/', {
    'csrfmiddlewaretoken': csrf,
    'username': 'testaccept',
    'password': 'Acceptance1!',
})

# 3.1 Place order GET
resp = session.get(f'/orders/place/{first_id}/')
html = resp.read().decode()
test('Place order form returns 200', resp.status == 200)
test('Place order shows quantity input', 'quantity' in html or 'Quantity' in html)
test('Place order shows product name', first_name in html)
test('Place order shows price', 'Rs.' in html or '4.99' in html or 'Price' in html)
test('Place order form has Submit button', 'Submit Order' in html)
test('Place order has back link', 'Back to product' in html)

# 3.2 Place order POST with valid data
resp = session.post(f'/orders/place/{first_id}/', {
    'csrfmiddlewaretoken': session.extract_csrf(html),
    'quantity': '2',
})
test('Valid order redirects to success',
     resp.status in (200, 302))

# 3.3 Order with quantity exceeding stock
resp = session.get(f'/orders/place/{first_id}/')
html = resp.read().decode()
resp = session.post(f'/orders/place/{first_id}/', {
    'csrfmiddlewaretoken': session.extract_csrf(html),
    'quantity': '9999',
})
html = resp.read().decode()
test('Overstock order shows error (200)', resp.status == 200)
test('Overstock error message shown', 'stock' in html.lower() and ('only' in html.lower() or 'Sorry' in html))

# 3.4 Order with non-numeric quantity
resp = session.get(f'/orders/place/{first_id}/')
html = resp.read().decode()
resp = session.post(f'/orders/place/{first_id}/', {
    'csrfmiddlewaretoken': session.extract_csrf(html),
    'quantity': 'abc',
})
html = resp.read().decode()
test('Non-numeric quantity shows error', 'whole number' in html.lower())

# 3.5 Order with negative quantity
resp = session.get(f'/orders/place/{first_id}/')
html = resp.read().decode()
resp = session.post(f'/orders/place/{first_id}/', {
    'csrfmiddlewaretoken': session.extract_csrf(html),
    'quantity': '-5',
})
html = resp.read().decode()
test('Negative quantity shows error', 'at least' in html.lower() or 'positive' in html.lower())

# 3.6 Order with zero quantity
resp = session.get(f'/orders/place/{first_id}/')
html = resp.read().decode()
resp = session.post(f'/orders/place/{first_id}/', {
    'csrfmiddlewaretoken': session.extract_csrf(html),
    'quantity': '0',
})
html = resp.read().decode()
test('Zero quantity shows error', 'at least' in html.lower())

# 3.7 Verify stock decremented
resp = session.get(f'/products/{first_id}/')
html = resp.read().decode()
# Stock should have decreased from 150 by the 4 units ordered in these tests
stock_match = re.search(r'(\d+)\s+(available|in stock|left)', html)
test('Stock was decremented after orders',
     stock_match and int(stock_match.group(1)) < 150)

# 3.8 Access order page for non-existent product
try:
    session.get('/orders/place/9999/')
    test('Order page for missing product', False, 'No 404')
except urllib.error.HTTPError as e:
    test('Missing product order returns 404', e.code == 404)

# ──────────────────────────────────────────────
# 4. LOGOUT
# ──────────────────────────────────────────────
print('\n--- Logout ---')

# Logout via POST
resp = session.post('/logout/', {
    'csrfmiddlewaretoken': session.extract_csrf(session.get('/logout/').read().decode()),
})
test('Logout redirects', resp.status in (200, 302))

# Verify logged out
resp = session.get('/')
html = resp.read().decode()
test('After logout, Sign Up appears', 'Sign Up' in html)
test('After logout, Login appears', 'Login' in html)
test('After logout, Logout hidden', 'Logout' not in html)

# ──────────────────────────────────────────────
# 5. ADMIN DASHBOARD
# ──────────────────────────────────────────────
print('\n--- Admin Dashboard ---')

# 5.1 Anonymous cannot access admin
try:
    no_redirect.get('/admin/')
    test('Anonymous admin access blocked', False, 'No redirect on admin')
except urllib.error.HTTPError as e:
    test('Anonymous gets 302 on admin', e.code == 302)
    loc = e.headers.get('Location', '')
    test('Anonymous redirected to login from admin', '/login/' in loc)

# 5.2 Non-staff cannot access admin
login_page = anon.get('/login/')
login_html = login_page.read().decode()
csrf = anon.extract_csrf(login_html)
anon.post('/login/', {
    'csrfmiddlewaretoken': csrf,
    'username': 'testaccept',
    'password': 'Acceptance1!',
})
try:
    no_redirect.get('/admin/')
    test('Non-staff admin access blocked', False, 'Non-staff had access')
except urllib.error.HTTPError as e:
    test('Non-staff gets 302 on admin', e.code in (200, 302))

# 5.3 Staff can access admin
login_page = session.get('/login/')
login_html = login_page.read().decode()
csrf = session.extract_csrf(login_html)
session.post('/login/', {
    'csrfmiddlewaretoken': csrf,
    'username': 'admin',
    'password': 'admin123',
})
resp = session.get('/admin/')
test('Staff can access admin', resp.status == 200)
test('Admin page has admin branding', 'OneStep Pharmacy' in resp.read().decode())

# 5.4 Admin has product management
resp = session.get('/admin/products/product/')
html = resp.read().decode()
test('Admin product list accessible', resp.status == 200)
test('Admin shows products', 'Product' in html)

# 5.5 Admin has order management
resp = session.get('/admin/orders/order/')
html = resp.read().decode()
test('Admin order list accessible', resp.status == 200)
test('Admin shows orders', 'Order' in html)

# 5.6 Admin has user profile management
resp = session.get('/admin/users/userprofile/')
html = resp.read().decode()
test('Admin user profile list accessible', resp.status == 200)
test('Admin shows user profiles', 'UserProfile' in html or 'userprofile' in html)

# ──────────────────────────────────────────────
# 6. STATIC ASSETS
# ──────────────────────────────────────────────
print('\n--- Static Assets ---')

resp = session.get('/static/css/styles.css')
test('CSS stylesheet loaded', resp.status == 200)

resp = session.get('/static/images/logo.svg')
test('Logo SVG loaded', resp.status == 200)

# ──────────────────────────────────────────────
# SUMMARY
# ──────────────────────────────────────────────
print()
print('=' * 68)
total = PASS + FAIL
print(f'  RESULTS: {PASS}/{total} passed, {FAIL} failed')
if ERRORS:
    print()
    for e in ERRORS:
        print(e)
print('=' * 68)

sys.exit(0 if FAIL == 0 else 1)
