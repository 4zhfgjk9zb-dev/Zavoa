
const deals=[
{id:1,shop:"MediaMarkt",cat:"Elektronik",title:"Sony WH-1000XM6",desc:"Noise-Cancelling-Kopfhörer · Schwarz",price:269,compare:319,score:96,low:269,check:"vor 8 Min."},
{id:2,shop:"Zalando",cat:"Mode",title:"adidas Ultraboost 5",desc:"Ausgewählte Farben und Größen",price:109.95,compare:139.95,score:91,low:104.95,check:"vor 14 Min."},
{id:3,shop:"OTTO",cat:"Wohnen",title:"Ninja Airfryer AF300EU",desc:"Dual-Zone Heißluftfritteuse",price:129,compare:159,score:88,low:124,check:"vor 11 Min."},
{id:4,shop:"Douglas",cat:"Beauty",title:"20 % auf ausgewählte Düfte",desc:"Gutschein auf teilnehmende Marken",price:63.99,compare:79.99,score:89,low:61.99,check:"vor 6 Min."},
{id:5,shop:"Saturn",cat:"Elektronik",title:"Samsung Galaxy Watch7 44mm",desc:"Bluetooth · ausgewählte Farben",price:199,compare:239,score:86,low:195,check:"vor 19 Min."},
{id:6,shop:"HelloFresh",cat:"Essen",title:"Neukunden-Kochbox-Aktion",desc:"Rabatt verteilt auf die ersten Boxen",price:34.99,compare:49.99,score:82,low:34.99,check:"vor 23 Min."}
];
const eur=n=>new Intl.NumberFormat("de-DE",{style:"currency",currency:"EUR"}).format(n);
function renderDeals(q="",cat=""){
 let el=document.querySelector("#dealGrid"); if(!el) return;
 let arr=deals.filter(d=>(!cat||d.cat===cat)&&(!q||(d.title+" "+d.shop+" "+d.cat).toLowerCase().includes(q.toLowerCase())));
 el.innerHTML=arr.map(d=>{let save=d.compare-d.price,p=Math.round(save/d.compare*100);return `<article class="deal">
 <div class="dealtop"><span class="merchant">${d.shop}</span><span class="badge ${d.score>=90?'hot':''}">${d.score>=90?'🔥 Top Deal':'✓ Sehr gut'}</span></div>
 <h3>${d.title}</h3><div class="desc">${d.desc}</div>
 <div class="priceRow"><div><div class="price">${eur(d.price)}</div><div class="saving">${eur(save)} / ${p}% günstiger</div></div><div class="compare">Vergleichspreis<br><b>${eur(d.compare)}</b></div></div>
 <div class="scorebox"><div class="scoretop"><span>Deal Score</span><span>${d.score}/100</span></div><div class="bar"><div class="fill" style="width:${d.score}%"></div></div></div>
 <div class="proof"><div>90-Tage-Tief<b>${eur(d.low)}</b></div><div>zuletzt geprüft<b>${d.check}</b></div></div>
 <div class="actions"><button class="go" onclick="demoGo('${d.shop}')">Zum Angebot →</button><button class="bell" onclick="alert('Deal-Alert Demo')">🔔</button></div>
 <div class="adnote">Affiliate-/Werbelink · Provision beeinflusst den Deal Score nicht</div></article>`}).join("");
}
function demoGo(shop){alert("Demo: Später erfolgt hier die Affiliate-Weiterleitung zu "+shop+".")}
document.addEventListener("DOMContentLoaded",()=>{
 renderDeals();
 let s=document.querySelector("#search"); if(s)s.addEventListener("input",()=>renderDeals(s.value,""));
 document.querySelectorAll("[data-cat]").forEach(b=>b.addEventListener("click",()=>renderDeals(s?s.value:"",b.dataset.cat)));
});
