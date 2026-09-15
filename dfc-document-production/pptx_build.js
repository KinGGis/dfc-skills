// DFC brand kit — PowerPoint (.pptx) template generator (pptxgenjs).
const pptxgen = require("pptxgenjs");
const path = require("path");
const KIT = __dirname;
const WHITE_LOGO = path.join(KIT, "assets/dfc-logo-white.png");
const EMBLEM = path.join(KIT, "assets/dfc-emblem-dark.png");

const INK="1C1C1C", GOLD="C5A253", CREAM="EFE4C8", PANEL="F2F2F0", RULE="D9D9D6",
      GREY="6E6E6E", GREEN="4A7C59", RED="A63D3D", WHITE="FFFFFF";
const FONT="Calibri";

const p = new pptxgen();
p.defineLayout({ name:"DFC", width:13.333, height:7.5 });
p.layout = "DFC";
const W=13.333, H=7.5, M=0.6;

// running header for content slides
function header(slide, sub){
  slide.addImage({ path:EMBLEM, x:M, y:0.34, w:0.42, h:0.42 });
  slide.addText("DUALFORCE CAPITAL", { isTextBox:true, x:W-5.6, y:0.34, w:5.0, h:0.24, align:"right",
    fontFace:FONT, fontSize:11, bold:true, color:INK, margin:0 });
  slide.addText(sub, { isTextBox:true, x:W-5.6, y:0.58, w:5.0, h:0.22, align:"right",
    fontFace:FONT, fontSize:9, color:GREY, margin:0 });
  // dual gold/black rule
  slide.addShape(p.ShapeType.rect, { x:M, y:0.92, w:(W-2*M)*0.42, h:0.05, fill:{color:GOLD}, line:{type:"none"} });
  slide.addShape(p.ShapeType.rect, { x:M+(W-2*M)*0.42, y:0.92, w:(W-2*M)*0.58, h:0.05, fill:{color:INK}, line:{type:"none"} });
}
function footer(slide, n){
  slide.addShape(p.ShapeType.line, { x:M, y:H-0.5, w:W-2*M, h:0, line:{color:RULE, width:0.75} });
  slide.addText("DualForce Capital Ltd  |  Confidentiel  |  DFC-NAV-DCA-2026-001", { isTextBox:true,
    x:M, y:H-0.46, w:9, h:0.28, fontFace:FONT, fontSize:9, color:GREY, margin:0, valign:"middle" });
  slide.addText(String(n), { isTextBox:true, x:W-M-1, y:H-0.46, w:1, h:0.28, align:"right",
    fontFace:FONT, fontSize:9, bold:true, color:INK, margin:0, valign:"middle" });
}
function band(slide, y, title, sub){
  slide.addShape(p.ShapeType.rect, { x:M, y, w:W-2*M, h:0.78, fill:{color:INK}, line:{type:"none"} });
  slide.addShape(p.ShapeType.rect, { x:M, y, w:0.08, h:0.78, fill:{color:GOLD}, line:{type:"none"} });
  slide.addText(title.toUpperCase(), { isTextBox:true, x:M+0.3, y:y+0.08, w:W-2*M-0.6, h:0.4,
    fontFace:FONT, fontSize:20, bold:true, color:WHITE, margin:0, valign:"middle" });
  slide.addText(sub, { isTextBox:true, x:M+0.3, y:y+0.46, w:W-2*M-0.6, h:0.26,
    fontFace:FONT, fontSize:11, color:GOLD, margin:0, valign:"middle" });
}

// ---- Slide 1: title (dark) ----
let s = p.addSlide(); s.background = { color: INK };
s.addShape(p.ShapeType.rect, { x:0, y:0, w:W*0.42, h:0.22, fill:{color:GOLD}, line:{type:"none"} });
s.addImage({ path:WHITE_LOGO, x:(W-2.2)/2, y:1.7, w:2.2, h:2.2 });
s.addText("NOTE D'ARRÊTÉ DE LA VALEUR LIQUIDATIVE", { isTextBox:true, x:1, y:4.2, w:W-2, h:1.0,
  align:"center", fontFace:FONT, fontSize:34, bold:true, color:WHITE });
s.addText("Programme d'investissement progressif · Août 2026", { isTextBox:true, x:1, y:5.25, w:W-2, h:0.5,
  align:"center", fontFace:FONT, fontSize:16, color:GOLD });
s.addText("Document confidentiel. Réservé aux souscripteurs et actionnaires autorisés de DualForce Capital Ltd.",
  { isTextBox:true, x:1, y:6.7, w:W-2, h:0.4, align:"center", fontFace:FONT, fontSize:10, color:"9A9A9A" });

