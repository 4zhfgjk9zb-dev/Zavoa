
const demoDeals=[
 {brand:"Beispielmarke",name:"Kopfhörer Pro",price:"199 €",old:"statt 249 €",score:"92/100"},
 {brand:"Beispielmarke",name:"65″ 4K OLED TV",price:"899 €",old:"statt 1.099 €",score:"90/100"},
 {brand:"Beispielmarke",name:"Smartwatch",price:"239 €",old:"statt 299 €",score:"88/100"},
 {brand:"Beispielmarke",name:"Sneaker",price:"89 €",old:"statt 119 €",score:"87/100"}
];
const grid=document.getElementById("dealGrid");
if(grid)grid.innerHTML=demoDeals.map(d=>`<article class="card"><div class="productpic"><div class="product-placeholder">Produktbild<br>kommt aus dem Partner-Feed</div></div><span class="score">ZAVOA Score ${d.score}</span><h3>${d.name}</h3><div class="muted">${d.brand}</div><div class="dealprice">${d.price}</div><div class="muted">${d.old}</div><a class="btn green" href="#" onclick="event.preventDefault();alert('Demo – Live-Link folgt nach Partnerfreischaltung.')">Angebot ansehen</a></article>`).join("");
function showDemoCode(b){b.closest(".coupon-code").classList.add("revealed");b.textContent="Demo-Code"}
function filterCoupons(){const q=(document.getElementById("couponShopSearch")?.value||"").toLowerCase();document.querySelectorAll("#couponGrid .coupon-card").forEach(c=>c.style.display=!q||(c.dataset.shop||"").toLowerCase().includes(q)?"":"none")}
