// DFC brand kit — Word (.docx) template generator (docx-js).
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell,
  WidthType, BorderStyle, ShadingType, AlignmentType, PageNumber, Header, Footer,
  TabStopType, VerticalAlign, TableLayoutType, PageOrientation
} = require("docx");

const KIT = __dirname;
const white = fs.readFileSync(path.join(KIT, "assets/dfc-logo-white.png"));
const emblem = fs.readFileSync(path.join(KIT, "assets/dfc-emblem-dark.png"));

// palette
const INK="1C1C1C", GOLD="C5A253", CREAM="EFE4C8", PANEL="F2F2F0", RULE="D9D9D6",
      GREY="6E6E6E", GREEN="4A7C59", RED="A63D3D", WHITE="FFFFFF";
const FONT="Calibri";

const A4W=11906, A4H=16838;

// ---------- COVER (section 1, margins 0, full-page dark table) ----------
const coverCell = new TableCell({
  shading: { type: ShadingType.CLEAR, color: "auto", fill: INK },
  verticalAlign: VerticalAlign.CENTER,
  margins: { top: 900, bottom: 900, left: 1400, right: 1400 },
  width: { size: A4W, type: WidthType.DXA },
  borders: noBorders(INK),
  children: [
    new Paragraph({ alignment: AlignmentType.CENTER, spacing:{after:500},
      children:[ new ImageRun({ type:"png", data: white, transformation:{ width:150, height:150 } }) ]}),
    center("NOTE D'ARRÊTÉ", 30, WHITE, true),
    center("DE LA VALEUR LIQUIDATIVE", 30, WHITE, true),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing:{before:260, after:700},
      children:[ new TextRun({ text:"Programme d'investissement progressif · Août 2026", font:FONT, size:26, color:GOLD }) ]}),
    ...coverKV([
      ["Émetteur","DualForce Capital Ltd, société de droit britannique"],
      ["Date d'arrêté","31 août 2026"],
      ["Devise de référence","Livre sterling (GBP)"],
      ["Classification","Confidentiel"],
      ["Référence","DFC-NAV-DCA-2026-001"],
    ]),
  ],
});
const coverTable = new Table({
  width:{ size:A4W, type:WidthType.DXA },
  columnWidths:[A4W],
  layout: TableLayoutType.FIXED,
  borders: noBorders(INK),
  rows:[ new TableRow({ height:{ value: A4H-20, rule:"atLeast" }, children:[coverCell] }) ],
});

function noBorders(c){ const b={style:BorderStyle.SINGLE,size:1,color:c};
  return {top:b,bottom:b,left:b,right:b,insideHorizontal:b,insideVertical:b}; }
function center(t,size,color,bold){ return new Paragraph({ alignment:AlignmentType.CENTER, spacing:{after:60},
  children:[ new TextRun({ text:t, font:FONT, size:size*2, color, bold:!!bold, allCaps:false }) ]}); }
function coverKV(rows){
  return rows.map(([k,v]) => new Paragraph({
    spacing:{after:90},
    border:{ left:{ style:BorderStyle.SINGLE, size:28, color:GOLD, space:10 } },
    tabStops:[{ type:TabStopType.LEFT, position:3200 }],
    children:[
      new TextRun({ text:k, font:FONT, size:20, bold:true, color:GOLD }),
      new TextRun({ text:"\t"+v, font:FONT, size:20, color:"E9E9E9" }),
    ],
  }));
}

// ---------- CONTENT helpers (section 2) ----------
function sectionBand(title, sub){
  return new Paragraph({
    shading:{ type:ShadingType.CLEAR, color:"auto", fill:INK },
    border:{ left:{ style:BorderStyle.SINGLE, size:34, color:GOLD, space:14 } },
    spacing:{ before:260, after:0 },
    children:[ new TextRun({ text:title.toUpperCase(), font:FONT, size:28, bold:true, color:WHITE }) ],
  });
}
function sectionSub(sub){
  return new Paragraph({
    shading:{ type:ShadingType.CLEAR, color:"auto", fill:INK },
    border:{ left:{ style:BorderStyle.SINGLE, size:34, color:GOLD, space:14 } },
    spacing:{ before:0, after:200 },
    children:[ new TextRun({ text:sub, font:FONT, size:18, color:GOLD }) ],
  });
}
function body(runs){ return new Paragraph({ alignment:AlignmentType.JUSTIFIED, spacing:{after:140},
  children: runs.map(r => new TextRun({ text:r.t, bold:r.b, color:r.c||INK, font:FONT, size:21 })) }); }
