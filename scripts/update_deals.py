#!/usr/bin/env python3
import csv, gzip, io, json, os, urllib.request
from datetime import datetime, timezone

FEED_URL=os.environ["AWIN_ANTHBOT_FEED_URL"]
OUT="deals.json"
MAX_DEALS=40

def money(v):
    if v is None: return None
    s=str(v).strip().replace("EUR","").replace("€","").strip().replace(",",".")
    try: return round(float(s),2)
    except: return None

with urllib.request.urlopen(FEED_URL, timeout=60) as r:
    raw=r.read()
if raw[:2]==b"\x1f\x8b":
    raw=gzip.decompress(raw)
text=raw.decode("utf-8-sig",errors="replace")
rows=list(csv.DictReader(io.StringIO(text)))

def get(row,*names):
    low={k.lower():v for k,v in row.items()}
    for n in names:
        v=low.get(n.lower())
        if v not in (None,""): return v.strip()
    return ""

deals=[]
for row in rows:
    availability=get(row,"availability").lower()
    if availability and availability not in ("in_stock","in stock","instock"): continue
    price=money(get(row,"price"))
    if not price or price<=0: continue
    title=get(row,"title","product_name","name")
    url=get(row,"aw_deep_link","deeplink","deep_link","merchant_deep_link","link")
    image=get(row,"image_link","merchant_image_url","image_url")
    if not title or not url or not image: continue
    sale=money(get(row,"sale_price"))
    current=sale if sale and sale>0 else price
    old=price if sale and sale<price else None
    saving=round(old-current,2) if old else None
    deals.append({
      "id": get(row,"id","product_id","merchant_product_id") or title.lower().replace(" ","-")[:80],
      "title": title,
      "subtitle": "ANTHBOT DE",
      "price": current,
      "oldPrice": old,
      "currency": "€",
      "savings": saving,
      "image": image,
      "imageAlt": title,
      "affiliateUrl": url,
      "active": True,
      "merchant": "ANTHBOT DE"
    })

deals.sort(key=lambda d: (d["savings"] or 0, -d["price"]), reverse=True)
payload={"updated":datetime.now(timezone.utc).isoformat(),"source":"AWIN ANTHBOT DE","deals":deals[:MAX_DEALS]}
with open(OUT,"w",encoding="utf-8") as f:
    json.dump(payload,f,ensure_ascii=False,indent=2)
    f.write("\n")
print(f"Wrote {len(payload['deals'])} active deals from {len(rows)} feed rows")
