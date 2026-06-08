
import os, shutil, re

base = '/home/user/output'
os.makedirs(base, exist_ok=True)

# Rebuild index.html from html_content with all fixes
html = html_content

# Remove second conference card
conf2_pos = html.find('<!-- CONFERENCE 2 -->')
if conf2_pos != -1:
    close_pattern = '\n    </div>\n  </div>\n</section>'
    close_pos = html.find(close_pattern, conf2_pos)
    inner_close = html.rfind('</div>', conf2_pos, close_pos)
    html = html[:conf2_pos] + html[inner_close+6:]

html = html.replace('class="conference-grid"', 'class="conference-grid single-conference"')

# Build CSS
css_match = re.search(r'<style>(.*?)</style>', html, re.DOTALL)
js_match = re.search(r'<script>(.*?)</script>', html, re.DOTALL)
css_code = css_match.group(1).strip() if css_match else ""
js_code = js_match.group(1).strip() if js_match else ""

# Color replacements
replacements = {
    '#f0f4f8':'#fff8ef','#ffffff':'#fffdf9','#f7fafc':'#fff6ea',
    '#e8edf3':'#f6ead8','#d0d9e4':'#ead9c2','#c4d0de':'#e2cfb3',
    '#1a2332':'#2b1d0e','#4a5a6e':'#7b6247','#8a9bb0':'#b89f86',
    '#1b4f8a':'#0d5c63','#163f6e':'#08484e','#0f2d50':'#063338',
    '#d6e4f5':'#d9f0ea','#e8a020':'#d97706','#c8861a':'#b85f00',
    '#fdf3dc':'#ffedd5','#2563a8':'#0f766e','#1a6e3e':'#2f855a',
    '#0d1520':'#14100d','#111b2b':'#1d1814','#162235':'#241d18',
    '#1a2840':'#2c241d','#1e3050':'#3a2d22','#263d60':'#4b3929',
    '#d4dfe8':'#f4ede4','#7a95b0':'#c9b49a','#4a6280':'#8d765f',
    '#5b9bd5':'#38b2ac','#4a84bf':'#2c9d96','#1a2d45':'#163632',
    '#f0b340':'#f59e0b','#d89a30':'#d97706','#2a2010':'#3a2815'
}
for old, new in replacements.items():
    css_code = css_code.replace(old, new)

css_code += '''
.hero{background:radial-gradient(circle at 20% 20%,rgba(245,158,11,0.22),transparent 26%),radial-gradient(circle at 80% 15%,rgba(56,178,172,0.18),transparent 24%),linear-gradient(135deg,#0d5c63 0%,#0f766e 45%,#7c4a03 100%);}
.single-conference{grid-template-columns:1fr!important;}
.single-conference .conference-card{max-width:860px;margin-inline:auto;}
.conference-card p+p{margin-top:var(--space-3);}
.theme-toggle{width:40px;height:40px;display:flex;align-items:center;justify-content:center;border-radius:var(--radius-full);color:var(--color-text)!important;background:var(--color-surface-offset);border:1px solid var(--color-border);transition:all var(--transition);}
.theme-toggle:hover{background:var(--color-primary-light);color:var(--color-primary)!important;border-color:var(--color-primary);}
.img-card{position:relative;overflow:hidden;min-height:200px;}
.img-card img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform 0.4s ease;}
.img-card:hover img{transform:scale(1.05);}
.img-overlay{position:absolute;bottom:0;left:0;right:0;background:linear-gradient(to top,rgba(0,0,0,0.7) 0%,transparent 100%);color:#fff;font-size:var(--text-xs);font-weight:600;padding:var(--space-3) var(--space-4);z-index:2;opacity:0;transition:opacity 0.3s ease;}
.img-card:hover .img-overlay,.img-card:focus .img-overlay{opacity:1;}
.footer-brand p{color:rgba(255,255,255,0.75)!important;}
'''

