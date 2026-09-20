async function loadZavoaDeals(){
  const grids=document.querySelectorAll('[data-deals-grid]');
  if(!grids.length)return;
  try{
    const r=await fetch('deals.json',{cache:'no-store'}); if(!r.ok)throw new Error('Deals konnten nicht geladen werden');
    const data=await r.json(); const deals=(data.deals||[]).filter(d=>d.active!==false);
    const card=d=>{const f=n=>new Intl.NumberFormat('de-DE',{style:'currency',currency:'EUR',maximumFractionDigits:0}).format(n);return `<article class="card"><div class="pic product-pic"><img src="${d.image}" alt="${d.imageAlt||d.title}"></div>${d.imageNote?`<div class="image-note">${d.imageNote}</div>`:''}<span class="badge">${d.savings} € Ersparnis</span><h3>${d.title}</h3><div class="muted">${d.subtitle||''}</div><div class="price">${f(d.price)}</div><div class="muted">statt ${f(d.oldPrice)}</div><a class="btn green" href="${d.affiliateUrl}" target="_blank" rel="sponsored noopener">Zum Angebot →</a></article>`};
    grids.forEach(g=>{const limit=Number(g.dataset.limit||deals.length);g.innerHTML=deals.slice(0,limit).map(card).join('')});
  }catch(e){console.error(e)}
}
document.addEventListener('DOMContentLoaded',loadZavoaDeals);