function retain(title, text){
  const sh={ type:ShadingType.CLEAR, color:"auto", fill:CREAM };
  const bd={ left:{ style:BorderStyle.SINGLE, size:34, color:GOLD, space:14 } };
  return [
    new Paragraph({ shading:sh, border:bd, spacing:{before:60,after:0},
      children:[ new TextRun({ text:title, bold:true, font:FONT, size:20, color:INK }) ]}),
    new Paragraph({ shading:sh, border:bd, alignment:AlignmentType.JUSTIFIED, spacing:{before:40,after:120},
      children:[ new TextRun({ text:text, font:FONT, size:19, color:INK }) ]}),
  ];
}

// KPI band: 3 columns cream
function kpiBand(items){
  const w = Math.floor(9026/3);
  const cell = (val,lbl) => new TableCell({
    shading:{ type:ShadingType.CLEAR, color:"auto", fill:CREAM },
    verticalAlign:VerticalAlign.CENTER, width:{size:w,type:WidthType.DXA}, borders:noBorders(CREAM),
    margins:{top:200,bottom:200,left:120,right:120},
    children:[
      new Paragraph({ alignment:AlignmentType.CENTER, spacing:{after:40}, children:[ new TextRun({ text:val, bold:true, font:FONT, size:40, color:INK }) ]}),
      new Paragraph({ alignment:AlignmentType.CENTER, children:[ new TextRun({ text:lbl, font:FONT, size:17, color:GREY }) ]}),
    ],
  });
  return new Table({ width:{size:9026,type:WidthType.DXA}, columnWidths:[w,w,w], layout:TableLayoutType.FIXED,
    borders:noBorders(CREAM), rows:[ new TableRow({ children: items.map(i=>cell(i[0],i[1])) }) ] });
}

// data table
function dataTable(cols, widths, rows){
  const headerCell = (t,align) => new TableCell({ shading:{type:ShadingType.CLEAR,color:"auto",fill:INK}, borders:cellBorders(),
    margins:{top:80,bottom:80,left:140,right:140},
    children:[ new Paragraph({ alignment: align==="num"?AlignmentType.RIGHT:AlignmentType.LEFT,
      children:[ new TextRun({ text:t, bold:true, color:WHITE, font:FONT, size:19 }) ]}) ]});
  const headRow = new TableRow({ tableHeader:true, children: cols.map((c,i)=>headerCell(c, widths.align[i])) });
  const bodyRows = rows.map((r, idx) => {
    const isTotal = r.total;
    const fill = isTotal ? CREAM : (idx%2===1 ? PANEL : WHITE);
    return new TableRow({ children: r.cells.map((cell,i)=>{
      const align = widths.align[i];
      let color = INK; let txt = cell;
      const m = /\((pos|neg)\)$/.exec(cell);
      if(m){ txt = cell.replace(/\s*\((pos|neg)\)$/,""); color = m[1]==="pos"?GREEN:RED; }
      return new TableCell({ shading:{type:ShadingType.CLEAR,color:"auto",fill}, borders:cellBorders(),
        margins:{top:70,bottom:70,left:140,right:140},
        children:[ new Paragraph({ alignment: align==="num"?AlignmentType.RIGHT:AlignmentType.LEFT,
          children:[ new TextRun({ text:txt, bold:isTotal, color, font:FONT, size:19 }) ]}) ]});
    })});
  });
  return new Table({ width:{size:9026,type:WidthType.DXA}, columnWidths:widths.cols, layout:TableLayoutType.FIXED,
    borders:cellBorders(), rows:[headRow, ...bodyRows] });
}
function cellBorders(){ const n={style:BorderStyle.NONE,size:0,color:"FFFFFF"};
  const b={style:BorderStyle.SINGLE,size:2,color:RULE};
  return {top:n,bottom:b,left:n,right:n,insideHorizontal:b,insideVertical:n}; }

