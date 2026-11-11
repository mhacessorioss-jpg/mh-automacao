// node colagem.js <itens.json> <pasta_campanha> <saida> <catalogo.csv>
const {chromium}=require('playwright'); const fs=require('fs'); const path=require('path');
const [itensF,campD,outD,catF]=process.argv.slice(2);
const itens=JSON.parse(fs.readFileSync(itensF,'utf8'));
const cat={}; fs.readFileSync(catF,'utf8').split('\n').slice(1).forEach(l=>{const m=l.match(/^([^,]+),("?)(.*?)\2,([^,]+),([^,]+),("?)(.*?)\6,/); if(m) cat[m[1]]={nome:m[3],material:m[7]};});
const F='file://'+__dirname+'/node_modules/@fontsource';
const num=s=>parseFloat(s.replace(',','.'));
(async()=>{const b=await chromium.launch(); fs.mkdirSync(outD,{recursive:true});
for(const it of itens){
 const c=cat[it.codigo]||{}; const nome=it.nome||c.nome; const mat=it.material||c.material||'';
 const foto=path.join(campD,'fotos',it.codigo+'.png'), d1=path.join(campD,'detalhes',it.codigo+'_1.png'), d2=path.join(campD,'detalhes',it.codigo+'_2.png');
 if(![foto,d1,d2].every(fs.existsSync)){console.log('FALTA',it.codigo);continue}
 const off=0&&it.de? Math.round((1-num(it.por)/num(it.de))*100):0;
 const pos=it.pos||'center 30%';
 const html=`<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Corm;font-weight:300;src:url(${F}/cormorant-garamond/files/cormorant-garamond-latin-300-normal.woff2)}
@font-face{font-family:Corm;font-weight:500;src:url(${F}/cormorant-garamond/files/cormorant-garamond-latin-500-normal.woff2)}
@font-face{font-family:Corm;font-weight:400;font-style:italic;src:url(${F}/cormorant-garamond/files/cormorant-garamond-latin-400-italic.woff2)}
@font-face{font-family:Barl;font-weight:300;src:url(${F}/barlow-semi-condensed/files/barlow-semi-condensed-latin-300-normal.woff2)}
@font-face{font-family:Barl;font-weight:500;src:url(${F}/barlow-semi-condensed/files/barlow-semi-condensed-latin-500-normal.woff2)}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1920px;position:relative;overflow:hidden;background:#F2E8DC}
.g{position:absolute;left:14px;right:14px;top:14px;height:1426px;display:grid;grid-template-columns:640px 1fr;grid-template-rows:1fr 1fr;gap:12px}
.g div{background-size:cover;background-position:center}
.m{grid-row:1/3;background-position:${pos}!important}
.selo{position:absolute;top:44px;left:44px;width:104px;opacity:.92}
.p{position:absolute;left:0;right:0;bottom:0;height:466px;background:#2A1E16;padding:52px 64px 0;color:#F2E8DC}
.top{display:flex;justify-content:space-between;align-items:flex-start}
.bf{font-family:Corm;font-weight:300;font-size:104px;line-height:.86}.bf i{font-style:italic;font-weight:400;color:#D2A86E}
.nome{margin-top:24px;font-family:Barl;font-weight:300;font-size:24px;letter-spacing:.14em;color:#D9CBB8;text-transform:uppercase;max-width:540px;line-height:1.4}
.preco{text-align:right}
.off{display:inline-block;font-family:Barl;font-weight:500;font-size:28px;letter-spacing:.08em;background:#C29A62;color:#2A1E16;padding:8px 18px;margin-bottom:16px}
.de{font-family:Barl;font-weight:300;font-size:30px;color:#BFAE98}.por{font-family:Barl;font-weight:300;font-size:28px;margin-top:4px;letter-spacing:.06em}
.valor{font-family:Corm;font-weight:500;font-size:118px;line-height:.9;color:#fff;font-variant-numeric:lining-nums}.valor small{font-size:52px;vertical-align:top;margin-right:6px;line-height:1.6}
.cta{position:absolute;left:0;right:0;bottom:44px;text-align:center;font-family:Barl;font-weight:500;font-size:27px;letter-spacing:.14em;color:#D2A86E}
</style></head><body>
<div class="g"><div class="m" style="background-image:url('file://${foto}')"></div><div style="background-image:url('file://${d1}')"></div><div style="background-image:url('file://${d2}')"></div></div>
<img class="selo" src="file://${__dirname}/selo.png">
<div class="p"><div class="top"><div><div class="bf">Chegou <i>novidade</i></div><div class="nome">${nome}${mat?'<br>'+mat:''}<br><span style="color:#D2A86E;font-weight:500">CÓD. ${it.codigo}</span></div></div>
<div class="preco"><div class="por" style="font-size:26px;letter-spacing:.2em;color:#D2A86E">NOVA COLEÇÃO</div><div style="font-family:Corm;font-style:italic;font-size:64px;margin-top:10px;color:#fff">${it.codigo}</div></div></div></div>
<div class="cta">CHAME A GENTE NO DIRECT E GARANTA A SUA</div></div></body></html>`;
 const hf=path.join(outD,'_t.html'); fs.writeFileSync(hf,html);
 const p=await b.newPage({viewport:{width:1080,height:1920}}); await p.goto('file://'+hf); await p.waitForTimeout(600);
 const nm=it.codigo+'.jpg'; await p.screenshot({path:path.join(outD,nm),type:'jpeg',quality:92}); await p.close(); console.log('ok',nm);
} await b.close()})();
