const {chromium}=require('playwright'); const fs=require('fs');
const F='file://'+__dirname+'/node_modules/@fontsource'; const M='/home/claude/mh-automacao/marca';
const html=`<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Corm;font-weight:300;src:url(${F}/cormorant-garamond/files/cormorant-garamond-latin-300-normal.woff2)}
@font-face{font-family:Corm;font-weight:500;src:url(${F}/cormorant-garamond/files/cormorant-garamond-latin-500-normal.woff2)}
@font-face{font-family:Corm;font-weight:400;font-style:italic;src:url(${F}/cormorant-garamond/files/cormorant-garamond-latin-400-italic.woff2)}
@font-face{font-family:Barl;font-weight:300;src:url(${F}/barlow-semi-condensed/files/barlow-semi-condensed-latin-300-normal.woff2)}
@font-face{font-family:Barl;font-weight:500;src:url(${F}/barlow-semi-condensed/files/barlow-semi-condensed-latin-500-normal.woff2)}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1920px;background:#F2E8DC;position:relative;overflow:hidden;font-family:Barl;color:#2A1E16}
.frame{position:absolute;inset:36px;border:1.5px solid #C29A62}
.c{position:absolute;left:100px;right:100px;top:300px;bottom:300px;text-align:center;display:flex;flex-direction:column;align-items:center;justify-content:space-between}
.logos{display:flex;align-items:center;gap:44px}.selo{width:190px;display:block}.sep{width:1.5px;height:110px;background:#C29A62}.val{height:118px;}
.k{font-weight:500;font-size:26px;letter-spacing:.32em;color:#A8804F}
.t{font-family:Corm;font-weight:300;font-size:100px;line-height:1;margin-top:22px}.t i{font-style:italic;font-weight:400;color:#A8804F}
.ic{width:130px;height:130px}
.b{font-weight:300;font-size:36px;line-height:1.5;color:#4A3A2E}
.b b{font-weight:500;color:#2A1E16}
.taxa{width:600px;background:#2A1E16;color:#F2E8DC;padding:30px 0 34px;text-align:center}
.taxa .l{font-weight:500;font-size:24px;letter-spacing:.26em;color:#D2A86E}
.taxa .v{font-family:Corm;font-weight:500;font-size:96px;line-height:1;margin-top:8px;font-variant-numeric:lining-nums}.taxa .v small{font-size:44px;vertical-align:top;line-height:1.7;margin-right:8px}
.cta{font-weight:300;font-size:30px;line-height:1.45;color:#4A3A2E}
.cta b{font-weight:500;color:#2A1E16}
</style></head><body><div class="frame"></div>
<div class="c"><div class="logos"><img class="selo" src="file://${M}/selo_marrom.png"></div>
<div class="k">AVISO ÀS NOSSAS CLIENTES</div>
<div class="t">Suas joias,<br><i>até a sua porta</i></div>
<svg class="ic" viewBox="0 0 64 64" fill="none" stroke="#A8804F" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="15" cy="45" r="7"/><circle cx="49" cy="45" r="7"/><path d="M22 45h17c0-8 4-14 10-14"/><path d="M15 38c2-6 7-8 13-8h8l3 15"/><path d="M42 18h5l4 13"/><path d="M45 18l-3-2"/><rect x="10" y="17" width="17" height="13" rx="2"/><path d="M14 23h9"/></svg>
<div class="b">Pensando em facilitar a sua vida, quem tem <b>entregas pendentes</b> pode receber a sua peça em casa, com a comodidade do nosso <b>motoboy</b>.</div>
<div class="taxa"><div class="l">TAXA FIXA DE ENTREGA</div><div class="v"><small>R$</small>10,00</div></div>
<div class="cta">Quer receber? É só chamar a gente no <b>direct</b><br>com a mensagem <b>"QUERO ENTREGA"</b>.</div></div>
</body></html>`;
(async()=>{const b=await chromium.launch(); fs.writeFileSync(__dirname+'/_m.html',html);
const p=await b.newPage({viewport:{width:1080,height:1920}}); await p.goto('file://'+__dirname+'/_m.html'); await p.waitForTimeout(700);
await p.screenshot({path:'/home/claude/mh-automacao/campanhas/avisos/entrega_motoboy_story.jpg',type:'jpeg',quality:93}); await b.close();})();
