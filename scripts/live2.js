const {chromium}=require('playwright'); const fs=require('fs');
const F='file://'+__dirname+'/node_modules/@fontsource'; const M='/home/claude/mh-automacao/marca';
const [W,H,out,faixa]=process.argv.slice(2); const story=H>1500;
(async()=>{const b=await chromium.launch();
const html=`<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Corm;font-weight:300;src:url(${F}/cormorant-garamond/files/cormorant-garamond-latin-300-normal.woff2)}
@font-face{font-family:Corm;font-weight:500;src:url(${F}/cormorant-garamond/files/cormorant-garamond-latin-500-normal.woff2)}
@font-face{font-family:Corm;font-weight:400;font-style:italic;src:url(${F}/cormorant-garamond/files/cormorant-garamond-latin-400-italic.woff2)}
@font-face{font-family:Barl;font-weight:300;src:url(${F}/barlow-semi-condensed/files/barlow-semi-condensed-latin-300-normal.woff2)}
@font-face{font-family:Barl;font-weight:500;src:url(${F}/barlow-semi-condensed/files/barlow-semi-condensed-latin-500-normal.woff2)}
*{margin:0;padding:0;box-sizing:border-box}
body{width:${W}px;height:${H}px;position:relative;overflow:hidden;background:#2A1E16;color:#F4EADD;font-family:Barl}
.foto{position:absolute;top:0;height:${story?1000:680}px;width:50%;background-size:cover;background-position:center 20%}
.f1{left:0;background-image:url('file://${M}/modelo_oficial_sem_joias.png')}.f2{right:0;background-image:url('file://${M}/valenra_modelo_sem_joias.png')}
.grad{position:absolute;left:0;right:0;top:${story?640:400}px;height:${story?365:285}px;background:linear-gradient(to bottom,rgba(42,30,22,0),#2A1E16)}
.live{position:absolute;top:${story?150:44}px;left:50%;transform:translateX(-50%);display:flex;align-items:center;gap:12px;background:#B3261E;color:#fff;font-weight:500;font-size:${story?32:24}px;letter-spacing:.2em;padding:12px 24px;white-space:nowrap}
.live:before{content:'';width:14px;height:14px;border-radius:50%;background:#fff}
.p{position:absolute;left:60px;right:60px;top:${story?860:540}px;text-align:center}
.logos{display:flex;align-items:center;justify-content:center;gap:34px;margin-bottom:${story?28:16}px}
.s1{width:${story?110:80}px}.s2{height:${story?86:62}px}.sep{width:1.5px;height:${story?84:60}px;background:#C29A62}
.t{font-family:Corm;font-weight:300;font-size:${story?140:100}px;line-height:.9}.t i{font-style:italic;font-weight:400;color:#D2A86E}
.d{display:inline-block;margin-top:${story?26:14}px;border:1.5px solid #C29A62;padding:${story?14:9}px 30px;font-weight:500;font-size:${story?36:26}px;letter-spacing:.12em}
.o{margin-top:${story?44:22}px;font-weight:300;font-size:${story?36:26}px;line-height:1.35;color:#E4D6C3}
.v{font-family:Corm;font-weight:500;font-size:${story?190:130}px;line-height:.95;color:#fff;font-variant-numeric:lining-nums;margin-top:${story?8:4}px}.v small{font-size:${story?80:56}px;vertical-align:top;line-height:1.6;margin-right:10px}
.av{font-weight:500;font-size:${story?34:24}px;letter-spacing:.24em;color:#D2A86E}
.r{margin-top:${story?40:16}px;font-weight:300;font-size:${story?28:21}px;letter-spacing:.06em;color:#BFAE98}
</style></head><body><div class="foto f1"></div><div class="foto f2"></div><div class="grad"></div><div class="live">${faixa}</div>
<div class="p"><div class="logos"><img class="s1" src="file://${M}/selo_branco.png"><span class="sep"></span><img class="s2" src="file://${M}/valenra_logo_claro.png"></div>
<div class="t">Live <i>11.11</i></div>
<div class="d">QUARTA · 11/11 · 12H</div>
<div class="o">Todas as peças divulgadas no grupo VIP<br>por apenas</div>
<div class="v"><small>R$</small>11,00</div><div class="av">À VISTA</div>
<div class="r">Só durante a live · ative o lembrete</div></div></body></html>`;
fs.writeFileSync(__dirname+'/_l2.html',html); const p=await b.newPage({viewport:{width:+W,height:+H}});
await p.goto('file://'+__dirname+'/_l2.html'); await p.waitForTimeout(700); await p.screenshot({path:out,type:'jpeg',quality:93}); await b.close();})();
