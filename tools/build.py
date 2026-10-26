"""Builds the static Lichi site (Ukrainian at the root, English under /en/) for GitHub Pages."""
import html
import re
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent
BASE = 'https://excrapt.github.io/lichi/'
EMAIL = 'lichisupport@gmail.com'
INSTAGRAM = 'https://www.instagram.com/lichi_app/'
UPDATED = {'uk': '26 жовтня 2026 р.', 'en': 'October 26, 2026'}
EULA = 'https://www.apple.com/legal/internet-services/itunes/dev/stdeula/'

T = {
    'uk': {
        'nav_support': 'Підтримка', 'nav_privacy': 'Конфіденційність', 'nav_terms': 'Умови',
        'other_lang': 'English', 'other_code': 'en',
        'foot_privacy': 'Політика конфіденційності', 'foot_terms': 'Умови використання', 'foot_support': 'Підтримка',
        'updated': 'Оновлено', 'skip': 'Перейти до змісту',
    },
    'en': {
        'nav_support': 'Support', 'nav_privacy': 'Privacy', 'nav_terms': 'Terms',
        'other_lang': 'Українська', 'other_code': 'uk',
        'foot_privacy': 'Privacy Policy', 'foot_terms': 'Terms of Use', 'foot_support': 'Support',
        'updated': 'Updated', 'skip': 'Skip to content',
    },
}

PAGES = ['index', 'privacy', 'terms', 'support']


def href(lang, page, from_lang):
    """Relative link from a page in `from_lang` to `page` in `lang`."""
    name = '' if page == 'index' else f'{page}.html'
    if lang == from_lang:
        return name or './'
    if from_lang == 'uk' and lang == 'en':
        return f'en/{name}'
    return f'../{name}'


def abs_url(lang, page):
    name = '' if page == 'index' else f'{page}.html'
    return BASE + ('en/' if lang == 'en' else '') + name


def layout(lang, page, title, description, body):
    t = T[lang]
    other = t['other_code']
    root = '' if lang == 'uk' else '../'
    nav = [('support', t['nav_support']), ('privacy', t['nav_privacy']), ('terms', t['nav_terms'])]
    nav_html = ''.join(
        f'<a href="{href(lang, p, lang)}"{" aria-current=\"page\"" if p == page else ""}>{label}</a>' for p, label in nav
    )
    lang_html = f'<a class="lang" href="{href(other, page, lang)}" hreflang="{other}" lang="{other}">{t["other_lang"]}</a>'
    foot = (
        f'<a href="{href(lang, "support", lang)}">{t["foot_support"]}</a>'
        f'<a href="{href(lang, "privacy", lang)}">{t["foot_privacy"]}</a>'
        f'<a href="{href(lang, "terms", lang)}">{t["foot_terms"]}</a>'
        f'<a href="mailto:{EMAIL}">{EMAIL}</a>'
        f'<a class="ig-only" href="{INSTAGRAM}"><img src="{root}assets/instagram.png" alt="Instagram @lichi_app" width="24" height="24"></a>'
    )
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="canonical" href="{abs_url(lang, page)}">
<link rel="alternate" hreflang="uk" href="{abs_url('uk', page)}">
<link rel="alternate" hreflang="en" href="{abs_url('en', page)}">
<link rel="alternate" hreflang="x-default" href="{abs_url('uk', page)}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:image" content="{BASE}assets/og.png">
<meta property="og:url" content="{abs_url(lang, page)}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#FBFAF9" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0F0E0D" media="(prefers-color-scheme: dark)">
<link rel="icon" type="image/png" sizes="64x64" href="{root}favicon.png">
<link rel="icon" type="image/png" sizes="32x32" href="{root}assets/favicon-32.png">
<link rel="apple-touch-icon" href="{root}assets/apple-touch-icon.png">
<link rel="stylesheet" href="{root}assets/style.css">
<script>document.documentElement.classList.add('js')</script>
</head>
<body class="page-{page}">
<header class="site-head">
  <div class="wrap">
    <a class="brand" href="{href(lang, 'index', lang)}"><img src="{root}assets/icon-96.png" alt="" width="36" height="36">Lichi</a>
    <nav class="site-nav" aria-label="{'Розділи' if lang == 'uk' else 'Sections'}">{nav_html}</nav>
    {lang_html}
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-foot">
  <div class="wrap">
    <span>© 2026 Mark Rishko</span>
    <nav aria-label="{'Документи' if lang == 'uk' else 'Documents'}">{foot}</nav>
  </div>
