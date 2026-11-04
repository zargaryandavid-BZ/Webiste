"""Generates the blog pages, sitemap.xml and robots.txt from articles.py.

Usage (from the repo root): python3 scripts/build_blog.py .
"""
import html, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from articles import ARTICLES

ROOT = sys.argv[1]
SITE = 'https://www.pulseprintautomation.com'
DATE = '2026-11-04'
DATE_LABEL = 'November 4, 2026'

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' "
           "height='32' rx='8' fill='%234f6ef7'/%3E%3Cpath d='M4 16h5l3-8 5 16 3-10 2 6h6' stroke='white' "
           "stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round' fill='none'/%3E%3C/svg%3E")

def esc(s):
    return html.escape(s, quote=True)

def read_time(body):
    words = len(re.sub(r'<[^>]+>', ' ', body).split())
    return max(1, round(words / 220))

def head(title, description, url, image, og_type, ld):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}" />
  <meta name="robots" content="index, follow, max-image-preview:large" />
  <link rel="canonical" href="{url}" />
  <meta name="theme-color" content="#06060e" />
  <meta property="og:site_name" content="Pulse Print" />
  <meta property="og:type" content="{og_type}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:title" content="{esc(title)}" />
  <meta property="og:description" content="{esc(description)}" />
  <meta property="og:image" content="{SITE}/{image}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{esc(title)}" />
  <meta name="twitter:description" content="{esc(description)}" />
  <meta name="twitter:image" content="{SITE}/{image}" />
  <link rel="icon" type="image/svg+xml" href="{FAVICON}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/blog/blog.css" />
  <script type="application/ld+json">
{json.dumps(ld, indent=2, ensure_ascii=False)}
  </script>
</head>
<body>

<nav class="blog-nav">
  <a href="/" class="nav-logo" aria-label="Pulse Print home">
    <div class="pulse-icon">
      <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M2 10h3l2-6 4 12 2-8 1.5 4H18" stroke="white" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </div>
    Pulse Print <span class="nav-tag">AI</span>
  </a>
  <ul>
    <li><a href="/#modules">Platform</a></li>
    <li><a href="/#ai">Pulse AI</a></li>
    <li><a href="/blog" aria-current="page">Blog</a></li>
  </ul>
  <a href="/#contact" class="btn">Request a Demo</a>
</nav>
'''

FOOTER = '''
<footer class="blog-footer">
  <span>© 2026 Pulse Print · AI print shop automation software</span>
  <ul>
    <li><a href="/">Home</a></li>
    <li><a href="/#modules">Platform</a></li>
    <li><a href="/blog">Blog</a></li>
    <li><a href="/#contact">Request Demo</a></li>
  </ul>
</footer>

</body>
</html>
'''

def card(a, heading='h2'):
    return f'''    <a class="post-card" href="/blog/{a['slug']}">
      <img src="/{a['image']}" alt="{esc(a['alt'])}" width="{a['w']}" height="{a['h']}" loading="lazy" decoding="async" />
      <div class="post-card-body">
        <span class="tag">{esc(a['tag'])}</span>
        <{heading}>{esc(a['title'])}</{heading}>
        <p>{esc(a['subtitle'])}</p>
        <div class="post-meta"><time datetime="{DATE}">{DATE_LABEL}</time><span>·</span><span>{read_time(a['body'])} min read</span></div>
      </div>
    </a>'''

org = {'@type': 'Organization', 'name': 'Pulse Print', 'url': SITE + '/'}

def article_page(a):
    url = f"{SITE}/blog/{a['slug']}"
    ld = {
        '@context': 'https://schema.org',
        '@graph': [
            {
                '@type': 'BlogPosting',
                'headline': a['title'],
                'description': a['description'],
                'image': f"{SITE}/{a['image']}",
                'datePublished': DATE,
                'dateModified': DATE,
                'author': org,
                'publisher': org,
                'mainEntityOfPage': url,
            },
            {
                '@type': 'BreadcrumbList',
                'itemListElement': [
                    {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE + '/'},
                    {'@type': 'ListItem', 'position': 2, 'name': 'Blog', 'item': SITE + '/blog'},
                    {'@type': 'ListItem', 'position': 3, 'name': a['title'], 'item': url},
                ],
            },
        ],
    }
    i = ARTICLES.index(a)
    related = [ARTICLES[(i + k) % len(ARTICLES)] for k in (1, 2, 3)]
    return head(a['seo_title'], a['description'], url, a['image'], 'article', ld) + f'''
