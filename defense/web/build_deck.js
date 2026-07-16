/**
 * build_deck.js — Element-by-element HTML→PPTX converter.
 *
 * Strategy:
 *  1. Pre-render gradient background + all SVG icons to PNGs via Sharp
 *  2. Open slides.html (light theme) in Playwright
 *  3. Extract each slide's elements (text, shapes, images) scoped per-slide section
 *  4. Build PPTX via PptxGenJS — each element is a real shape/text/image
 *  5. Output: defense_deck.pptx with all 16 slides as native elements
 */
const pptxgen = require('pptxgenjs');
const { chromium } = require('playwright');
const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const SLIDE_W = 13.333;
const SLIDE_H = 7.5;
const PX_PER_IN = 96;
const PT_PER_PX = 0.75;

const SRC = __dirname;
const ASSETS = path.join(SRC, 'assets');
const TMP = path.join(SRC, '.build_tmp');
fs.mkdirSync(TMP, { recursive: true });

const COLORS = {
  ink: '0C1226', surface: 'FFFFFF', surface2: 'F3F6FC',
  line: 'E2E7F1', line2: 'D4DBE8',
  text: '0C1226', muted: '52617E', dim: '7C89A3',
  coral: 'F2622E', teal: '0E9E8E', indigo: '3552D8',
};

// ─── Icon catalog ────────────────────────────────────────────────────────────
const ICONS = {
  trend:     'M4 18 L9 8 L13 14 L20 5 M20 5 h-4 M20 5 v4',
  clock:     'M12 2 C6.48 2 2 6.48 2 12 s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z M12 7 v5 l3 3',
  nodes:     'M6 7 m-2.4 0 a2.4 2.4 0 1 1 4.8 0 a2.4 2.4 0 1 1 -4.8 0 M18 7 m-2.4 0 a2.4 2.4 0 1 1 4.8 0 a2.4 2.4 0 1 1 -4.8 0 M12 17 m-2.4 0 a2.4 2.4 0 1 1 4.8 0 a2.4 2.4 0 1 1 -4.8 0 M8 8 L11 15 M16 8 L13 15',
  heartbeat: 'M3 12 h4 l3 7 4-14 3 7 h4',
  stack:     'M3 6 h18 M3 12 h18 M3 18 h18',
  cube:      'M12 3 L5 8 L12 13 L19 8 z M5 8 v8 l7 5 7-5 V8',
  star:      'M12 3 l2.5 5 5.5 0.8 -4 3.9 0.9 5.5 L12 21 l-4.9-2.8 0.9-5.5 -4-3.9 5.5-0.8 z',
  wave:      'M4 14 c3-8 5 8 8 0 s4-6 8 0',
  chart:     'M3 20 V6 M3 20 h16 M7 20 v-6 M12 20 V9 M17 20 v-9',
};

// ─── Pre-render gradient background ──────────────────────────────────────────
async function renderBg() {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720">
    <defs>
      <linearGradient id="bg" x1="0%" y1="100%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#FBFCFE"/>
        <stop offset="55%" stop-color="#F3F6FC"/>
        <stop offset="100%" stop-color="#ECF0F8"/>
      </linearGradient>
      <radialGradient id="r1" cx="82%" cy="-10%" r="60%">
        <stop offset="0%" stop-color="rgba(53,82,216,0.10)"/>
        <stop offset="100%" stop-color="transparent"/>
      </radialGradient>
      <radialGradient id="r2" cx="-8%" cy="110%" r="50%">
        <stop offset="0%" stop-color="rgba(242,98,46,0.08)"/>
        <stop offset="100%" stop-color="transparent"/>
      </radialGradient>
    </defs>
    <rect width="1280" height="720" fill="url(#bg)"/>
    <rect width="1280" height="720" fill="url(#r1)"/>
    <rect width="1280" height="720" fill="url(#r2)"/>
  </svg>`;
  const p = path.join(TMP, 'bg.png');
  await sharp(Buffer.from(svg)).resize(640, 360).png({ compressionLevel: 9 }).toFile(p);
  return p;
}

// ─── Pre-render icons ────────────────────────────────────────────────────────
async function renderIcons() {
  const variants = [
    { name: 'coral',  bg: 'F2622E1A', fg: COLORS.coral },
    { name: 'teal',   bg: '0E9E8E1E', fg: COLORS.teal },
    { name: 'indigo', bg: '3552D81E', fg: COLORS.indigo },
    { name: 'gray',   bg: 'F3F6FC',   fg: COLORS.dim },
  ];
  const map = {};
  for (const [icName, icSvg] of Object.entries(ICONS)) {
    for (const v of variants) {
      const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="46" height="46">
        <rect x="0.5" y="0.5" width="45" height="45" rx="12" fill="#${v.bg}" stroke="#${v.fg}" stroke-opacity="0.3" stroke-width="1"/>
        <g transform="translate(10,10)" stroke="#${v.fg}" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round">${icSvg}</g>
      </svg>`;
      const key = `${icName}_${v.name}`;
      const p = path.join(TMP, `ico_${key}.png`);
      await sharp(Buffer.from(svg)).resize(69, 69).png({ compressionLevel: 9 }).toFile(p);
      map[key] = p;
    }
  }
  return map;
}

