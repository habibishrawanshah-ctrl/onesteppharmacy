# OneStep Pharmacy — Acceptance Criteria & Edge Cases

## 1. Product Catalog

### 1.1 Product List (`/products/`)

| ID | Acceptance Criteria | Risk / Edge Case |
|---|---|---|
| P1.1 | Page returns 200 for anonymous and authenticated users | N/A |
| P1.2 | All products in DB are displayed as cards | DB has 0 products → shows "No products available" |
| P1.3 | Each card shows: name, truncated description, price, image (or SVG placeholder), stock badge, "View Details" link | Product has no image → SVG placeholder shown |
| P1.4 | Green "X in stock" badge when stock > 10 | Stock > 10 → badge shows "in stock" |
| P1.5 | Amber "Only X left" badge when 1 ≤ stock ≤ 10 | Stock = 1 → shows "Only 1 left" |
| P1.6 | Red "Out of Stock" badge when stock = 0 | Stock = 0 → shows "Out of Stock" |
| P1.7 | Expiry badge hidden when `expiry_date` is null | Product has no expiry → no badge rendered |

### 1.2 Product Detail (`/products/<pk>/`)

| ID | Acceptance Criteria | Risk / Edge Case |
|---|---|---|
| P2.1 | Page returns 200 for valid pk | Invalid pk → 404 |
| P2.2 | Shows: name (h1), price, full description, stock badge, expiry date (if set), image | No image → SVG placeholder |
| P2.3 | "Place Order" button shown when authenticated AND stock > 0 | Stock = 0 → button hidden; Unauthenticated → not shown |
| P2.4 | "Login to Order" button shown when anonymous AND stock > 0 | Stock = 0 → button hidden (guard added in fix) |
| P2.5 | "Login to Order" link includes `?next=/products/<pk>/` for post-login redirect | N/A |
| P2.6 | "Back to Products" link always shown | N/A |

---

## 2. User Authentication

### 2.1 Signup (`/users/signup/`)

| ID | Acceptance Criteria | Risk / Edge Case |
|---|---|---|
| A1.1 | Page returns 200 on GET, shows form with CSRF | N/A |
| A1.2 | Valid POST: creates User + UserProfile, redirects to `/login/` | N/A |
| A1.3 | Duplicate username → field error "already exists" | Case-insensitive collision possible |
| A1.4 | Passwords don't match → field error | N/A |
| A1.5 | Password too short (< 8 chars) → validation error | N/A |
| A1.6 | Password too common (e.g. "password") → validation error | N/A |
| A1.7 | Password entirely numeric → validation error | N/A |
| A1.8 | Password too similar to username → validation error | N/A |

### 2.2 Login (`/login/`)

| ID | Acceptance Criteria | Risk / Edge Case |
|---|---|---|
| A2.1 | Page returns 200 on GET, shows form with CSRF | N/A |
| A2.2 | Valid credentials → login, redirect to `?next=` (if present) or `/` | No `next` param → redirects to home |
| A2.3 | Invalid credentials → form error "Please enter a correct username and password" | N/A |
| A2.4 | Hidden field `<input name="next">` included when `?next=` in URL (fix: login template) | N/A |

### 2.3 Logout (`/logout/`)

| ID | Acceptance Criteria | Risk / Edge Case |
|---|---|---|
| A3.1 | GET shows confirmation page with "Sign Out" button | N/A |
| A3.2 | POST logs out user, redirects to `/login/` | N/A |
| A3.3 | Accessible to anonymous users (no `@login_required`) | Shows same page |

### 2.4 Navigation (role-based)

| ID | Acceptance Criteria | Risk / Edge Case |
|---|---|---|
| A4.1 | Anonymous sees: Home, Products, Sign Up, Login | Order and Logout hidden |
| A4.2 | Authenticated sees: Home, Products, Order, Logout | Sign Up and Login hidden |
| A4.3 | Staff sees additional "Admin" link | N/A |

---

## 3. Order Placement

### 3.1 Place Order (`/orders/place/<product_id>/`)

| ID | Acceptance Criteria | Risk / Edge Case |
|---|---|---|
| O1.1 | GET returns 200 for authenticated user, shows quantity form | Unauthenticated → 302 to `/login/?next=...` |
| O1.2 | Form shows: product name, price, quantity input (min=1, max=stock), Submit, back link | N/A |
| O1.3 | Valid POST (1 ≤ qty ≤ stock): creates Order, decrements stock, redirects to `/orders/success/` | N/A |
| O1.4 | qty > stock → error "Only N in stock" (200, no order created) | Boundary: qty = stock + 1 |
| O1.5 | qty = 0 → error "Quantity must be at least 1" | Boundary |
| O1.6 | qty < 0 → error "Quantity must be at least 1" | Negative integer |
| O1.7 | Non-numeric qty (e.g. "abc") → error "Quantity must be a whole number" | No 500 error (fix applied) |
| O1.8 | Missing qty → error "Quantity must be a whole number" | Empty POST body |
| O1.9 | Invalid product_id → 404 | N/A |