</footer>
<script>
(function () {{
  var head = document.querySelector('.site-head');
  var onScroll = function () {{ head.classList.toggle('scrolled', window.scrollY > 8); }};
  onScroll(); window.addEventListener('scroll', onScroll, {{ passive: true }});
  var items = document.querySelectorAll('[data-reveal]');
  if (!('IntersectionObserver' in window)) {{ items.forEach(function (el) {{ el.classList.add('in'); }}); return; }}
  var io = new IntersectionObserver(function (entries) {{
    entries.forEach(function (e) {{ if (e.isIntersecting) {{ e.target.classList.add('in'); io.unobserve(e.target); }} }});
  }}, {{ threshold: 0.3 }});
  items.forEach(function (el) {{ io.observe(el); }});
}})();
</script>
</body>
</html>
'''


def mail(text=None):
    return f'<a href="mailto:{EMAIL}">{text or EMAIL}</a>'


def insta(root):
    return (f'<a class="ig" href="{INSTAGRAM}"><img src="{root}assets/instagram.png" alt="Instagram" width="22" height="22">'
            '<span>@lichi_app</span></a>')


# ---------------------------------------------------------------- home

def home(lang):
    root = '' if lang == 'uk' else '../'
    c = {
        'uk': dict(
            title='Lichi — сканер складу продуктів',
            desc='Наведіть камеру на штрихкод — Lichi покаже оцінку складу від 0 до 10 і пояснить її простими словами.',
            h1='Що всередині продукту — простими словами',
            lead='Наведіть камеру iPhone на штрихкод, і Lichi покаже оцінку складу від 0 до 10 та пояснить, що в ньому добре, а на що варто звернути увагу.',
            soon='Незабаром в App Store',
            scale_label='Шкала оцінки від 0 до 10: поганий, сумнівний, компромісний, хороший і дуже хороший склад. Приклад: 8,6 — дуже хороший склад',
            marker='8,6',
            scale_note='Приклад: 8,6 — дуже хороший склад',
            mascot_alt='Лічі — маскот застосунку',
            what_h='Що показує Lichi',
            points=[
                ('Оцінку від 0 до 10', ' — за поживністю й інгредієнтами, а не лише за калоріями.'),
                ('Позитивне й негативне', ': що саме підняло чи опустило оцінку — цукор, сіль, насичені жири, клітковина, білок, фрукти й овочі, добавки.'),
                ('Склад', ' з кольоровими позначками й коротким коментарем до інгредієнтів.'),
                ('Алергени', ', якщо вони вказані у складі.'),
                ('Поживність', ' на 100 г чи 100 мл.'),
            ],
            ex_cap='Приклад картки продукту',
            ex_name='Гранола з горіхами',
            ex_score='7,2', ex_band='Хороший склад',
            ex_plus='Позитивне', ex_plus_items=['Цільне зерно', 'Горіхи', 'Клітковина'],
            ex_minus='Негативне', ex_minus_items=['Цукор'],
            ex_ingr='Склад', ex_ingr_items=[('green', 'Вівсяні пластівці'), ('amber', 'Мед'), ('green', 'Мигдаль'), ('blue', 'Кориця')],
            db_num='70 000+', db_h='продуктів з українських магазинів',
            db_p1='Власна база з фото. Якщо продукту в ній немає, Lichi шукає його у відкритій базі Open Food Facts.',
            db_p2='Історія сканувань і «Збережене» лишаються на вашому телефоні. Акаунт не потрібен, реклами немає.',
            pro_h='Безкоштовно і з Lichi PRO',
            free_t='Безкоштовно', free_d='3 нові продукти на день, а після першого ще 5 сканів у подарунок.',
            pro_t='Lichi PRO', pro_d='Скани без ліміту й пошук продуктів з оцінками. Місяць або рік; ціну App Store показує перед покупкою.',
            pro_link='Умови підписки',
            note='Оцінка Lichi описує сам продукт, а не ваш стан здоров’я. Це не медична порада. Якщо у вас алергії чи особлива дієта, завжди перевіряйте упаковку.',
            dev_h='Розробник',
            dev_p='Lichi створює Mark Rishko (Марк Рішко), Україна.<br>Питання, помилки в даних і пропозиції: ',
            news='Новини Lichi:',
            an_h='Як Lichi розбирає склад',
            an_sub='Скануєте пачку — і бачите, що в складі корисне, на що варто звернути увагу, а що нейтральне.',
            an_pack_alt='Пачка вівсяного батончика з шоколадом',
            an_pack1='Вівсяний', an_pack2='батончик', an_pack3='з шоколадом',
            an_score='4,1', an_band='Сумнівний склад',
            an_good='Корисне', an_bad='Варто звернути увагу', an_neutral='Нейтрально',
            an_items=[
                ('good', 'top', 'Вівсяні пластівці', 'Цільне зерно: більше клітковини.'),
                ('good', 'low', 'Фундук', 'Горіхи: корисні жири.'),
                ('bad', 'top', 'Цукор — 24 г', 'На 100 г — багато для батончика.'),
                ('bad', 'low', 'Пальмова олія', 'Додає насичених жирів.'),
                ('neutral', 'up', 'Ароматизатор', 'Дає запах і смак; на поживну цінність не впливає.'),
            ],
            an_note='Ілюстрація: вигаданий продукт, щоб показати, як виглядає розбір.',
        ),
        'en': dict(
            title='Lichi — food ingredient scanner',
            desc='Point your camera at a barcode: Lichi gives the product a 0–10 ingredient score and explains it in plain words.',
            h1='What’s inside a product, in plain words',
            lead='Point your iPhone camera at a barcode, and Lichi gives the product a score from 0 to 10 and explains what is good in it and what to watch for.',
            soon='Coming soon to the App Store',
            scale_label='Score scale from 0 to 10: poor, questionable, compromise, good and very good composition. Example: 8.6 — very good composition',
            marker='8.6',
            scale_note='Example: 8.6 — very good composition',
            mascot_alt='The Lichi mascot',
            what_h='What Lichi shows',
            points=[
                ('A score from 0 to 10', ', based on nutrition and ingredients, not just calories.'),
                ('Positive and negative', ': what raised or lowered the score — sugar, salt, saturated fat, fibre, protein, fruit and vegetables, additives.'),
                ('Ingredients', ' with colour marks and short notes.'),
                ('Allergens', ', when the ingredient list names them.'),
                ('Nutrition', ' per 100 g or 100 ml.'),
            ],
            ex_cap='Example of a product card',
            ex_name='Granola with nuts',
            ex_score='7.2', ex_band='Good composition',
            ex_plus='Positive', ex_plus_items=['Whole grain', 'Nuts', 'Fibre'],
            ex_minus='Negative', ex_minus_items=['Sugar'],
            ex_ingr='Ingredients', ex_ingr_items=[('green', 'Rolled oats'), ('amber', 'Honey'), ('green', 'Almonds'), ('blue', 'Cinnamon')],
            db_num='70,000+', db_h='products from Ukrainian shops',
            db_p1='Our own database, with photos. If a product is not there, Lichi looks it up in the open Open Food Facts database.',
            db_p2='Your scan history and Saved products stay on your phone. No account needed, no ads.',
            pro_h='Free and with Lichi PRO',
            free_t='Free', free_d='3 new products a day, plus 5 gift scans after your first one.',
            pro_t='Lichi PRO', pro_d='Unlimited scans and product search with scores. Monthly or yearly; the App Store shows the price before you buy.',
            pro_link='Subscription terms',
            note='Lichi’s score describes the product itself, not your health. It is not medical advice. If you have allergies or a special diet, always check the pack.',
            dev_h='Developer',
            dev_p='Lichi is made by Mark Rishko, Ukraine.<br>Questions, data errors and ideas: ',
            news='Lichi news:',
            an_h='How Lichi reads a label',
            an_sub='Scan the pack and see what in the ingredients is good, what to watch for, and what is neutral.',
            an_pack_alt='A pack of an oat bar with chocolate',
            an_pack1='Oat', an_pack2='bar', an_pack3='with chocolate',
            an_score='4.1', an_band='Questionable composition',
            an_good='Good', an_bad='Watch for', an_neutral='Neutral',
            an_items=[
                ('good', 'top', 'Rolled oats', 'Whole grain: more fibre.'),
                ('good', 'low', 'Hazelnuts', 'Nuts: good fats.'),
                ('bad', 'top', 'Sugar — 24 g', 'Per 100 g, a lot for a bar.'),
                ('bad', 'low', 'Palm oil', 'Adds saturated fat.'),
                ('neutral', 'up', 'Flavouring', 'Adds smell and taste; it doesn’t change the nutrition.'),
            ],
            an_note='Illustration: a made-up product, to show what the breakdown looks like.',
        ),
    }[lang]

    points = ''.join(f'<li><b>{b}</b>{rest}</li>' for b, rest in c['points'])
    plus = ''.join(f'<li style="--i:{i}">{x}</li>' for i, x in enumerate(c['ex_plus_items']))
    minus = ''.join(f'<li style="--i:{i + 3}">{x}</li>' for i, x in enumerate(c['ex_minus_items']))
    ingr = ''.join(f'<li style="--i:{i + 4}"><i class="dot {col}"></i>{x}</li>' for i, (col, x) in enumerate(c['ex_ingr_items']))

    tags = {'good': c['an_good'], 'bad': c['an_bad'], 'neutral': c['an_neutral']}
    arrows = {
        'top': '<svg class="arw" viewBox="0 0 72 40" aria-hidden="true"><path pathLength="1" d="M2 8 C 30 8, 38 31, 66 31"/><path class="head" pathLength="1" d="M57 25 L66 31 L57 37"/></svg>',
        'low': '<svg class="arw" viewBox="0 0 72 40" aria-hidden="true"><path pathLength="1" d="M2 32 C 30 32, 38 9, 66 9"/><path class="head" pathLength="1" d="M57 3 L66 9 L57 15"/></svg>',
        'up': '<svg class="arw" viewBox="0 0 40 56" aria-hidden="true"><path pathLength="1" d="M20 54 L20 6"/><path class="head" pathLength="1" d="M13 14 L20 5 L27 14"/></svg>',
    }

    def call(i, kind, pos, name, note):
        return (f'<li class="call {kind} {pos}" style="--i:{i}"><span class="tag">{tags[kind]}</span>'
                f'<b>{name}</b><span class="call-note">{note}</span>{arrows[pos]}</li>')

    items = c['an_items']
    left = ''.join(call(i, *it) for i, it in enumerate(items) if it[0] == 'good')
    right = ''.join(call(i, *it) for i, it in enumerate(items) if it[0] == 'bad')
    bottom = ''.join(call(i, *it) for i, it in enumerate(items) if it[0] == 'neutral')
    oats = ''.join(f'<ellipse cx="{x}" cy="{y}" rx="7" ry="4" transform="rotate({r} {x} {y})"/>'
                   for x, y, r in [(22, 16, 20), (48, 30, -15), (76, 14, 30), (104, 34, 10), (126, 18, -25), (36, 40, 40), (92, 42, -35), (64, 24, 5), (118, 40, 25)])
    bars = ''.join(f'<rect x="{x}" y="8" width="{w}" height="22" />' for x, w in [(8, 2), (12, 1), (15, 3), (20, 1), (23, 2), (27, 1), (30, 3), (35, 2), (39, 1), (42, 2), (46, 1), (49, 3), (54, 1), (56, 2)])
    pack = f'''<svg class="pack-svg" viewBox="0 0 260 340" role="img" aria-label="{c['an_pack_alt']}">
        <defs>
          <linearGradient id="pk" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F6BE78"/><stop offset="1" stop-color="#DC7A33"/></linearGradient>
          <linearGradient id="br" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8E5A33"/><stop offset="1" stop-color="#5A3218"/></linearGradient>
        </defs>
        <ellipse cx="130" cy="328" rx="92" ry="8" fill="rgba(23,21,19,.14)"/>
        <rect x="30" y="20" width="200" height="298" rx="20" fill="url(#pk)"/>
        <path d="M30 40 Q30 20 50 20 H210 Q230 20 230 40 V58 H30 Z" fill="rgba(255,255,255,.2)"/>
        <rect x="46" y="74" width="168" height="78" rx="14" fill="#FFF8F0"/>
        <text x="130" y="106" text-anchor="middle" class="pk-t1">{c['an_pack1']}</text>
        <text x="130" y="134" text-anchor="middle" class="pk-t1">{c['an_pack2']}</text>
        <g transform="translate(58 172) rotate(-7 72 26)">
          <rect width="144" height="54" rx="15" fill="url(#br)"/>
          <rect x="6" y="5" width="132" height="16" rx="8" fill="rgba(255,255,255,.12)"/>
          <g fill="#EBCB9C">{oats}</g>
        </g>
        <text x="130" y="262" text-anchor="middle" class="pk-t2">{c['an_pack3']}</text>
        <g transform="translate(152 274)"><rect width="64" height="34" rx="6" fill="#fff"/><g fill="#171513">{bars}</g></g>
      </svg>'''
    anatomy = f'''
