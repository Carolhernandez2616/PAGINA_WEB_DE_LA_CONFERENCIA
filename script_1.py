
import os, shutil

base = '/home/user/output'
img_src = '/home/user'

# Copy all 8 images to output folder
for i in range(1, 9):
    src = f'{img_src}/IMAGEN{i}.jpg'
    dst = f'{base}/IMAGEN{i}.jpg'
    shutil.copy2(src, dst)
    print(f'Copied IMAGEN{i}.jpg -> {os.path.getsize(dst)} bytes')

# Now update index.html to replace img-card placeholders with real images
with open(f'{base}/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Image captions / alt texts
captions_es = [
    "Con el conferencista Gabriel Alzate – Colombia 5.0",
    "¿Para qué se usa la IA en una empresa?",
    "Taller práctico – Agentes de IA en acción",
    "Horizontes de Tiempo en IA – Midiendo la Frontera",
    "Agentes de IA – Taller de Alto Impacto",
    "Talento Local – Colombia 5.0",
    "Presentación de tecnología en el evento",
    "Presentación Colombia 5.0 – @gabalzate"
]
captions_en = [
    "With speaker Gabriel Alzate – Colombia 5.0",
    "How is AI used in a company?",
    "Practical workshop – AI Agents in action",
    "Time Horizons in AI – Measuring the Frontier",
    "AI Agents – High Impact Workshop",
    "Local Talent – Colombia 5.0",
    "Technology presentation at the event",
    "Colombia 5.0 Presentation – @gabalzate"
]

# Build 8 real image cards + 2 placeholder cards
image_cards_html = ''

# Card 1: large (spans 2 cols & 2 rows)
image_cards_html += f'''
      <div class="img-card" role="listitem" tabindex="0">
        <img src="IMAGEN1.jpg" alt="{captions_es[0]}" width="600" height="400" loading="lazy" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;">
        <div class="img-overlay">
          <span class="es-text">{captions_es[0]}</span>
          <span class="en-text">{captions_en[0]}</span>
        </div>
      </div>'''

for i in range(1, 8):
    extra = ' style="grid-column:3/5;"' if i == 4 else ''
    image_cards_html += f'''
      <div class="img-card" role="listitem" tabindex="0"{extra}>
        <img src="IMAGEN{i+1}.jpg" alt="{captions_es[i]}" width="400" height="300" loading="lazy" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;">
        <div class="img-overlay">
          <span class="es-text">{captions_es[i]}</span>
          <span class="en-text">{captions_en[i]}</span>
        </div>
      </div>'''

# Cards 9 and 10: placeholder
for j in [9, 10]:
    image_cards_html += f'''
      <div class="img-card" role="listitem" tabindex="0">
        <div class="img-card-label">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="3"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="m21 15-5-5L5 21"/></svg>
          <span><span class="es-text">Foto {j} – Agrega tu imagen</span><span class="en-text">Photo {j} – Add your image</span></span>
        </div>
      </div>'''

# Replace the entire img-grid-10 content
import re
html = re.sub(
    r'<div class="img-grid-10"[^>]*>.*?</div>\s*(?=\n\s*<!--)',
    f'<div class="img-grid-10" role="list" aria-label="Galería de imágenes">{image_cards_html}\n    </div>\n    ',
    html, flags=re.DOTALL
)

# Add overlay CSS
overlay_css = '''
.img-card { position: relative; overflow: hidden; min-height: 200px; }
.img-card img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; transition: transform 0.4s ease; }
.img-card:hover img { transform: scale(1.05); }
.img-overlay { position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(to top, rgba(0,0,0,0.7) 0%, transparent 100%); color: #fff; font-size: var(--text-xs); font-weight: 600; padding: var(--space-3) var(--space-4); z-index: 2; opacity: 0; transition: opacity 0.3s ease; }
.img-card:hover .img-overlay { opacity: 1; }
.img-card:focus .img-overlay { opacity: 1; }
'''

with open(f'{base}/style.css', 'a', encoding='utf-8') as f:
    f.write(overlay_css)

with open(f'{base}/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done! index.html size:", os.path.getsize(f'{base}/index.html'))