<main>
  <article class="article">
    <nav class="crumbs" aria-label="Breadcrumb">
      <ol>
        <li><a href="/">Home</a></li>
        <li><a href="/blog">Blog</a></li>
        <li aria-current="page">{esc(a['tag'])}</li>
      </ol>
    </nav>
    <header>
      <span class="tag">{esc(a['tag'])}</span>
      <h1>{esc(a['title'])}</h1>
      <p class="subtitle">{esc(a['subtitle'])}</p>
      <div class="post-meta"><span>By the Pulse Print team</span><span>·</span><time datetime="{DATE}">{DATE_LABEL}</time><span>·</span><span>{read_time(a['body'])} min read</span></div>
    </header>
    <figure class="hero-figure">
      <img src="/{a['image']}" alt="{esc(a['alt'])}" width="{a['w']}" height="{a['h']}" fetchpriority="high" />
      <figcaption>{esc(a['caption'])}</figcaption>
    </figure>
    <div class="prose">
{a['body'].strip()}
    </div>
    <aside class="cta-box">
      <h2>See Pulse Print in action</h2>
      <p>AI print shop automation software for small and mid-size print shops. Live demo in 30 minutes.</p>
      <a href="/#contact" class="btn">Request a Demo</a>
    </aside>
  </article>

  <section class="related" aria-labelledby="related-title">
    <h2 id="related-title">Keep reading</h2>
    <div class="post-grid">
{chr(10).join(card(r, 'h3') for r in related)}
    </div>
  </section>
</main>
''' + FOOTER

def index_page():
    url = f"{SITE}/blog"
    ld = {
        '@context': 'https://schema.org',
        '@type': 'Blog',
        'name': 'Pulse Print Blog',
        'url': url,
        'publisher': org,
        'blogPost': [{'@type': 'BlogPosting', 'headline': a['title'], 'url': f"{SITE}/blog/{a['slug']}",
                      'datePublished': DATE} for a in ARTICLES],
    }
    return head('Print Shop Automation & AI Blog | Pulse Print',
                'Guides on print shop automation software, AI for print shops and print shop management software: cut waste, raise throughput and know your numbers.',
                url, ARTICLES[0]['image'], 'website', ld) + f'''
<main>
  <header class="blog-hero">
    <span class="label">Pulse Print Blog</span>
    <h1>Print shop automation, AI and management: practical guides</h1>
    <p>How small and mid-size print shops use automation and AI to cut waste, raise throughput and know their numbers.</p>
  </header>
  <section class="post-grid" aria-label="Articles">
{chr(10).join(card(a) for a in ARTICLES)}
  </section>
</main>
''' + FOOTER

os.makedirs(os.path.join(ROOT, 'blog'), exist_ok=True)
for a in ARTICLES:
    with open(os.path.join(ROOT, 'blog', a['slug'] + '.html'), 'w') as f:
        f.write(article_page(a))
with open(os.path.join(ROOT, 'blog', 'index.html'), 'w') as f:
    f.write(index_page())

urls = [(SITE + '/', '1.0'), (SITE + '/blog', '0.8')] + [(f"{SITE}/blog/{a['slug']}", '0.7') for a in ARTICLES]
with open(os.path.join(ROOT, 'sitemap.xml'), 'w') as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for u, pr in urls:
        f.write(f'  <url><loc>{u}</loc><lastmod>{DATE}</lastmod><priority>{pr}</priority></url>\n')
    f.write('</urlset>\n')
with open(os.path.join(ROOT, 'robots.txt'), 'w') as f:
    f.write(f'User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {SITE}/sitemap.xml\n')

print('built', len(ARTICLES), 'articles')
for a in ARTICLES:
    print(f"  {a['slug']}: {read_time(a['body'])} min, title {len(a['seo_title'])} chars, description {len(a['description'])} chars")