<section class="block anatomy">
  <div class="wrap">
    <h2>{c['an_h']}</h2>
    <p class="sub">{c['an_sub']}</p>
    <div class="anat" data-reveal>
      <ul class="anat-side anat-left">{left}</ul>
      <div class="anat-pack">
        {pack}
        <span class="scan-line" aria-hidden="true"></span>
        <div class="pack-score"><span class="ring ring-weak" style="--score:41"><span>{c['an_score']}</span></span><span class="pack-band">{c['an_band']}</span></div>
      </div>
      <ul class="anat-side anat-right">{right}</ul>
      <ul class="anat-bottom">{bottom}</ul>
    </div>
    <p class="anat-note">{c['an_note']}</p>
  </div>
</section>
'''

    body = f'''
<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <h1>{c['h1']}</h1>
      <p class="lead">{c['lead']}</p>
      <span class="soon">{c['soon']}</span>
      <div class="scale" role="img" aria-label="{c['scale_label']}">
        <div class="scale-track">
          <div class="scale-bar"><span class="poor"></span><span class="weak"></span><span class="mid"></span><span class="good"></span><span class="best"></span></div>
          <span class="marker" style="--at:86%"><b>{c['marker']}</b></span>
        </div>
        <div class="scale-nums"><span>0</span><span>10</span></div>
        <p class="scale-note">{c['scale_note']}</p>
      </div>
    </div>
    <div class="hero-art">
      <picture><source srcset="{root}assets/lichi.webp" type="image/webp"><img src="{root}assets/lichi.png" alt="{c['mascot_alt']}" width="440" height="440"></picture>
      <span class="scan-line" aria-hidden="true"></span>
    </div>
  </div>
