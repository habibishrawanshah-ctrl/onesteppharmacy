import os

css_content = """
/* ── SECTIONS & GRIDS ── */
.section { padding: var(--space-12) 0; position: relative; }
.section-header { text-align: center; max-width: 640px; margin: 0 auto var(--space-8); }
.section-header h2 { font-size: clamp(1.8rem, 3vw, 2.4rem); font-weight: 800; color: var(--text-primary); margin-bottom: var(--space-2); }
.section-header p { font-size: 1.1rem; color: var(--text-secondary); }
.section-badge { display: inline-flex; align-items: center; background: var(--primary-50); color: var(--primary-600); padding: 6px 16px; border-radius: var(--radius-full); font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: var(--space-3); }

/* ── HERO SECTION ── */
.hero-section { position: relative; display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-8); align-items: center; padding: var(--space-8) 0 var(--space-12); min-height: 80vh; overflow: hidden; }
.hero-section::before { content: ''; position: absolute; top: -10%; left: -10%; width: 50%; height: 50%; background: radial-gradient(circle, var(--primary-50) 0%, transparent 70%); z-index: -1; filter: blur(60px); }
.hero-badge { display: inline-flex; align-items: center; gap: 8px; background: var(--bg-surface); border: 1px solid var(--border-light); color: var(--text-secondary); padding: 8px 16px; border-radius: var(--radius-full); font-size: 0.8rem; font-weight: 600; margin-bottom: var(--space-4); box-shadow: var(--shadow-sm); animation: fadeInUp 0.8s var(--ease-spring) both; }
.hero-content h1 { font-size: clamp(3rem, 5vw, 4.5rem); font-weight: 800; line-height: 1.05; letter-spacing: -0.04em; color: var(--text-primary); margin-bottom: var(--space-3); animation: fadeInUp 0.8s var(--ease-spring) 0.1s both; }
.hero-content h1 span { background: linear-gradient(135deg, var(--primary-500), var(--secondary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.hero-desc { font-size: 1.15rem; color: var(--text-secondary); line-height: 1.7; margin-bottom: var(--space-5); max-width: 520px; animation: fadeInUp 0.8s var(--ease-spring) 0.2s both; }
.hero-buttons { display: flex; gap: var(--space-3); flex-wrap: wrap; margin-bottom: var(--space-6); animation: fadeInUp 0.8s var(--ease-spring) 0.3s both; }
.trust-badges { display: flex; gap: var(--space-4); flex-wrap: wrap; animation: fadeInUp 0.8s var(--ease-spring) 0.4s both; }
.trust-badge { display: flex; align-items: center; gap: 8px; font-size: 0.85rem; font-weight: 500; color: var(--text-tertiary); }
.trust-badge svg { width: 18px; height: 18px; color: var(--success); }
.hero-visual { position: relative; display: flex; align-items: center; justify-content: center; animation: fadeInUp 1s var(--ease-spring) 0.3s both; }
.hero-image-wrapper { position: relative; width: 100%; max-width: 540px; }
.hero-main-image { width: 100%; border-radius: var(--radius-2xl); box-shadow: var(--shadow-lg); aspect-ratio: 4/3; object-fit: cover; border: 1px solid rgba(255,255,255,0.1); }
.hero-float-card { position: absolute; background: var(--bg-surface-elevated); backdrop-filter: blur(12px); border: 1px solid var(--border-light); border-radius: var(--radius-lg); padding: var(--space-3); box-shadow: var(--shadow-md); display: flex; align-items: center; gap: var(--space-2); animation: fadeInUp 1s var(--ease-spring) 0.6s both; }
.hero-float-card-1 { bottom: -20px; left: -20px; }
.hero-float-card-2 { top: 40px; right: -30px; }
.float-card-icon { width: 48px; height: 48px; border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center; font-size: 1.3rem; }
.float-card-icon.green { background: var(--success-light); color: var(--success); }
.float-card-icon.blue { background: var(--primary-50); color: var(--primary-500); }
.float-card-text p { font-size: 0.8rem; color: var(--text-tertiary); margin: 0; }
.float-card-text strong { font-size: 1.05rem; font-weight: 800; color: var(--text-primary); }

/* ── PRODUCT CARDS ── */
.products-grid, .product-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: var(--space-4); }
.product-card { display: flex; flex-direction: column; background: var(--bg-surface); border-radius: var(--radius-xl); border: 1px solid var(--border-light); overflow: hidden; transition: transform var(--duration-normal) var(--ease-out), box-shadow var(--duration-normal) var(--ease-out), border-color var(--duration-normal); position: relative; box-shadow: var(--shadow-sm); }
.product-card:hover { transform: translateY(-6px); box-shadow: var(--shadow-lg); border-color: transparent; }
.product-image { width: 100%; aspect-ratio: 4/3; background: var(--bg-surface-hover); display: flex; align-items: center; justify-content: center; overflow: hidden; position: relative; }
.product-image img { width: 100%; height: 100%; object-fit: cover; transition: transform var(--duration-slow) var(--ease-out); }
.product-card:hover .product-image img { transform: scale(1.05); }
.product-image.no-image { color: var(--border-strong); }
.product-wishlist { position: absolute; top: var(--space-2); right: var(--space-2); width: 36px; height: 36px; border-radius: 50%; background: var(--bg-surface-elevated); backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; border: 1px solid var(--border-light); cursor: pointer; opacity: 0; transform: translateY(4px); transition: all var(--duration-fast); color: var(--text-tertiary); box-shadow: var(--shadow-sm); }
.product-card:hover .product-wishlist { opacity: 1; transform: translateY(0); }
.product-wishlist:hover { color: var(--danger); background: var(--danger-light); border-color: var(--danger-light); }
.product-info { padding: var(--space-3); display: flex; flex-direction: column; gap: var(--space-1); flex: 1; }
.product-info h3 { font-size: 1.1rem; font-weight: 700; color: var(--text-primary); margin: 0; }
.product-info .description { font-size: 0.85rem; color: var(--text-secondary); line-height: 1.5; margin: 0; flex: 1; }
.product-meta { display: flex; gap: var(--space-1); flex-wrap: wrap; margin-bottom: var(--space-2); }
.product-meta .badge { font-size: 0.7rem; padding: 4px 10px; border-radius: var(--radius-full); font-weight: 600; background: var(--bg-surface-hover); color: var(--text-secondary); border: 1px solid var(--border-light); }
.product-card-footer { display: flex; align-items: center; justify-content: space-between; padding-top: var(--space-3); border-top: 1px solid var(--border-light); margin-top: auto; }
.price { font-size: 1.25rem; font-weight: 800; color: var(--primary-500); letter-spacing: -0.02em; }
.stock-badge { font-size: 0.75rem; font-weight: 600; padding: 4px 12px; border-radius: var(--radius-full); }
.stock-badge.in-stock { background: var(--success-light); color: var(--success); }
.stock-badge.low-stock { background: var(--warning-light); color: var(--warning); }
.stock-badge.out-of-stock { background: var(--danger-light); color: var(--danger); }
.product-card-actions { display: flex; gap: var(--space-2); padding: 0 var(--space-3) var(--space-3); }
.product-card-actions .btn { flex: 1; font-size: 0.85rem; padding: 10px 16px; }

/* ── STEPS & BENEFITS & TESTIMONIALS ── */
.steps-grid, .benefits-grid, .testimonials-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-4); }
.step-card, .benefit-card, .testimonial-card { text-align: left; padding: var(--space-5) var(--space-4); background: var(--bg-surface); border-radius: var(--radius-xl); border: 1px solid var(--border-light); transition: all var(--duration-normal) var(--ease-out); box-shadow: var(--shadow-sm); }
.step-card:hover, .benefit-card:hover, .testimonial-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-lg); }
.step-number { width: 56px; height: 56px; border-radius: var(--radius-xl); background: var(--primary-50); color: var(--primary-500); display: flex; align-items: center; justify-content: center; font-size: 1.4rem; font-weight: 800; margin-bottom: var(--space-4); transition: transform var(--duration-fast); }
.step-card:hover .step-number { transform: scale(1.05); background: var(--primary-500); color: white; }
.step-card h3, .benefit-card h3 { font-size: 1.15rem; font-weight: 700; margin-bottom: var(--space-2); }
.step-card p, .benefit-card p { font-size: 0.9rem; color: var(--text-secondary); line-height: 1.6; }
.benefit-icon { width: 56px; height: 56px; border-radius: var(--radius-xl); display: flex; align-items: center; justify-content: center; font-size: 1.4rem; margin-bottom: var(--space-4); }
.benefit-icon.blue { background: var(--primary-50); color: var(--primary-500); }
.benefit-icon.teal { background: var(--secondary-light); color: var(--secondary); }
.benefit-icon.green { background: var(--success-light); color: var(--success); }
.benefit-stat { font-size: 2rem; font-weight: 800; color: var(--text-primary); margin-top: var(--space-3); letter-spacing: -0.03em; }
.benefit-stat-label { font-size: 0.8rem; color: var(--text-secondary); font-weight: 500; }
.testimonial-stars { color: var(--warning); font-size: 1rem; letter-spacing: 2px; margin-bottom: var(--space-3); }
.testimonial-text { font-size: 0.95rem; color: var(--text-secondary); line-height: 1.7; margin-bottom: var(--space-4); font-style: italic; }
.testimonial-author { display: flex; align-items: center; gap: var(--space-2); }
.testimonial-avatar { width: 48px; height: 48px; border-radius: 50%; background: linear-gradient(135deg, var(--primary-50), var(--primary-100)); color: var(--primary-600); display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.95rem; flex-shrink: 0; }
.testimonial-name { font-size: 0.9rem; font-weight: 700; color: var(--text-primary); }
.testimonial-role { font-size: 0.8rem; color: var(--text-tertiary); }

/* ── NEWSLETTER ── */
.newsletter-section { background: linear-gradient(135deg, var(--primary-600), var(--primary-700)); border-radius: var(--radius-2xl); padding: var(--space-10) var(--space-6); text-align: center; color: white; position: relative; overflow: hidden; box-shadow: var(--shadow-lg); }
.newsletter-section::before { content: ''; position: absolute; inset: 0; background: radial-gradient(circle at 30% 20%, rgba(255,255,255,0.1) 0%, transparent 50%); }
.newsletter-section h2 { font-size: clamp(2rem, 3vw, 2.5rem); font-weight: 800; margin-bottom: var(--space-2); position: relative; color: white; }
.newsletter-section p { opacity: 0.9; margin-bottom: var(--space-5); position: relative; font-size: 1.1rem; }
.newsletter-form { display: flex; gap: var(--space-2); max-width: 480px; margin: 0 auto; position: relative; }
.newsletter-form input { flex: 1; padding: 16px 24px; border-radius: var(--radius-full); border: none; font-size: 1rem; font-family: var(--font-sans); outline: none; box-shadow: var(--shadow-sm); }
.newsletter-form input:focus { box-shadow: 0 0 0 4px rgba(255,255,255,0.2); }
.newsletter-form .btn { background: var(--text-primary); color: var(--bg-surface); }
.newsletter-form .btn:hover { opacity: 0.9; }

/* ── RESPONSIVE COMPATIBILITY ── */
@media (max-width: 1024px) {
  .hero-section { grid-template-columns: 1fr; text-align: center; min-height: auto; padding: var(--space-6) 0 var(--space-8); }
  .hero-desc { margin: 0 auto var(--space-5); }
  .hero-buttons, .trust-badges { justify-content: center; }
  .steps-grid, .benefits-grid, .testimonials-grid { grid-template-columns: repeat(2, 1fr); }
  .footer-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 768px) {
  .hero-content h1 { font-size: 2.5rem; }
  .products-grid, .product-list { grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); }
  .steps-grid, .benefits-grid, .testimonials-grid { grid-template-columns: 1fr; }
  .footer-grid { grid-template-columns: 1fr; gap: var(--space-6); }
  .newsletter-form { flex-direction: column; }
}
"""

with open("/home/neo/Projects/onesteppharmacy/pharmacy_ecommerce/products/static/css/styles.css", "a") as f:
    f.write(css_content)

print("CSS appended.")