# Fix JS
js_code = '''(function(){
  var t=document.querySelector('[data-theme-toggle]');
  var r=document.documentElement;
  var d=matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light';
  r.setAttribute('data-theme',d);
  var sun='<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>';
  var moon='<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
  if(t){t.innerHTML=d==='dark'?sun:moon;t.addEventListener('click',function(){d=d==='dark'?'light':'dark';r.setAttribute('data-theme',d);t.innerHTML=d==='dark'?sun:moon;});}
})();

function setLang(lang){
  document.body.className='lang-'+lang;
  document.documentElement.setAttribute('lang',lang);
  document.getElementById('btn-es').classList.toggle('active',lang==='es');
  document.getElementById('btn-en').classList.toggle('active',lang==='en');
}

document.addEventListener('DOMContentLoaded',function(){
  setLang('es');
  var menuBtn=document.getElementById('menu-btn');
  var navLinks=document.getElementById('nav-links');
  if(menuBtn&&navLinks){
    menuBtn.addEventListener('click',function(){var open=navLinks.classList.toggle('open');menuBtn.setAttribute('aria-expanded',open);});
    navLinks.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){navLinks.classList.remove('open');menuBtn.setAttribute('aria-expanded','false');});});
  }
  var observer=new IntersectionObserver(function(entries){entries.forEach(function(e){if(e.isIntersecting)e.target.classList.add('visible');});},{threshold:0.1});
  document.querySelectorAll('.fade-in').forEach(function(el){observer.observe(el);});
});
'''

# Build image gallery
captions_es = ["Con Gabriel Alzate – Colombia 5.0","¿Para qué se usa la IA?","Taller práctico – Agentes de IA","Horizontes de Tiempo en IA","Agentes de IA – Taller Alto Impacto","Talento Local – Colombia 5.0","Presentación del evento","Colombia 5.0 – @gabalzate"]
captions_en = ["With Gabriel Alzate – Colombia 5.0","How is AI used in business?","Practical workshop – AI Agents","Time Horizons in AI","AI Agents – High Impact Workshop","Local Talent – Colombia 5.0","Event presentation","Colombia 5.0 – @gabalzate"]

img_cards = '\n'
img_cards += f'      <div class="img-card" role="listitem" tabindex="0"><img src="IMAGEN1.jpg" alt="{captions_es[0]}" width="600" height="400" loading="lazy"><div class="img-overlay"><span class="es-text">{captions_es[0]}</span><span class="en-text">{captions_en[0]}</span></div></div>\n'
for i in range(1,8):
    extra = ' style="grid-column:3/5;"' if i==4 else ''
    img_cards += f'      <div class="img-card" role="listitem" tabindex="0"{extra}><img src="IMAGEN{i+1}.jpg" alt="{captions_es[i]}" width="400" height="300" loading="lazy"><div class="img-overlay"><span class="es-text">{captions_es[i]}</span><span class="en-text">{captions_en[i]}</span></div></div>\n'
# 2 placeholder cards
for j in [9,10]:
    img_cards += f'      <div class="img-card" role="listitem" tabindex="0"><div class="img-card-label"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="3"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="m21 15-5-5L5 21"/></svg><span><span class="es-text">Foto {j} – Agrega tu imagen</span><span class="en-text">Photo {j} – Add your image</span></span></div></div>\n'

html = re.sub(
    r'<div class="img-grid-10"[^>]*>.*?</div>\s*(?=\n\s*<!--|\n\s*<div class="video)',
    f'<div class="img-grid-10" role="list" aria-label="Galería de imágenes">{img_cards}    </div>\n    ',
    html, flags=re.DOTALL
)

# Build final separated files
clean_html = re.sub(r'<style>.*?</style>', '<link rel="stylesheet" href="style.css">', html, flags=re.DOTALL)
clean_html = re.sub(r'<script>.*?</script>', '<script src="script.js"></script>', clean_html, flags=re.DOTALL)

with open(f'{base}/index.html','w',encoding='utf-8') as f: f.write(clean_html)
with open(f'{base}/style.css','w',encoding='utf-8') as f: f.write(css_code)
with open(f'{base}/script.js','w',encoding='utf-8') as f: f.write(js_code)

# Copy images
import glob
for img in glob.glob('/home/user/IMAGEN*.jpg'):
    shutil.copy2(img, base)

for fn in ['index.html','style.css','script.js']:
    print(fn, os.path.getsize(f'{base}/{fn}'), 'bytes ✅')