</section>

<section class="block features">
  <div class="wrap feat-grid">
    <div>
      <h2>{c['what_h']}</h2>
      <ul class="points">{points}</ul>
    </div>
    <figure class="example" data-reveal>
      <figcaption>{c['ex_cap']}</figcaption>
      <div class="ex-card">
        <div class="ex-top">
          <div class="ring" style="--score:72"><span>{c['ex_score']}</span></div>
          <div>
            <p class="ex-name">{c['ex_name']}</p>
            <p class="ex-band">{c['ex_band']}</p>
          </div>
        </div>
        <p class="ex-h">{c['ex_plus']}</p>
        <ul class="ex-list plus">{plus}</ul>
        <p class="ex-h">{c['ex_minus']}</p>
        <ul class="ex-list minus">{minus}</ul>
        <p class="ex-h">{c['ex_ingr']}</p>
        <ul class="ex-ingr">{ingr}</ul>
      </div>
    </figure>
  </div>
</section>

{anatomy}
<section class="block sheet-block">
  <div class="wrap">
    <div class="sheet">
      <div class="sheet-db">
        <p class="big-num">{c['db_num']}</p>
        <h2 class="num-h">{c['db_h']}</h2>
        <p>{c['db_p1']}</p>
        <p>{c['db_p2']}</p>
      </div>
      <div class="sheet-pro">
        <h2>{c['pro_h']}</h2>
        <dl class="plans">
          <div><dt>{c['free_t']}</dt><dd>{c['free_d']}</dd></div>
          <div class="pro"><dt>{c['pro_t']}</dt><dd>{c['pro_d']}</dd></div>
        </dl>
        <p><a href="terms.html#pro">{c['pro_link']}</a></p>
      </div>
    </div>
    <p class="note">{c['note']}</p>
  </div>
</section>

<section class="block dev-block">
  <div class="wrap">
    <h2>{c['dev_h']}</h2>
    <div class="dev">
      <img src="{root}assets/icon-96.png" alt="" width="64" height="64">
      <div>
        <p>{c['dev_p']}{mail()}</p>
        <p class="social">{c['news']} {insta(root)}</p>
      </div>
    </div>
  </div>
</section>
'''
    return c['title'], c['desc'], body


# ---------------------------------------------------------------- privacy

def services(lang):
    rows = {
        'uk': [
            ('Supabase', 'https://supabase.com/privacy', 'сервер нашої бази продуктів (Франкфурт, ЄС)'),
            ('Open Food Facts', 'https://world.openfoodfacts.org/privacy', 'відкрита база продуктів'),
            ('Sentry', 'https://sentry.io/privacy/', 'звіти про збої (сервер у ЄС)'),
            ('RevenueCat', 'https://www.revenuecat.com/privacy', 'перевірка підписки Lichi PRO'),
            ('Apple', 'https://www.apple.com/legal/privacy/', 'App Store і оплата підписки'),
        ],
        'en': [
            ('Supabase', 'https://supabase.com/privacy', 'our product database server (Frankfurt, EU)'),
            ('Open Food Facts', 'https://world.openfoodfacts.org/privacy', 'open product database'),
            ('Sentry', 'https://sentry.io/privacy/', 'crash reports (servers in the EU)'),
            ('RevenueCat', 'https://www.revenuecat.com/privacy', 'checking the Lichi PRO subscription'),
            ('Apple', 'https://www.apple.com/legal/privacy/', 'App Store and subscription payments'),
        ],
    }[lang]
    return '<ul>' + ''.join(f'<li><a href="{u}">{n}</a> — {d}</li>' for n, u, d in rows) + '</ul>'


def privacy(lang):
    t = T[lang]
    if lang == 'uk':
        title = 'Політика конфіденційності — Lichi'
        desc = 'Які дані використовує застосунок Lichi для iPhone і цей сайт.'
        body = f'''
<article class="doc"><div class="prose-wrap">
<h1>Політика конфіденційності</h1>
<p class="updated">{t['updated']} {UPDATED[lang]}</p>
<p class="intro">Ця політика описує, які дані використовує застосунок Lichi для iPhone і цей сайт. Lichi створює й відповідає за обробку даних Mark Rishko (Марк Рішко), Україна. Зв’язок: {mail()}.</p>
<div class="summary"><ul>
<li>Акаунт не потрібен, і Lichi не знає, хто ви.</li>
<li>Історія сканувань і «Збережене» лишаються на вашому телефоні.</li>
<li>Реклами й відстеження немає; ми не продаємо дані.</li>
</ul></div>

