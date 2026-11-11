// node live11.js <itens.json> <saida>   itens: [{codigo,nome,obs}]
const {chromium}=require('playwright'); const fs=require('fs'); const path=require('path');
const F='file://'+__dirname+'/node_modules/@fontsource'; const FOT='/home/claude/mh-automacao/fotos';
const [itF,out]=process.argv.slice(2); const itens=JSON.parse(fs.readFileSync(itF,'utf8')); fs.mkdirSync(out,{recursive:true});
(async()=>{const b=await chromium.launch();
for(const it of itens){
 const fs_=fs.readdirSync(FOT).filter(n=>n.startsWith((it.foto||it.codigo)+'_')).sort(); const f1=`${FOT}/${fs_[0]}`, f2=fs_[1]?`${FOT}/${fs_[1]}`:null;
 const html=`<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Corm;font-weight:300;src:url(${F}/cormorant-garamond/files/cormorant-garamond-latin-300-normal.woff2)}
@font-face{font-family:Corm;font-weight:500;src:url(${F}/cormorant-garamond/files/cormorant-garamond-latin-500-normal.woff2)}
@font-face{font-family:Corm;font-weight:400;font-style:italic;src:url(${F}/cormorant-garamond/files/cormorant-garamond-latin-400-italic.woff2)}
@font-face{font-family:Barl;font-weight:300;src:url(${F}/barlow-semi-condensed/files/barlow-semi-condensed-latin-300-normal.woff2)}
@font-face{font-family:Barl;font-weight:500;src:url(${F}/barlow-semi-condensed/files/barlow-semi-condensed-latin-500-normal.woff2)}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:#F2E8DC;position:relative;overflow:hidden;font-family:Barl}
.g{position:absolute;left:24px;right:24px;top:24px;height:880px;display:grid;grid-template-columns:1fr 1fr;gap:14px}
.g div{background:#fff center/cover no-repeat}
.live{position:absolute;top:48px;left:48px;display:flex;align-items:center;gap:10px;background:#B3261E;color:#fff;font-weight:500;font-size:24px;letter-spacing:.18em;padding:10px 20px}
.live:before{content:'';width:12px;height:12px;border-radius:50%;background:#fff}
.selo{position:absolute;top:40px;right:48px;width:96px;opacity:.9}
.p{position:absolute;left:0;right:0;bottom:0;height:422px;background:#2A1E16;color:#F4EADD;padding:46px 64px 0;display:flex;justify-content:space-between}
.t{font-family:Corm;font-weight:300;font-size:92px;line-height:.9}.t i{font-style:italic;font-weight:400;color:#D2A86E}
.n{margin-top:24px;font-weight:300;font-size:26px;letter-spacing:.12em;text-transform:uppercase;color:#D9CBB8;max-width:520px;line-height:1.4}
.o{margin-top:16px;display:inline-block;border:1.5px solid #C29A62;color:#D2A86E;font-weight:500;font-size:22px;letter-spacing:.14em;padding:8px 16px}
.pr{text-align:right;padding-top:6px}.pa{font-weight:300;font-size:28px;letter-spacing:.06em}
.v{font-family:Corm;font-weight:500;font-size:150px;line-height:.9;color:#fff;font-variant-numeric:lining-nums}.v small{font-size:60px;vertical-align:top;line-height:1.7;margin-right:6px}
.av{font-weight:500;font-size:26px;letter-spacing:.24em;color:#D2A86E}
.cta{position:absolute;left:0;right:0;bottom:38px;text-align:center;font-weight:500;font-size:24px;letter-spacing:.14em;color:#D2A86E}
</style></head><body>
<div class="g" style="${f2?'':'grid-template-columns:1fr'}"><div style="background-image:url('file://${f1}');${f2?'':'background-size:contain'}"></div>${f2?`<div style="background-image:url('file://${f2}')"></div>`:''}</div>
<div class="live">${it.badge||"LIVE 11.11"}</div><img class="selo" src="file:///home/claude/mh-automacao/marca/selo_branco.png" style="filter:drop-shadow(0 1px 4px rgba(0,0,0,.4))">
<div class="p"><div><div class="t">${it.titulo||"Live <i>11.11</i>"}</div><div class="n">${it.nome}<br>${it.material||"Folheado a ouro 18k"}<br><span style="color:#D2A86E;font-weight:500">CÓD. ${it.cod_txt||it.codigo}</span></div>${it.obs?`<div class="o">${it.obs}</div>`:''}</div>
<div class="pr"><div class="pa">por apenas</div><div class="v"><small>R$</small>${it.preco||"11,00"}</div><div class="av">À VISTA</div></div>
<div class="cta">${it.cta||"SÓ NA LIVE · CHAME A GENTE NO PRIVADO E GARANTA A SUA"}</div></div></body></html>`;
 const hf=path.join(out,'_t.html'); fs.writeFileSync(hf,html);
 const p=await b.newPage({viewport:{width:1080,height:1350}}); await p.goto('file://'+hf); await p.waitForTimeout(400);
 await p.screenshot({path:path.join(out,it.codigo+'.jpg'),type:'jpeg',quality:90}); await p.close(); console.log('ok',it.codigo);}
await b.close();})();
