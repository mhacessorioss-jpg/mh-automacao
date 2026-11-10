const {chromium}=require('playwright'); const fs=require('fs');
const F='file://'+__dirname+'/node_modules/@fontsource'; const M='/home/claude/mh-automacao/marca';
const [W,H,out,kick]=process.argv.slice(2); const story=H>1500;
(async()=>{const b=await chromium.launch();
const html=`<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Corm;font-weight:300;src:url(${F}/cormorant-garamond/files/cormorant-garamond-latin-300-normal.woff2)}
@font-face{font-family:Corm;font-weight:500;src:url(${F}/cormorant-garamond/files/cormorant-garamond-latin-500-normal.woff2)}
@font-face{font-family:Corm;font-weight:400;font-style:italic;src:url(${F}/cormorant-garamond/files/cormorant-garamond-latin-400-italic.woff2)}
@font-face{font-family:Barl;font-weight:300;src:url(${F}/barlow-semi-condensed/files/barlow-semi-condensed-latin-300-normal.woff2)}
@font-face{font-family:Barl;font-weight:500;src:url(${F}/barlow-semi-condensed/files/barlow-semi-condensed-latin-500-normal.woff2)}
*{margin:0;padding:0;box-sizing:border-box}
body{width:${W}px;height:${H}px;position:relative;overflow:hidden;background:#2A1E16;color:#F4EADD;font-family:Barl}
.foto{position:absolute;left:0;right:0;top:0;height:${story?1180:760}px;background:url('file://${M}/modelo_oficial_sem_joias.png') center 22%/cover}
.grad{position:absolute;left:0;right:0;top:${story?760:400}px;height:440px;background:linear-gradient(to bottom,rgba(42,30,22,0),#2A1E16)}
.live{position:absolute;top:${story?150:56}px;left:56px;display:flex;align-items:center;gap:12px;background:#B3261E;color:#fff;font-weight:500;font-size:${story?30:26}px;letter-spacing:.18em;padding:12px 22px}
.live:before{content:'';width:14px;height:14px;border-radius:50%;background:#fff}
.p{position:absolute;left:70px;right:70px;bottom:${story?250:70}px;text-align:center}
.logos{display:flex;align-items:center;justify-content:center;gap:36px;margin-bottom:${story?40:26}px}
.logos img{display:block}.s1{width:${story?118:96}px}.s2{height:${story?92:76}px}.sep{width:1.5px;height:${story?90:72}px;background:#C29A62}
.k{font-weight:500;font-size:${story?26:22}px;letter-spacing:.3em;color:#D2A86E}
.t{font-family:Corm;font-weight:300;font-size:${story?118:96}px;line-height:.95;margin-top:${story?22:14}px}.t i{font-style:italic;font-weight:400;color:#D2A86E}
.d{display:inline-block;margin-top:${story?34:24}px;border:1.5px solid #C29A62;padding:${story?16:12}px 34px;font-weight:500;font-size:${story?40:32}px;letter-spacing:.12em}
.b{margin-top:${story?30:20}px;font-weight:300;font-size:${story?33:27}px;line-height:1.45;color:#E4D6C3}
</style></head><body><div class="foto"></div><div class="grad"></div><div class="live">LIVE</div>
<div class="p"><div class="logos"><img class="s1" src="file://${M}/selo_branco.png"><span class="sep"></span><img class="s2" src="file://${__dirname}/valenra_logo_claro.png"></div>
<div class="k">${kick}</div><div class="t">Live de <i>Black Friday</i></div>
<div class="d">QUARTA · 11/11 · 12H</div>
<div class="b">Ofertas exclusivas ao vivo, novidades<br>e muita conversa boa com a gente.</div></div></body></html>`;
fs.writeFileSync(__dirname+'/_l.html',html); const p=await b.newPage({viewport:{width:+W,height:+H}});
await p.goto('file://'+__dirname+'/_l.html'); await p.waitForTimeout(700); await p.screenshot({path:out,type:'jpeg',quality:93}); await b.close();})();