<h2>Камера</h2>
<p>Lichi використовує камеру лише для сканування штрихкодів і пошуку продуктів. Штрихкод розпізнається на телефоні; зображення з камери нікуди не надсилаються.</p>

<h2>На пристрої</h2>
<p>Історія сканувань, збережені продукти, ваш рівень і налаштування нагадувань зберігаються лише на цьому пристрої. Вони зникають, коли ви видаляєте застосунок.</p>

<h2>Без акаунта</h2>
<p>Акаунт не потрібен: Lichi не просить ваше ім’я, email чи номер телефону і не створює профіль.</p>

<h2>Пошук продукту</h2>
<p>Щоб знайти продукт, Lichi надсилає лише штрихкод або текст пошуку на наш сервер з базою продуктів (Supabase, Франкфурт, ЄС). Якщо продукту там немає або бракує даних про поживність, штрихкод надсилається й до Open Food Facts. Ім’я, акаунт, фото чи місцезнаходження разом з ними не надсилаються. Як і будь-який вебсервер, ці сервіси бачать IP-адресу запиту. Щоб захистити сервер від зловживань, ми рахуємо кількість запитів з однієї IP-адреси.</p>

<h2>Сповіщення</h2>
<p>Нагадування ставить і показує сам телефон. Lichi не надсилає їх зі свого сервера, тож ваш розклад нікуди не передається. Вимкнути нагадування можна в профілі Lichi або в налаштуваннях iPhone.</p>

<h2>Звіти про збої</h2>
<p>Щоб помічати й виправляти збої, Lichi надсилає в Sentry (сервер у ЄС) технічні дані: опис помилки, модель пристрою, версії iOS і застосунку, а якщо помилка сталася з продуктом — його штрихкод. Також Sentry отримує анонімну позначку про кожен запуск, щоб ми бачили, яка частка запусків минає без збоїв. Ім’я, email, фото й місцезнаходження не надсилаються. Як і будь-який вебсервер, Sentry бачить IP-адресу запиту.</p>

<h2>Покупки</h2>
<p>Підписку Lichi PRO оформлює й оплачує Apple; дані вашої картки Lichi не бачить. Щоб перевіряти підписку, Lichi використовує сервіс RevenueCat: він отримує випадковий ідентифікатор цього встановлення (без імені й email), історію покупок Lichi PRO з Apple, мову й валюту магазину, а також версії iOS і застосунку. Як і будь-який вебсервер, RevenueCat бачить IP-адресу запиту.</p>

<h2>Чого ми не робимо</h2>
<ul>
<li>Не показуємо рекламу й не підключаємо рекламні сервіси.</li>
<li>Не відстежуємо вас в інших застосунках і на сайтах.</li>
<li>Не продаємо дані й не передаємо їх брокерам даних.</li>
<li>Не просимо доступу до контактів чи геолокації. Якщо ви зберігаєте картинку з оцінкою, телефон лише додає її у «Фото» — ваші фото Lichi не читає.</li>
</ul>

<h2>Сервіси, які ми використовуємо</h2>
{services(lang)}

<h2>Ваші права</h2>
<p>Lichi не пов’язує дані з вашою особою, тому зазвичай не може знайти на серверах записи саме про вас. Дані на телефоні ви контролюєте самі: щоб стерти історію, «Збережене» й налаштування, видаліть застосунок.</p>
<p>Якщо ви хочете дізнатися, які дані про вас є, виправити чи видалити їх або заперечити проти обробки, напишіть на {mail()}. Якщо ви в ЄС, ви також можете звернутися до органу із захисту даних своєї країни.</p>

<h2>Діти</h2>
<p>Lichi не створений спеціально для дітей і свідомо не збирає персональних даних дітей.</p>

<h2>Цей сайт</h2>
<p>Сайт не використовує файли cookie, аналітику чи рекламу. Його розміщує GitHub Pages; як і будь-який вебсервер, GitHub бачить IP-адресу відвідувача.</p>

<h2>Зміни</h2>
<p>Якщо політика зміниться, ми оновимо цю сторінку й дату вгорі.</p>

<h2>Контакти</h2>
<p>Mark Rishko (Марк Рішко), Україна — {mail()}</p>
</div></article>
'''
    else:
        title = 'Privacy Policy — Lichi'
        desc = 'What data the Lichi iPhone app and this website use.'
        body = f'''
<article class="doc"><div class="prose-wrap">
<h1>Privacy Policy</h1>
<p class="updated">{t['updated']} {UPDATED[lang]}</p>
<p class="intro">This policy describes what data the Lichi iPhone app and this website use. Lichi is made by Mark Rishko, Ukraine, who is responsible for processing the data. Contact: {mail()}.</p>
<div class="summary"><ul>
<li>No account is needed, and Lichi does not know who you are.</li>
<li>Your scan history and Saved products stay on your phone.</li>
<li>No ads, no tracking; we do not sell data.</li>
</ul></div>

<h2>Camera</h2>
<p>Lichi uses the camera only to scan barcodes and look up products. The barcode is read on your phone; camera images are never sent anywhere.</p>

<h2>On this device</h2>
<p>Your scan history, saved products, level and reminder settings are stored only on this device. They are removed when you delete the app.</p>

<h2>No account</h2>
<p>No account is needed: Lichi does not ask for your name, email or phone number and does not create a profile.</p>

<h2>Finding a product</h2>
<p>To find a product, Lichi sends only the barcode or the search text to our product database server (Supabase, Frankfurt, EU). If the product is not there, or its nutrition data is missing, the barcode is sent to Open Food Facts as well. No name, account, photo or location is sent with them. Like any web server, these services see the IP address of the request. To protect the server from abuse, we count requests coming from one IP address.</p>

<h2>Notifications</h2>
<p>Reminders are scheduled and shown by your phone itself. Lichi does not send them from its server, so your schedule is not shared anywhere. You can turn reminders off in your Lichi profile or in iPhone Settings.</p>

