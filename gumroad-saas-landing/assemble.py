#!/usr/bin/env python3
import os
D = os.path.expanduser("~/Desktop/Oficina_Ranuk/gumroad-saas-landing")
parts = []
for n in ["head.html","nav.html","hero.html","problem.html","features.html","pricing.html","testimonials.html","faq.html","cta.html","scripts.html"]:
    p = os.path.join(D, n)
    if os.path.exists(p):
        with open(p) as f: parts.append(f.read())
html = "\n".join(parts)
with open(os.path.join(D, "index.html"), "w") as f: f.write(html)
print(f"Wrote index.html ({len(html)} bytes)")