### 3.2 Place Order Index (`/orders/place/`)

| ID | Acceptance Criteria | Risk / Edge Case |
|---|---|---|
| O2.1 | Always redirects to `/products/` regardless of auth | N/A |

### 3.3 Order Success (`/orders/success/`)

| ID | Acceptance Criteria | Risk / Edge Case |
|---|---|---|
| O3.1 | Returns 200, shows "Order Placed Successfully" | Accessible to anyone (no auth check) |
| O3.2 | "Continue Shopping" link goes to `/products/` | N/A |

---

## 4. Admin Dashboard (`/admin/`)

| ID | Acceptance Criteria | Risk / Edge Case |
|---|---|---|
| D1.1 | Anonymous → 302 redirect to `/admin/login/` | N/A |
| D1.2 | Authenticated non-staff → 302 redirect to admin login | Tested via `no_redirect` |
| D1.3 | Staff → 200, shows "OneStep Pharmacy Administration" branding | N/A |
| D1.4 | Product admin: list with id, name, price, stock, expiry, image preview; search by name; filter by expiry | N/A |
| D1.5 | Order admin: list with id, user, product, qty, status, date; filter by status/date; search by username/product | N/A |
| D1.6 | UserProfile admin: list with user, phone, address; search by username/phone | N/A |

---

## 5. Seed Data — Production Scale

| ID | Acceptance Criteria | Risk / Edge Case |
|---|---|---|
| S1.1 | 6 users: admin (staff/superuser), staff_jane (staff), alice, bob, carol, dave | Passwords: `admin123`, `staffpass12`, `customer1A!`, etc. |
| S1.2 | 10 products with images (Wikimedia/Pexels), varying prices ($4.99–$15.99), stocks (60–200), expiry dates | All images downloadable at seed time |
| S1.3 | 10 orders across users, 3 statuses (Pending/Shipped/Delivered), date range 60 days | Stock decremented for each order |
| S1.4 | All users have UserProfile with address and phone | N/A |
| S1.5 | Media directory cleaned of orphaned files | Old `download_*.jpg` and `.svg` removed |

---

## 6. Sanitization & Security

| ID | Acceptance Criteria | Risk / Edge Case |
|---|---|---|
| SE1.1 | CSRF token on every POST form (login, signup, logout, order) | Missing token → 403 |
| SE1.2 | DB excluded from git via `.gitignore` | Confirmed via `git check-ignore` |
| SE1.3 | Media files excluded from git via `.gitignore` | `media/product_images/` in `.gitignore` |
| SE1.4 | `SECURE_CONTENT_TYPE_NOSNIFF = True` | N/A |
| SE1.5 | `SECURE_BROWSER_XSS_FILTER = True` | N/A |
| SE1.6 | `X_FRAME_OPTIONS = 'DENY'` | Clickjacking prevention |
| SE1.7 | `SESSION_COOKIE_HTTPONLY = True`, `CSRF_COOKIE_HTTPONLY = True` | N/A |
| SE1.8 | `SSESSION_COOKIE_SAMESITE = 'Lax'`, `CSRF_COOKIE_SAMESITE = 'Lax'` | N/A |

---

## Edge Case Matrix (Cross-Feature)

| Scenario | Feature | Expected | Risk Level |
|---|---|---|---|
| User orders while product stock = 0 | Order | Button hidden on detail; form shows max=0, server rejects qty>0 | **High** (data integrity) |
| User sends non-numeric quantity | Order | Error message, no order created, no 500 | **High** (crash prevention) |
| Anonymous hits `/orders/place/N/` | Order | Redirect to login with `?next=` | **Medium** (UX) |
| User logs in after `?next=` redirect | Auth | Redirected to original page, not home | **Medium** (UX) |
| Two simultaneous users ordering last unit | Order | No over-sell (DB-level constraint is advisory) | **Low** (SQLite concurrency) |
| User signs up with existing username | Auth | Form error, no duplicate user | **Medium** |
| Staff accesses order admin | Admin | Shows all orders from all users | **Low** |
| Product with no expiry | Catalog | Expiry badge hidden, no error | **Low** |
| Product with no image | Catalog | SVG placeholder, no broken image | **Low** |
| All products deleted | Catalog | "No products available" message | **Low** |