<h2>Crash reports</h2>
<p>To notice and fix crashes, Lichi sends technical data to Sentry (servers in the EU): a description of the error, the device model, the iOS and app versions, and, if the error happened with a product, its barcode. Sentry also receives an anonymous note about each launch, so we can see what share of launches go without a crash. No name, email, photo or location is sent. Like any web server, Sentry sees the IP address of the request.</p>

<h2>Purchases</h2>
<p>Apple handles and charges the Lichi PRO subscription; Lichi never sees your card details. To check the subscription, Lichi uses RevenueCat: it receives a random identifier of this install (no name or email), your Lichi PRO purchase history from Apple, the store language and currency, and the iOS and app versions. Like any web server, RevenueCat sees the IP address of the request.</p>

<h2>What we don’t do</h2>
<ul>
<li>We don’t show ads or use advertising services.</li>
<li>We don’t track you across other apps and websites.</li>
<li>We don’t sell data or share it with data brokers.</li>
<li>We don’t ask for access to your contacts or location. If you save a score image, your phone only adds it to Photos — Lichi does not read your photos.</li>
</ul>

<h2>Services we use</h2>
{services(lang)}

<h2>Your rights</h2>
<p>Lichi does not link data to your identity, so it usually cannot find records about you on its servers. You control the data on your phone: to erase your history, Saved products and settings, delete the app.</p>
<p>If you want to know what data about you exists, correct or delete it, or object to its processing, write to {mail()}. If you are in the EU, you can also contact your country’s data protection authority.</p>

<h2>Children</h2>
<p>Lichi is not made specifically for children and does not knowingly collect children’s personal data.</p>

<h2>This website</h2>
<p>This website uses no cookies, analytics or ads. It is hosted on GitHub Pages; like any web server, GitHub sees the visitor’s IP address.</p>

<h2>Changes</h2>
<p>If this policy changes, we will update this page and the date at the top.</p>

<h2>Contact</h2>
<p>Mark Rishko, Ukraine — {mail()}</p>
</div></article>
'''
    return title, desc, body


# ---------------------------------------------------------------- terms

def terms(lang):
    t = T[lang]
    if lang == 'uk':
        title = 'Умови використання — Lichi'
        desc = 'Умови використання застосунку Lichi і підписки Lichi PRO.'
        body = f'''
<article class="doc"><div class="prose-wrap">
<h1>Умови використання</h1>
<p class="updated">{t['updated']} {UPDATED[lang]}</p>
<p class="intro">Ці умови стосуються застосунку Lichi для iPhone. Користування застосунком також регулюють <a href="{EULA}">Стандартні умови ліцензії Apple (EULA)</a>.</p>

<h2>Оцінка 0–10</h2>
<p>Lichi допомагає швидко розібратися у складі продукту та показує власну оцінку від 0 до 10.</p>
<h2>Чим оцінка не є</h2>
<p>Ця оцінка не є Nutri-Score, медичною рекомендацією або офіційною сертифікацією продукту.</p>
<h2>Зовнішні дані</h2>
<p>Інформація про продукти може надходити з зовнішніх баз даних, тому іноді вона може бути неповною або неточною. Частина даних — з Open Food Facts за ліцензією <a href="https://opendatacommons.org/licenses/odbl/1-0/">Open Database License (ODbL)</a>.</p>
<h2>Упаковка</h2>
<p>Перед покупкою чи вживанням продукту перевіряйте актуальну інформацію на його упаковці.</p>
<h2>Ваш вибір</h2>
<p>Остаточний вибір завжди залишається за вами.</p>

<h2>Медичне застереження</h2>
<ul>
<li>Оцінка Lichi не є діагнозом, лікуванням або персональною медичною рекомендацією.</li>
<li>Вона описує сам продукт — його склад і поживність, а не ваш стан здоров’я чи індивідуальні потреби.</li>
<li>Якщо у вас є алергії, медичні обмеження або спеціальна дієта, завжди перевіряйте інформацію на упаковці та за потреби консультуйтеся з лікарем.</li>
<li>Дані про продукти бувають неповними або застарілими, а оцінку рахує програма. Важливу інформацію, особливо склад і алергени, завжди перевіряйте на упаковці.</li>
</ul>

<h2 id="pro">Lichi PRO</h2>
<p>Lichi PRO — підписка на місяць або на рік, що поновлюється автоматично. Ціну App Store показує перед покупкою. Якщо Apple дає вам пробний тиждень, першу оплату знімуть з Apple ID після нього, далі — на початку кожного терміну, поки ви не скасуєте.</p>
<p>Скасувати можна в налаштуваннях Apple ID щонайменше за 24 години до кінця пробного тижня чи поточного терміну; PRO працює до кінця оплаченого. Без PRO — 3 нові продукти на день і 5 сканів у подарунок після першого.</p>

<h2>Контакти</h2>
<p>Mark Rishko (Марк Рішко), Україна — {mail()}</p>
</div></article>
'''
    else:
        title = 'Terms of Use — Lichi'
        desc = 'Terms of use of the Lichi app and the Lichi PRO subscription.'
        body = f'''
<article class="doc"><div class="prose-wrap">
<h1>Terms of Use</h1>
<p class="updated">{t['updated']} {UPDATED[lang]}</p>
<p class="intro">These terms apply to the Lichi iPhone app. Use of the app is also governed by <a href="{EULA}">Apple’s Standard License Agreement (EULA)</a>.</p>

<h2>A 0–10 score</h2>
<p>Lichi helps you make sense of a product’s ingredients quickly and shows its own score from 0 to 10.</p>
<h2>What the score is not</h2>
<p>This score is not Nutri-Score, medical advice, or an official product certification.</p>
<h2>Outside data</h2>
<p>Product information can come from outside databases, so it is sometimes incomplete or inaccurate. Part of the data comes from Open Food Facts under the <a href="https://opendatacommons.org/licenses/odbl/1-0/">Open Database License (ODbL)</a>.</p>
<h2>The pack</h2>
<p>Before you buy or eat a product, check the current information on its pack.</p>
<h2>Your choice</h2>
<p>The final choice is always yours.</p>

