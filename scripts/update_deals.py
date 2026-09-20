#!/usr/bin/env python3
import csv, gzip, io, json, os, urllib.request
from datetime import datetime, timezone

FEEDS=[
    ("ANTHBOT DE", os.environ["AWIN_ANTHBOT_FEED_URL"]),
    ("OutIn Germany", os.environ["AWIN_OUTIN_FEED_URL"]),
    ("Blitec DE", os.environ["AWIN_BLITEC_FEED_URL"]),
]
OUT="deals.json"
HISTORY="price-history.json"
MAX_DEALS=40
MIN_MAIN_PRICE=100

# Manually verified deals stay visible even when the feed has no comparison price.
PINNED_DEALS=[{
  "id":"anthbot-m5-verified",
  "title":"ANTHBOT M5",
  "subtitle":"Kabelloser Smart-Mähroboter",
  "price":599,
  "oldPrice":749,
  "currency":"€",
  "savings":150,
  "discountPercent":20.0,
  "image":"anthbot-m5-illustration.png",
  "imageAlt":"Illustration des ANTHBOT M5 Mähroboters",
  "imageNote":"Produktabbildung: Illustration",
  "affiliateUrl":"https://www.awin1.com/cread.php?awinmid=125144&awinaffid=3095153&ued=https%3A%2F%2Fde.anthbot.com%2Fproducts%2Fm5-robot-lawn-mower%3Fvariant%3D52055426236729",
  "active":True,
  "merchant":"ANTHBOT DE",
  "verified":True
}]
MIN_DROP_PERCENT=5

def money(v):
    if v is None: return None
    s=str(v).strip().replace("EUR","").replace("€","").strip().replace(",",".")
    try: return round(float(s),2)
    except: return None

def get(row,*names):
    low={k.lower():v for k,v in row.items()}
    for n in names:
        v=low.get(n.lower())
        if v not in (None,""): return v.strip()
    return ""

try:
    with open(HISTORY,encoding="utf-8") as f: history=json.load(f)
except (FileNotFoundError,json.JSONDecodeError):
    history={"products":{}}

all_rows=[]
for merchant, feed_url in FEEDS:
    with urllib.request.urlopen(feed_url, timeout=60) as r: raw=r.read()
    if raw[:2]==b"\x1f\x8b": raw=gzip.decompress(raw)
    feed_rows=list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig",errors="replace"))))
    for row in feed_rows:
        row["_zavoa_merchant"]=merchant
        all_rows.append(row)
rows=all_rows
now=datetime.now(timezone.utc).isoformat()
deals=[]

for row in rows:
    merchant=row.get("_zavoa_merchant","AWIN")
    availability=get(row,"availability").lower()
    if availability and availability not in ("in_stock","in stock","instock"): continue
    regular=money(get(row,"price"))
    sale=money(get(row,"sale_price"))
    current=sale if sale and regular and 0<sale<regular else regular
    if not current or current<MIN_MAIN_PRICE: continue
    title=get(row,"title","product_name","name")
    url=get(row,"aw_deep_link","deeplink","deep_link","merchant_deep_link","link")
    image=get(row,"image_link","merchant_image_url","image_url")
    raw_pid=get(row,"id","product_id","merchant_product_id") or title.lower().replace(" ","-")[:80]
    pid=(merchant.lower().replace(" ","-")+"-"+raw_pid)
    if not title or not url or not image: continue

    h=history["products"].setdefault(pid,{"title":title,"prices":[]})
    previous=[p["price"] for p in h.get("prices",[]) if p.get("price")]
    historical=max(previous) if previous else None
    h["title"]=title
    h.setdefault("prices",[]).append({"at":now,"price":current})
    h["prices"]=h["prices"][-120:]

    comparison=regular if sale and regular and sale<regular else historical
    if not comparison or current>=comparison: continue
    saving=round(comparison-current,2)
    drop=100*saving/comparison
    if drop<MIN_DROP_PERCENT: continue
    deals.append({
      "id":pid,"title":title,"subtitle":merchant,"price":current,
      "oldPrice":comparison,"currency":"€","savings":saving,
      "discountPercent":round(drop,1),"image":image,"imageAlt":title,
      "affiliateUrl":url,"active":True,"merchant":merchant
    })

deals.sort(key=lambda d:(d["discountPercent"],d["savings"]),reverse=True)
auto_ids={d["id"] for d in deals}
deals=[d for d in PINNED_DEALS if d["id"] not in auto_ids]+deals
with open(HISTORY,"w",encoding="utf-8") as f:
    json.dump(history,f,ensure_ascii=False,indent=2); f.write("\n")
with open(OUT,"w",encoding="utf-8") as f:
    json.dump({"updated":now,"source":"AWIN ANTHBOT DE + OutIn Germany + Blitec DE","deals":deals[:MAX_DEALS]},f,ensure_ascii=False,indent=2); f.write("\n")
print(f"Tracked {len(history['products'])} products; published {len(deals[:MAX_DEALS])} verified price-drop deals")