// ─── Render all inline SVGs from HTML → PNG, replace with <img> ──────────────
async function renderInlineSvgs(html) {
  let result = html;
  const regex = /<svg[^>]*>[\s\S]*?<\/svg>/gi;
  let match;
  let idx = 0;
  while ((match = regex.exec(result)) !== null) {
    const block = match[0];
    try {
      let clean = block;
      if (!clean.includes('viewBox')) {
        const w = clean.match(/width="([^"]+)"/);
        const h = clean.match(/height="([^"]+)"/);
        if (w && h) clean = clean.replace('<svg', `<svg viewBox="0 0 ${w[1]} ${h[1]}"`);
      }
      const p = path.join(TMP, `svg_${idx++}.png`);
      await sharp(Buffer.from(clean)).png({ compressionLevel: 9 }).toFile(p);
      result = result.replace(block, `<img src="file:///${p.replace(/\\/g, '/')}" />`);
    } catch (e) {
      // skip unrenderable
    }
  }
  return result;
}

// ─── Helpers ──────────────────────────────────────────────────────────────────
function pxIn(p)  { return p / PX_PER_IN; }
function ptPx(p)  { return parseFloat(p) * PT_PER_PX; }
function rgbToHex(s) {
  if (!s || s === 'transparent' || s === 'rgba(0, 0, 0, 0)') return null;
  const m = s.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
  return m ? m.slice(1).map(n => parseInt(n).toString(16).padStart(2, '0')).join('') : null;
}
function extractAlpha(s) {
  const m = s.match(/rgba\((\d+),\s*(\d+),\s*(\d+),\s*([\d.]+)\)/);
  return m ? Math.round((1 - parseFloat(m[4])) * 100) : null;
}
function parseBoxShadow(bs) {
  if (!bs || bs === 'none' || bs.includes('inset')) return null;
  const cm = bs.match(/rgba?\([^)]+\)/);
  const parts = bs.match(/([-\d.]+)(px|pt)/g);
  if (!parts || parts.length < 2) return null;
  const ox = parseFloat(parts[0]), oy = parseFloat(parts[1]);
  const blur = parts.length > 2 ? parseFloat(parts[2]) : 0;
  let angle = 0;
  if (ox !== 0 || oy !== 0) angle = (Math.atan2(oy, ox) * 180 / Math.PI + 360) % 360;
  const offset = Math.sqrt(ox*ox + oy*oy) * PT_PER_PX;
  let opacity = 0.5;
  if (cm) { const om = cm[0].match(/[\d.]+\)$/); if (om) opacity = parseFloat(om[0].replace(')', '')); }
  return { type: 'outer', angle: Math.round(angle), blur: blur * 0.75, color: cm ? rgbToHex(cm[0]) : '000000', offset, opacity };
}
function fontFace(family) {
  const name = (family || '').split(',')[0].replace(/['"]/g, '').trim().toLowerCase();
  if (name.includes('jetbrains') || name.includes('courier') || name.includes('mono')) return 'Courier New';
  return 'Arial';
}

// ─── Main ─────────────────────────────────────────────────────────────────────
async function main() {
  console.log('=== Build Defense Deck ===\n');

  console.log('1. Pre-rendering assets...');
  const [bgImg] = await Promise.all([renderBg(), renderIcons()]);
  console.log('   ✓ Background + icons done\n');

  console.log('2. Processing HTML...');
  let html = fs.readFileSync(path.join(SRC, 'slides.html'), 'utf-8');
  // Replace web fonts
  html = html.replace(/Space Grotesk/g, 'Arial').replace(/Inter/g, 'Arial').replace(/JetBrains Mono/g, 'Courier New');
  // Remove external font loads
  html = html.replace(/@import url[^;]+;/g, '').replace(/<link[^>]*fonts\.googleapis[^>]*>/gi, '');
  // Inject base font fallback
  html = html.replace('</head>', '<style>*{font-family:Arial,sans-serif}</style></head>');
  // Render inline SVGs → PNGs
  html = await renderInlineSvgs(html);
  const modPath = path.join(TMP, 'slides_modified.html');
  fs.writeFileSync(modPath, html);
  console.log('   ✓ Modified HTML written\n');

  console.log('3. Extracting elements via Playwright...');
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  await page.goto('file:///' + modPath.replace(/\\/g, '/'), { waitUntil: 'networkidle', timeout: 30000 });
  await page.evaluate(() => document.fonts.ready);
  const slideCount = await page.$$eval('.slide', els => els.length);
  console.log(`   Found ${slideCount} slides`);

  const allElements = [];
  for (let si = 0; si < slideCount; si++) {
    const data = await page.evaluate((idx) => {
      const PX = 96, PT = 0.75;
      const slides = document.querySelectorAll('.slide');
      const slide = slides[idx];
      if (!slide) return null;
      const sr = slide.getBoundingClientRect();
      const elements = [];
      const pxI = p => p / PX;
      const ptP = p => parseFloat(p) * PT;
      const r2h = s => { if (!s || s === 'transparent' || s === 'rgba(0, 0, 0, 0)') return null; const m = s.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/); return m ? m.slice(1).map(n=>parseInt(n).toString(16).padStart(2,'0')).join('') : null; };
      const extA = s => { const m = s.match(/rgba\((\d+),\s*(\d+),\s*(\d+),\s*([\d.]+)\)/); return m ? Math.round((1-parseFloat(m[4]))*100) : null; };
      const pShadow = bs => { if (!bs||bs==='none'||bs.includes('inset')) return null; const cm=bs.match(/rgba?\([^)]+\)/); const parts=bs.match(/([-\d.]+)(px|pt)/g); if(!parts||parts.length<2)return null; const ox=parseFloat(parts[0]),oy=parseFloat(parts[1]),blur=parts.length>2?parseFloat(parts[2]):0; let angle=0; if(ox||oy)angle=(Math.atan2(oy,ox)*180/Math.PI+360)%360; const offset=Math.sqrt(ox*ox+oy*oy)*PT; let op=.5; if(cm){const om=cm[0].match(/[\d.]+\)$/);if(om)op=parseFloat(om[0].replace(')',''));} return {type:'outer',angle:Math.round(angle),blur:blur*0.75,color:cm?r2h(cm[0]):'000000',offset,opacity:op}; };
      const ff = f => { const n=(f||'').split(',')[0].replace(/['"]/g,'').trim().toLowerCase(); return n.includes('jetbrains')||n.includes('courier')||n.includes('mono')?'Courier New':'Arial'; };
      const processed = new Set();

      // Process images
      slide.querySelectorAll('img').forEach(img => {
        const r = img.getBoundingClientRect();
        if (r.width>0 && r.height>0) {
          elements.push({ type:'image', src:img.currentSrc||img.src, x:pxI(r.left-sr.left), y:pxI(r.top-sr.top), w:pxI(r.width), h:pxI(r.height), z:0 });
        }
        processed.add(img);
      });

      // Process DIVs with background/border as shapes
      slide.querySelectorAll('div').forEach(div => {
        if (processed.has(div)) return;
        const r = div.getBoundingClientRect();
        if (r.width<2||r.height<2) return;
        const cs = window.getComputedStyle(div);
        const bgHex = r2h(cs.backgroundColor);
        const hasBg = bgHex && cs.backgroundColor !== 'rgba(0,0,0,0)';
        const hasBorder = parseFloat(cs.borderTopWidth)>0;
        if (!hasBg && !hasBorder) return;
        const rad = parseFloat(cs.borderRadius)||0;
        let rr = 0;
        if (rad>0) { if (cs.borderRadius.includes('%')) { rr = (rad/100)*pxI(Math.min(r.width,r.height)); } else if (cs.borderRadius.includes('pt')) { rr=rad/72; } else { rr=rad/PX; } }
        elements.push({ type:'shape', x:pxI(r.left-sr.left), y:pxI(r.top-sr.top), w:pxI(r.width), h:pxI(r.height), fillColor:bgHex, transparency:extA(cs.backgroundColor), borderColor:hasBorder?r2h(cs.borderColor):null, borderWidth:hasBorder?ptP(cs.borderTopWidth):0, rectRadius:rr, shadow:pShadow(cs.boxShadow), z:1 });
        processed.add(div);
      });

      // Process text elements
      const textTags = new Set(['P','H1','H2','H3','H4','H5','H6','LI','SPAN','STRONG','B','A','TD','TH']);
      slide.querySelectorAll('p, h1, h2, h3, h4, h5, h6, li, span, strong, b, a, td, th').forEach(el => {
        if (processed.has(el)) return;
        const text = el.textContent.trim();
        if (!text) return;
        const r = el.getBoundingClientRect();
        if (r.width<2||r.height<2) return;
        const cs = window.getComputedStyle(el);
        const fs = ptP(cs.fontSize);
        if (fs<4) return;
        let align = cs.textAlign;
        if (align==='start'||align==='end') align='left';
        elements.push({ type:'text', tag:el.tagName.toLowerCase(), text:text, x:pxI(r.left-sr.left), y:pxI(r.top-sr.top), w:pxI(r.width), h:pxI(r.height), fontSize:fs, fontFace:ff(cs.fontFamily), color:r2h(cs.color)||'0C1226', bold:parseInt(cs.fontWeight)>=600, align:align, valign:'top', lineSpacing:cs.lineHeight&&cs.lineHeight!=='normal'?ptP(cs.lineHeight):null, paddingLeft:pxI(parseFloat(cs.paddingLeft)), paddingRight:pxI(parseFloat(cs.paddingRight)), paddingTop:pxI(parseFloat(cs.paddingTop)), paddingBottom:pxI(parseFloat(cs.paddingBottom)), textTransform:cs.textTransform, letterSpacing:parseFloat(cs.letterSpacing)||0, z:2 });
        processed.add(el);
      });

      return { elements };
    }, si);

    if (data) {
      allElements.push(data.elements);
      console.log(`   Slide ${si+1}: ${data.elements.length} elements`);
    }
  }

  await browser.close();

  console.log('\n4. Building PPTX...');
  const pptx = new pptxgen();
  pptx.defineLayout({ name: 'CUSTOM', width: SLIDE_W, height: SLIDE_H });
  pptx.layout = 'CUSTOM';
  pptx.author = 'Team Paradox';
  pptx.title = 'FYDP-I Defense — Lorenz × ANN';

  for (let si = 0; si < allElements.length; si++) {
    const els = allElements[si];
    const slide = pptx.addSlide();
    slide.background = { path: bgImg };

    const sorted = els.sort((a,b) => (a.z||0)-(b.z||0));

    for (const el of sorted) {
      try {
        if (el.type === 'shape' && el.fillColor) {
          slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
            x: el.x, y: el.y, w: el.w, h: el.h,
            fill: { color: el.fillColor, transparency: el.transparency ?? 0 },
            rectRadius: el.rectRadius || 0,
            line: el.borderColor ? { color: el.borderColor, width: el.borderWidth||1 } : { width:0 },
            shadow: el.shadow || undefined,
          });
        } else if (el.type === 'image') {
          let ip = el.src;
          if (ip.startsWith('file:///')) ip = ip.slice(8);
          else if (!path.isAbsolute(ip)) { const c = path.join(ASSETS, path.basename(ip)); if (fs.existsSync(c)) ip=c; else continue; }
          if (fs.existsSync(ip)) slide.addImage({ path:ip, x:el.x, y:el.y, w:el.w, h:el.h });
        } else if (el.type === 'text' && el.text.trim()) {
          let txt = el.text;
          if (el.textTransform === 'uppercase') txt = txt.toUpperCase();
          const opts = {
            x:el.x, y:el.y, w:Math.max(el.w,0.1), h:Math.max(el.h,0.1),
            fontSize:el.fontSize, fontFace:el.fontFace||'Arial', color:el.color||'0C1226',
            bold:el.bold||false, align:el.align||'left', valign:el.valign||'top',
            margin:[el.paddingLeft||0, el.paddingRight||0, el.paddingBottom||0, el.paddingTop||0],
          };
          if (el.lineSpacing) opts.lineSpacing = el.lineSpacing;
          if (el.letterSpacing) opts.letterSpacing = el.letterSpacing;
          if (opts.margin.every(v=>v===0)) delete opts.margin;
          slide.addText(txt, opts);
        }
      } catch(e) { /* skip problematic elements */ }
    }
  }

  const outPath = path.join(SRC, 'defense_deck.pptx');
  await pptx.writeFile({ fileName: outPath });
  const sizeMB = (fs.statSync(outPath).size / 1024 / 1024).toFixed(1);
  console.log(`\n✓ Saved: ${outPath} (${sizeMB} MB, ${allElements.length} slides)`);
}

main().catch(err => { console.error('✗ Build failed:', err); process.exit(1); });