<h2>Health disclaimer</h2>
<ul>
<li>Lichi’s score is not a diagnosis, a treatment, or personal medical advice.</li>
<li>It describes the product itself — its ingredients and nutrition — not your health or your individual needs.</li>
<li>If you have allergies, medical restrictions, or a special diet, always check the information on the pack and talk to a doctor when you need to.</li>
<li>Product data can be incomplete or out of date, and the score is calculated by the app. Always check important information, especially ingredients and allergens, on the pack.</li>
</ul>

<h2 id="pro">Lichi PRO</h2>
<p>Lichi PRO is a monthly or yearly subscription that renews automatically. The App Store shows the price before you buy. If Apple gives you a free week, the first payment is charged to your Apple ID after it, and then at the start of each period until you cancel.</p>
<p>Cancel in your Apple ID settings at least 24 hours before the free week or the current period ends; PRO keeps working until the end of what you paid for. Without PRO: 3 new products a day and 5 gift scans after the first one.</p>

<h2>Contact</h2>
<p>Mark Rishko, Ukraine — {mail()}</p>
</div></article>
'''
    return title, desc, body


# ---------------------------------------------------------------- support

FAQ = {
    'uk': [
        ('Як формується оцінка 0–10?', 'Lichi враховує склад продукту та поживність на 100 г / мл, а потім показує одну підсумкову оцінку.'),
        ('Чому продукт із високою калорійністю може мати хороший бал?', 'Бо калорійність — лише один із факторів. Наприклад, горіхи й олії калорійні, але можуть містити сприятливі жири та інші корисні компоненти.'),
        ('Чому продукт із низькою калорійністю може мати низький бал?', 'Низька калорійність сама по собі не означає хороший склад. Важливі також цукри, тип жирів, рафіновані інгредієнти та інші фактори.'),
        ('Чому E-добавка не знижує бал автоматично?', 'Сам номер E ще не означає, що інгредієнт небажаний. Lichi оцінює конкретну роль і властивості інгредієнта.'),
        ('Чи враховує Lichi алергени?', 'Так, якщо інформація про алергени доступна, Lichi показує її окремо. Але алерген сам по собі не знижує оцінку продукту.'),
        ('Чому оцінка Lichi може відрізнятися від Nutri-Score?', 'Lichi використовує власний метод оцінки й аналізує не тільки поживні показники, а й сам склад продукту.'),
        ('Продукт знайдено неправильно або дані помилкові', f'Перевірте назву, фото та склад на упаковці. Дані з зовнішніх баз іноді бувають неповними або застарілими. Надішліть нам штрихкод і фото упаковки на {mail()} — ми виправимо дані.'),
        ('Чи можна користуватися Lichi офлайн?', 'Історія сканів і збережені продукти відкриваються без інтернету, але для нових сканів і пошуку потрібна мережа.'),
    ],
    'en': [
        ('How is the 0–10 score formed?', 'Lichi takes the product’s ingredients and its nutrition per 100 g / ml, then shows one overall score.'),
        ('Why can a high-calorie product still score well?', 'Because calories are only one factor. Nuts and oils are calorie-dense, for example, but they can contain favourable fats and other useful components.'),
        ('Why can a low-calorie product score poorly?', 'Low calories on their own do not mean a good ingredient list. Sugars, the type of fat, refined ingredients, and other factors matter too.'),
        ('Why doesn’t an E-number lower the score automatically?', 'The E number itself does not mean an ingredient is harmful. Lichi judges that ingredient’s specific role and properties.'),
        ('Does Lichi take allergens into account?', 'Yes. When allergen information is available, Lichi shows it separately. An allergen on its own does not lower the product’s score.'),
        ('Why can Lichi’s score differ from Nutri-Score?', 'Lichi uses its own scoring method and looks at the ingredient list as well as the nutrition figures.'),
        ('The wrong product was found, or the data is wrong', f'Check the name, photo, and ingredients on the pack. Data from outside databases can sometimes be incomplete or out of date. Send us the barcode and a photo of the pack at {mail()}, and we will fix the data.'),
        ('Can I use Lichi offline?', 'You can open your scan history and saved products without internet, but new scans and search need a network connection.'),
    ],
}

PRO_FAQ = {
    'uk': [
        ('Скільки можна сканувати безкоштовно?', 'Без PRO — 3 нові продукти на день, а після першого продукту ще 5 сканів у подарунок; подарунок не згорає. Повторний скан того самого продукту того ж дня не рахується.'),
        ('Як оформити Lichi PRO?', 'У Lichi відкрийте «Профіль» → «Lichi PRO» і оберіть місяць або рік. Ціну App Store показує перед покупкою.'),
        ('Як скасувати підписку?', 'На iPhone: «Налаштування» → ваше ім’я → «Підписки» → Lichi → «Скасувати підписку». Або в Lichi: «Профіль» → «Lichi PRO» → «Скасувати» — відкриється те саме вікно Apple. Скасуйте щонайменше за 24 години до кінця пробного тижня чи оплаченого терміну; PRO працює до кінця оплаченого.'),
        ('Новий iPhone або перевстановили застосунок', 'Відкрийте «Профіль» → «Відновити покупки». Потрібен той самий Apple ID, з яким ви оформлювали підписку.'),
        ('Як повернути гроші?', 'Оплату приймає Apple, тож і повернення оформлює Apple: <a href="https://reportaproblem.apple.com">reportaproblem.apple.com</a>.'),
    ],
    'en': [
        ('How much can I scan for free?', 'Without PRO: 3 new products a day, plus 5 gift scans after your first product; the gift does not expire. Scanning the same product again on the same day does not count.'),
        ('How do I get Lichi PRO?', 'In Lichi, open Profile → Lichi PRO and choose monthly or yearly. The App Store shows the price before you buy.'),
        ('How do I cancel?', 'On iPhone: Settings → your name → Subscriptions → Lichi → Cancel Subscription. Or in Lichi: Profile → Lichi PRO → Cancel, which opens the same Apple window. Cancel at least 24 hours before the free week or the paid period ends; PRO keeps working until the end of what you paid for.'),
        ('New iPhone or reinstalled the app', 'Open Profile → Restore Purchases. Use the same Apple ID you subscribed with.'),
        ('How do I get a refund?', 'Apple takes the payment, so refunds go through Apple: <a href="https://reportaproblem.apple.com">reportaproblem.apple.com</a>.'),
    ],
}


def details(items):
    return '<div class="faq">' + ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in items) + '</div>'


def support(lang):
    root = '' if lang == 'uk' else '../'
    if lang == 'uk':
        title = 'Підтримка — Lichi'
        desc = 'Питання про Lichi і підписку Lichi PRO, зв’язок з розробником.'
        body = f'''