// ---------- header / footer ----------
const header = new Header({ children:[
  new Paragraph({
    tabStops:[{ type:TabStopType.RIGHT, position:9026 }],
    border:{ bottom:{ style:BorderStyle.SINGLE, size:12, color:GOLD, space:6 } },
    spacing:{ after:120 },
    children:[
      new ImageRun({ type:"png", data:emblem, transformation:{ width:34, height:34 } }),
      new TextRun({ text:"\tDUALFORCE CAPITAL", bold:true, font:FONT, size:18, color:INK }),
    ],
  }),
  new Paragraph({ alignment:AlignmentType.RIGHT, spacing:{after:80},
    children:[ new TextRun({ text:"Arrêté de la valeur liquidative · Août 2026", font:FONT, size:15, color:GREY }) ]}),
]});
const footer = new Footer({ children:[
  new Paragraph({
    tabStops:[{ type:TabStopType.RIGHT, position:9026 }],
    border:{ top:{ style:BorderStyle.SINGLE, size:4, color:RULE, space:6 } },
    children:[
      new TextRun({ text:"DualForce Capital Ltd  |  Confidentiel  |  DFC-NAV-DCA-2026-001", font:FONT, size:15, color:GREY }),
      new TextRun({ text:"\t", font:FONT, size:15 }),
      new TextRun({ children:[PageNumber.CURRENT], bold:true, font:FONT, size:15, color:INK }),
    ],
  }),
]});

// ---------- content ----------
const content = [
  sectionBand("1. Synthèse de l'arrêté"), sectionSub("Le chiffre qui engage le mois"),
  new Paragraph({ spacing:{after:120}, children:[new TextRun({text:"",size:2})] }),
  kpiBand([["1 051,62 £","Prix de l'action, août 2026"],["+5,162 %","Variation de la NAV sur le mois"],["3 765,18 £","NAV opérationnelle nette"]]),
  new Paragraph({ spacing:{after:120}, children:[new TextRun({text:"",size:2})] }),
  body([{t:"La valeur liquidative du portefeuille opérationnel de DualForce Capital Ltd est arrêtée au 31 août 2026 à "},{t:"3 765,18 £",b:true},{t:", contre 3 580,35 £ au 31 juillet 2026. La progression du mois s'établit à "},{t:"+5,162 %",b:true,c:GREEN},{t:", soit +184,83 £, après provision des frais de gestion et neutralisation des souscriptions."}]),
  ...retain("Ce qu'il faut retenir","La performance du mois provient très majoritairement de la poche Actions, qui progresse de 7,95 % et apporte 138,94 £ sur les 184,83 £ de variation. Les poches de portage délivrent leur coupon sans incident de crédit."),
  sectionBand("2. Composition et valorisation"), sectionSub("Poche par poche, aux deux dates d'arrêté"),
  new Paragraph({ spacing:{after:120}, children:[new TextRun({text:"",size:2})] }),
  dataTable(
    ["Poche","31/07/2026 (£)","31/08/2026 (£)","Variation (£)"],
    { cols:[3626,1800,1800,1800], align:["left","num","num","num"] },
    [
      {cells:["Actions (compte de courtage institutionnel)","1 747,07","1 886,01","+138,94 (pos)"]},
      {cells:["Crypto","476,83","517,22","+40,39 (pos)"]},
      {cells:["Dette privée","1 248,57","1 263,04","+14,47 (pos)"]},
      {cells:["Crowd2fund","113,97","114,61","+0,64 (pos)"]},
      {cells:["Trésorerie","-6,09","251,05","+257,14 (pos)"]},
      {cells:["Actif total","3 580,35","4 031,93","+451,58"],total:true},
      {cells:["Provision de frais de gestion","—","-9,52","-9,52 (neg)"]},
      {cells:["Souscriptions du programme","—","-257,23","-257,23 (neg)"]},
      {cells:["NAV opérationnelle nette","3 580,35","3 765,18","+184,83 (pos)"],total:true},
    ]
  ),
];

const doc = new Document({
  styles:{ default:{ document:{ run:{ font:FONT, size:21, color:INK } } } },
  sections:[
    { properties:{ page:{ size:{ width:A4W, height:A4H }, margin:{ top:0,bottom:0,left:0,right:0 } } },
      children:[ coverTable ] },
    { properties:{ page:{ size:{ width:A4W, height:A4H }, margin:{ top:1700,bottom:1200,left:1440,right:1440 } } },
      headers:{ default:header }, footers:{ default:footer },
      children: content },
  ],
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(path.join(KIT,"out/DFC_gabarit_note.docx"), buf);
  console.log("OK docx ->", path.join(KIT,"out/DFC_gabarit_note.docx"));
});