// ---- Slide 2: synthèse (KPI + text) ----
s = p.addSlide(); s.background = { color: WHITE }; header(s, "Arrêté de la valeur liquidative · Août 2026");
band(s, 1.25, "1. Synthèse de l'arrêté", "Le chiffre qui engage le mois");
const kpis = [["1 051,62 £","Prix de l'action, août 2026"],["+5,162 %","Variation de la NAV sur le mois"],["3 765,18 £","NAV opérationnelle nette"]];
const cw=(W-2*M-0.6)/3;
kpis.forEach((k,i)=>{
  const x=M+i*(cw+0.3);
  s.addShape(p.ShapeType.rect, { x, y:2.35, w:cw, h:1.25, fill:{color:CREAM}, line:{type:"none"} });
  s.addText(k[0], { isTextBox:true, x, y:2.5, w:cw, h:0.6, align:"center", fontFace:FONT, fontSize:26, bold:true, color:INK, margin:0 });
  s.addText(k[1], { isTextBox:true, x, y:3.12, w:cw, h:0.4, align:"center", fontFace:FONT, fontSize:10, color:GREY, margin:0 });
});
s.addText([
  { text:"La valeur liquidative du portefeuille opérationnel est arrêtée au 31 août 2026 à ", options:{} },
  { text:"3 765,18 £", options:{ bold:true } },
  { text:", en progression de ", options:{} },
  { text:"+5,162 %", options:{ bold:true, color:GREEN } },
  { text:" sur le mois (+184,83 £), après provision des frais de gestion et neutralisation des souscriptions.", options:{} },
], { isTextBox:true, x:M, y:3.95, w:W-2*M, h:1.0, fontFace:FONT, fontSize:14, color:INK, align:"justify" });
footer(s, 1);

// ---- Slide 3: composition (table) ----
s = p.addSlide(); s.background = { color: WHITE }; header(s, "Arrêté de la valeur liquidative · Août 2026");
band(s, 1.25, "2. Composition et valorisation", "Poche par poche, aux deux dates d'arrêté");
const hdr = (t,al)=>({ text:t, options:{ fill:{color:INK}, color:WHITE, bold:true, align:al, valign:"middle", fontFace:FONT, fontSize:11 } });
function cell(t, al, opts={}){
  let color=INK, txt=t; const m=/\((pos|neg)\)$/.exec(t);
  if(m){ txt=t.replace(/\s*\((pos|neg)\)$/,""); color=m[1]==="pos"?GREEN:RED; }
  return { text:txt, options:{ align:al, valign:"middle", fontFace:FONT, fontSize:11, color, ...opts } };
}
const rowsData = [
  ["Actions (compte de courtage institutionnel)","1 747,07","1 886,01","+138,94 (pos)"],
  ["Crypto","476,83","517,22","+40,39 (pos)"],
  ["Dette privée","1 248,57","1 263,04","+14,47 (pos)"],
  ["Crowd2fund","113,97","114,61","+0,64 (pos)"],
  ["Trésorerie","-6,09","251,05","+257,14 (pos)"],
  ["Actif total|T","3 580,35|T","4 031,93|T","+451,58|T"],
  ["Provision de frais de gestion","—","-9,52","-9,52 (neg)"],
  ["Souscriptions du programme","—","-257,23","-257,23 (neg)"],
  ["NAV opérationnelle nette|T","3 580,35|T","3 765,18|T","+184,83 (pos)|T"],
];
const rows = [[ hdr("Poche","left"), hdr("31/07/2026 (£)","right"), hdr("31/08/2026 (£)","right"), hdr("Variation (£)","right") ]];
rowsData.forEach((r,idx)=>{
  const isTotal = r[0].endsWith("|T");
  const clean = r.map(c=>c.replace(/\|T$/,""));
  const fill = isTotal ? CREAM : (idx%2===1?PANEL:WHITE);
  rows.push([
    cell(clean[0],"left",{fill:{color:fill}, bold:isTotal}),
    cell(clean[1],"right",{fill:{color:fill}, bold:isTotal}),
    cell(clean[2],"right",{fill:{color:fill}, bold:isTotal}),
    cell(clean[3],"right",{fill:{color:fill}, bold:isTotal}),
  ]);
});
s.addTable(rows, { x:M, y:2.35, w:W-2*M, colW:[5.7,2.14,2.14,2.15],
  border:{ type:"solid", color:RULE, pt:0.5 }, rowH:0.36, valign:"middle", margin:[2,6,2,6] });
footer(s, 2);

p.writeFile({ fileName: path.join(KIT,"out/DFC_gabarit_deck.pptx") }).then(f=>console.log("OK pptx ->", f));