<article class="doc"><div class="prose-wrap">
<h1>Підтримка</h1>
<p class="intro">Відповіді на часті питання — нижче. Якщо не знайшли свою, напишіть нам.</p>
<div class="contact"><p>Email: {mail()}<br>{insta(root)}<br><span class="muted">Якщо питання про продукт, додайте штрихкод і фото упаковки (склад і таблицю поживності).</span></p></div>

<h2>Lichi PRO і безкоштовні скани</h2>
{details(PRO_FAQ[lang])}

<h2>Оцінка й дані</h2>
{details(FAQ[lang])}

<h2>Ваші дані</h2>
<p>Акаунт не потрібен. Історія сканувань, «Збережене» й налаштування зберігаються лише на телефоні та зникають, коли ви видаляєте застосунок. Докладніше — у <a href="privacy.html">політиці конфіденційності</a>.</p>

<h2>Розробник</h2>
<p>Mark Rishko (Марк Рішко), Україна — {mail()}</p>
</div></article>
'''
    else:
        title = 'Support — Lichi'
        desc = 'Questions about Lichi and the Lichi PRO subscription, and how to contact the developer.'
        body = f'''
<article class="doc"><div class="prose-wrap">
<h1>Support</h1>
<p class="intro">Answers to common questions are below. If yours is not there, write to us.</p>
<div class="contact"><p>Email: {mail()}<br>{insta(root)}<br><span class="muted">For a question about a product, include the barcode and a photo of the pack (ingredients and nutrition table).</span></p></div>

<h2>Lichi PRO and free scans</h2>
{details(PRO_FAQ[lang])}

<h2>Score and data</h2>
{details(FAQ[lang])}

<h2>Your data</h2>
<p>No account is needed. Your scan history, Saved products and settings are stored only on your phone and are removed when you delete the app. Read more in the <a href="privacy.html">Privacy Policy</a>.</p>

<h2>Developer</h2>
<p>Mark Rishko, Ukraine — {mail()}</p>
</div></article>
'''
    return title, desc, body


TOC_LABEL = {'uk': 'На цій сторінці', 'en': 'On this page'}


def with_toc(lang, body):
    """Gives every h2 an id and adds a contents list beside the text (shown on wide screens)."""
    n = 0

    def number(m):
        nonlocal n
        n += 1
        return m.group(0) if m.group(1) else f'<h2 id="s{n}">{m.group(3)}</h2>'

    body = re.sub(r'<h2( id="([^"]+)")?>(.*?)</h2>', number, body)
    items = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body)
    toc = (f'<nav class="toc" aria-label="{TOC_LABEL[lang]}"><p class="toc-h">{TOC_LABEL[lang]}</p><ol>'
           + ''.join(f'<li><a href="#{i}">{t}</a></li>' for i, t in items) + '</ol></nav>')
    body = body.replace('<article class="doc"><div class="prose-wrap">',
                        f'<article class="doc has-toc"><div class="doc-grid">{toc}<div class="prose">', 1)
    return body.replace('</div></article>', '</div></div></article>', 1)


BUILDERS = {'index': home, 'privacy': privacy, 'terms': terms, 'support': support}

for lang in ('uk', 'en'):
    folder = OUT if lang == 'uk' else OUT / 'en'
    folder.mkdir(parents=True, exist_ok=True)
    for page in PAGES:
        title, desc, body = BUILDERS[page](lang)
        if page in ('privacy', 'terms'):
            body = with_toc(lang, body)
        name = 'index.html' if page == 'index' else f'{page}.html'
        (folder / name).write_text(layout(lang, page, title, desc, body), encoding='utf-8')

# 404 page (GitHub Pages serves it for missing paths)
nf_body = '''
<article class="doc"><div class="prose-wrap">
<h1>Сторінку не знайдено</h1>
<p class="intro">Такої сторінки немає. Перейдіть на <a href="/lichi/">головну</a> або до <a href="/lichi/support.html">підтримки</a>.</p>
<p lang="en">This page does not exist. Go to the <a href="/lichi/en/">home page</a> or <a href="/lichi/en/support.html">support</a>.</p>
</div></article>
'''
nf = layout('uk', 'index', 'Сторінку не знайдено — Lichi', 'Сторінку не знайдено.', nf_body)
nf = nf.replace('href="./"', 'href="/lichi/"').replace('href="support.html"', 'href="/lichi/support.html"') \
       .replace('href="privacy.html"', 'href="/lichi/privacy.html"').replace('href="terms.html"', 'href="/lichi/terms.html"') \
       .replace('href="en/"', 'href="/lichi/en/"').replace('href="favicon.png"', 'href="/lichi/favicon.png"') \
       .replace('href="assets/', 'href="/lichi/assets/').replace('src="assets/', 'src="/lichi/assets/')
(OUT / '404.html').write_text(nf, encoding='utf-8')
(OUT / '.nojekyll').write_text('', encoding='utf-8')
print('built', sorted(str(p.relative_to(OUT)) for p in OUT.rglob('*') if p.is_file()))
