import os

css_content = """
/* ── PAGE HEADER ── */
.page-header { margin-bottom: var(--space-8); animation: fadeInUp var(--duration-slow) var(--ease-spring) both; text-align: center; max-width: 640px; margin-left: auto; margin-right: auto; }
.page-header h1 { font-size: clamp(2rem, 4vw, 3rem); font-weight: 800; letter-spacing: -0.03em; margin-bottom: var(--space-2); }
.page-header p { font-size: 1.15rem; color: var(--text-secondary); }

/* ── PRODUCT DETAIL ── */
.detail-layout { display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-8); align-items: start; animation: fadeInUp var(--duration-slow) var(--ease-spring) both; }
.detail-image { border-radius: var(--radius-2xl); overflow: hidden; background: var(--bg-surface-hover); aspect-ratio: 1; display: flex; align-items: center; justify-content: center; border: 1px solid var(--border-light); box-shadow: var(--shadow-md); }
.detail-image img { width: 100%; height: 100%; object-fit: cover; }
.detail-image.no-image { color: var(--border-strong); font-size: 4rem; }
.detail-info { display: flex; flex-direction: column; }
.detail-rating { display: flex; align-items: center; gap: var(--space-2); margin-bottom: var(--space-3); }
.detail-rating .stars { color: var(--warning); font-size: 1rem; letter-spacing: 2px; }
.detail-rating .count { font-size: 0.9rem; color: var(--text-secondary); }
.detail-info h1 { font-size: clamp(2rem, 3vw, 2.5rem); font-weight: 800; letter-spacing: -0.02em; margin-bottom: var(--space-2); }
.detail-price { font-size: 2.5rem; font-weight: 800; color: var(--primary-500); margin-bottom: var(--space-4); letter-spacing: -0.03em; }
.detail-description { font-size: 1.05rem; color: var(--text-secondary); line-height: 1.7; margin-bottom: var(--space-6); }
.detail-meta { display: flex; flex-direction: column; gap: var(--space-3); margin-bottom: var(--space-6); padding: var(--space-4); background: var(--bg-surface-hover); border-radius: var(--radius-xl); border: 1px solid var(--border-light); }
.detail-meta .meta-row { display: flex; align-items: center; gap: var(--space-2); font-size: 0.95rem; color: var(--text-secondary); }
.detail-meta .meta-row strong { color: var(--text-primary); min-width: 100px; font-weight: 600; }
.detail-actions { display: flex; gap: var(--space-3); flex-wrap: wrap; }
.btn-disabled { background: var(--bg-surface-hover); color: var(--text-tertiary); border: 1px solid var(--border-light); cursor: not-allowed; }
.btn-lg { padding: 16px 32px; font-size: 1.05rem; }

@media (max-width: 900px) {
  .detail-layout { grid-template-columns: 1fr; gap: var(--space-6); }
}
"""

with open("/home/neo/Projects/onesteppharmacy/pharmacy_ecommerce/products/static/css/styles.css", "a") as f:
    f.write(css_content)

print("CSS products components appended.")
