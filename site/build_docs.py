#!/usr/bin/env python3
import os
import re
import sys
from html import escape

try:
    import markdown
except ImportError:
    print("Please install the python 'markdown' package: pip install markdown")
    sys.exit(1)

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{description}">
  <title>{title} · BoundaryKit specs</title>
  <style>
    :root {{
      color-scheme: dark;
      --ink: #070b10;
      --ink-2: #0b111a;
      --panel: rgba(14, 24, 36, 0.78);
      --panel-strong: #101a27;
      --line: rgba(142, 246, 255, 0.22);
      --text: #f8fbff;
      --muted: #b7c8d8;
      --dim: #7f93a8;
      --cyan: #8ef6ff;
      --font-body: "SF Pro Text", "Segoe UI", ui-sans-serif, system-ui, sans-serif;
      --font-mono: "SFMono-Regular", "Cascadia Code", "Liberation Mono", ui-monospace, monospace;
    }}

    body {{
      background-color: var(--ink);
      color: var(--text);
      font-family: var(--font-body);
      line-height: 1.6;
      margin: 0;
      padding: 0;
    }}

    .container {{
      max-width: 1040px;
      margin: 0 auto;
      padding: clamp(1rem, 4vw, 3rem) 1.5rem;
    }}

    .site-header {{
      position: sticky;
      top: 16px;
      z-index: 100;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0.7rem 1.4rem;
      border: 1px solid rgba(142, 246, 255, 0.18);
      border-radius: 999px;
      background: rgba(7, 11, 16, 0.74);
      backdrop-filter: blur(18px);
      -webkit-backdrop-filter: blur(18px);
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.4);
      margin-bottom: 3.5rem;
    }}

    .top-nav-group {{
      display: flex;
      align-items: center;
      gap: 0.75rem;
      font-family: var(--font-mono);
      font-size: 0.85rem;
    }}

    .top-nav-link {{
      color: var(--dim);
      text-decoration: none;
      transition: color 0.2s;
      border-bottom: none !important;
    }}

    .top-nav-link:hover:not(.disabled) {{
      color: var(--cyan);
    }}

    .top-nav-link.disabled {{
      color: rgba(127, 147, 168, 0.3);
      cursor: not-allowed;
    }}

    .top-nav-separator {{
      color: rgba(142, 246, 255, 0.15);
    }}

    .back-link {{
      color: var(--cyan);
      text-decoration: none;
      font-family: var(--font-mono);
      font-size: 0.9rem;
      transition: color 0.2s;
      border-bottom: none !important;
    }}

    .back-link:hover {{
      color: var(--text);
      border-bottom: none !important;
    }}

    h1, h2, h3, h4, h5, h6 {{
      color: var(--text);
      font-weight: 600;
      margin-top: 2rem;
      margin-bottom: 1rem;
    }}

    h1 {{
      font-size: 2.2rem;
      margin-top: 0;
      letter-spacing: -0.02em;
    }}

    h2 {{
      font-size: 1.6rem;
      border-bottom: 1px solid rgba(142, 246, 255, 0.1);
      padding-bottom: 0.4rem;
    }}

    h3 {{
      font-size: 1.25rem;
    }}

    p, li {{
      color: var(--muted);
      font-size: 1.05rem;
    }}

    a {{
      color: var(--cyan);
      text-decoration: none;
      border-bottom: 1px dotted rgba(142, 246, 255, 0.4);
    }}

    a:hover {{
      color: var(--text);
      border-bottom-style: solid;
    }}

    ul, ol {{
      padding-left: 1.5rem;
      margin-bottom: 1.5rem;
    }}

    li {{
      margin-bottom: 0.5rem;
    }}

    code {{
      font-family: var(--font-mono);
      background-color: var(--ink-2);
      border: 1px solid var(--line);
      padding: 0.15rem 0.35rem;
      border-radius: 4px;
      font-size: 0.9rem;
      color: var(--cyan);
    }}

    pre {{
      background-color: var(--ink-2);
      border: 1px solid var(--line);
      padding: 1.2rem;
      border-radius: 8px;
      overflow-x: auto;
      margin: 1.5rem 0;
    }}

    pre code {{
      background-color: transparent;
      border: none;
      padding: 0;
      color: var(--text);
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 2rem 0;
      font-size: 0.95rem;
    }}

    th, td {{
      padding: 0.75rem 1rem;
      border: 1px solid var(--line);
      text-align: left;
    }}

    th {{
      background-color: rgba(142, 246, 255, 0.05);
      color: var(--cyan);
      font-weight: 600;
    }}

    tr:nth-child(even) {{
      background-color: rgba(255, 255, 255, 0.01);
    }}

    blockquote {{
      border-left: 4px solid var(--cyan);
      margin: 1.5rem 0;
      padding: 0.5rem 0 0.5rem 1.5rem;
      background-color: rgba(142, 246, 255, 0.02);
      border-radius: 0 4px 4px 0;
    }}

    blockquote p {{
      margin: 0;
      font-style: italic;
    }}

    /* Pagination CSS */
    .pagination-nav {{
      display: flex;
      justify-content: space-between;
      gap: 1.5rem;
      margin-top: 4rem;
      border-top: 1px solid var(--line);
      padding-top: 2rem;
    }}

    .nav-prev, .nav-next {{
      flex: 1;
      display: flex;
      flex-direction: column;
      text-decoration: none;
      border-bottom: none !important;
    }}

    .nav-next {{
      align-items: flex-end;
      text-align: right;
    }}

    .nav-label {{
      font-size: 0.75rem;
      color: var(--dim);
      text-transform: uppercase;
      font-family: var(--font-mono);
      margin-bottom: 0.35rem;
    }}

    .nav-title {{
      font-size: 1.05rem;
      color: var(--cyan);
      font-weight: 600;
      transition: color 0.2s, transform 0.2s;
    }}

    .nav-prev:hover .nav-title {{
      color: var(--text);
      transform: translateX(-4px);
    }}

    .nav-next:hover .nav-title {{
      color: var(--text);
      transform: translateX(4px);
    }}

    footer {{
      margin-top: 4rem;
      border-top: 1px solid var(--line);
      padding-top: 1.5rem;
      text-align: center;
      color: var(--dim);
      font-family: var(--font-mono);
      font-size: 0.85rem;
    }}

    @media (max-width: 720px) {{
      .site-header {{
        top: 12px;
        padding: 0.55rem 1.1rem;
        margin-bottom: 2rem;
        font-size: 0.9rem;
      }}
      .back-link {{
        font-size: 0.8rem;
      }}
      .top-nav-group {{
        font-size: 0.75rem;
        gap: 0.5rem;
      }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <header class="site-header">
      <a class="back-link" href="{back_depth}index.html">← Back to Console</a>
      <div class="top-nav-group">
        {top_prev_html}
        <span class="top-nav-separator">|</span>
        {top_next_html}
      </div>
    </header>
    <main>
      {content}
    </main>

    <footer>
      BoundaryKit security substrate · open-source verification receipt
    </footer>
  </div>
</body>
</html>
"""

def extract_title(html_content, default="spec"):
    match = re.search(r'<h1[^>]*>(.*?)</h1>', html_content, re.IGNORECASE | re.DOTALL)
    if match:
        return re.sub('<[^<]+?>', '', match.group(1)).strip()
    return default

def extract_description(html_content, fallback):
    match = re.search(r'<p>(.*?)</p>', html_content, re.IGNORECASE | re.DOTALL)
    if not match:
        return fallback
    text = re.sub('<[^<]+?>', '', match.group(1))
    text = re.sub(r'\s+', ' ', text).strip()
    if not text:
        return fallback
    if len(text) <= 180:
        return text
    truncated = text[:177].rsplit(' ', 1)[0].rstrip('.,;:')
    return f"{truncated}..."

def compile_file(src_path, dest_path, back_depth, prev_info, next_html_info):
    with open(src_path, 'r', encoding='utf-8') as f:
        md_text = f.read()
    
    # Resolve absolute-looking github links to local HTML links
    md_text = re.sub(
        r'https://github.com/sambegui/agent-vm/blob/main/docs/architecture/(\d+)-([a-zA-Z0-9_-]+)\.md',
        r'\1-\2.html',
        md_text
    )
    md_text = re.sub(
        r'https://github.com/sambegui/agent-vm/blob/main/docs/([a-zA-Z0-9_-]+)\.md',
        r'../\1.html',
        md_text
    )
    md_text = re.sub(
        r'https://github.com/sambegui/agent-vm/blob/main/docs/evidence/([a-zA-Z0-9_-]+)\.md',
        r'../evidence/\1.html',
        md_text
    )

    # Resolve links to repo source files outside the docs tree (../../<path>) to
    # absolute GitHub blob URLs. The published static site contains only rendered
    # docs, not the source tree, so these would otherwise 404.
    md_text = re.sub(
        r'\]\(\.\./\.\./([^)]+)\)',
        r'](https://github.com/sambegui/agent-vm/blob/main/\1)',
        md_text
    )

    # Resolve local relative links
    md_text = re.sub(r'(?<!\.)\.\./([a-zA-Z0-9_-]+)\.md', r'../\1.html', md_text)
    md_text = re.sub(r'(?<![a-zA-Z0-9_/-])evidence/([a-zA-Z0-9_-]+)\.md', r'evidence/\1.html', md_text)
    md_text = re.sub(r'(\d+)-([a-zA-Z0-9_-]+)\.md', r'\1-\2.html', md_text)
    md_text = re.sub(r'(?<!/)(?<![a-zA-Z0-9_-])([a-zA-Z0-9_-]+)\.md', r'\1.html', md_text)

    html_body = markdown.markdown(md_text, extensions=['tables', 'fenced_code', 'toc'])
    title = extract_title(html_body)
    description = escape(extract_description(html_body, title), quote=True)
    
    # Generate pagination HTML
    prev_html = ""
    if prev_info:
        prev_label, prev_link = prev_info
        # Prepend back_depth to target site-root-relative link
        prev_html = f"""
      <a href="{back_depth}{prev_link}" class="nav-prev">
        <span class="nav-label">← Previous Spec</span>
        <span class="nav-title">{prev_label}</span>
      </a>
        """
    else:
        # Keep an empty div so the flexbox grid aligns 'next' to the right!
        prev_html = "<div></div>"
        
    next_html = ""
    if next_html_info:
        next_label, next_link = next_html_info
        # Prepend back_depth to target site-root-relative link
        next_html = f"""
      <a href="{back_depth}{next_link}" class="nav-next">
        <span class="nav-label">Next Spec →</span>
        <span class="nav-title">{next_label}</span>
      </a>
        """
    else:
        next_html = "<div></div>"

    # Generate top-nav compact HTML
    top_prev_html = ""
    if prev_info:
        prev_label, prev_link = prev_info
        top_prev_html = f'<a href="{back_depth}{prev_link}" class="top-nav-link" title="{prev_label}">← Prev</a>'
    else:
        top_prev_html = '<span class="top-nav-link disabled">← Prev</span>'

    top_next_html = ""
    if next_html_info:
        next_label, next_link = next_html_info
        top_next_html = f'<a href="{back_depth}{next_link}" class="top-nav-link" title="{next_label}">Next →</a>'
    else:
        top_next_html = '<span class="top-nav-link disabled">Next →</span>'

    full_html = TEMPLATE.format(
        title=title,
        description=description,
        content=html_body,
        back_depth=back_depth,
        prev_html=prev_html,
        next_html=next_html,
        top_prev_html=top_prev_html,
        top_next_html=top_next_html
    )
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(full_html)

def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    site_dir = os.path.join(repo_root, 'site')
    docs_dir = os.path.join(repo_root, 'docs')
    
    # Exact documentation chain in sequence: (rel_src_path, rel_dest_path, back_depth, display_title)
    files_to_compile = [
        ('architecture/00-overview.md', 'docs/architecture/00-overview.html', '../../', '00 — Overview'),
        ('architecture/01-isolation-substrate.md', 'docs/architecture/01-isolation-substrate.html', '../../', '01 — Isolation Substrate'),
        ('architecture/02-promotion-control-plane.md', 'docs/architecture/02-promotion-control-plane.html', '../../', '02 — Promotion Control Plane'),
        ('architecture/03-gateway-runtime-layout.md', 'docs/architecture/03-gateway-runtime-layout.html', '../../', '03 — Gateway Runtime Layout'),
        ('architecture/04-production-governance.md', 'docs/architecture/04-production-governance.html', '../../', '04 — Production Governance'),
        ('architecture/05-secure-gated-agent-preview-access.md', 'docs/architecture/05-secure-gated-agent-preview-access.html', '../../', '05 — Gated Preview Access'),
        ('security-methodology.md', 'docs/security-methodology.html', '../', 'Security Methodology'),
        ('threat-model.md', 'docs/threat-model.html', '../', 'Threat Model'),
        ('verification.md', 'docs/verification.html', '../', 'Verification Model'),
        ('evidence/governed-agent-workload-case-study.md', 'docs/evidence/governed-agent-workload-case-study.html', '../../', 'Governed Workload Case Study'),
        ('evidence/substrate-validation-receipt.md', 'docs/evidence/substrate-validation-receipt.html', '../../', 'Evidence Receipt')
    ]
    
    for i, (rel_src, rel_dest, depth, display_title) in enumerate(files_to_compile):
        src = os.path.join(docs_dir, rel_src)
        dest = os.path.join(site_dir, rel_dest)
        
        # Calculate previous link info
        prev_info = None
        if i > 0:
            prev_info = (files_to_compile[i - 1][3], files_to_compile[i - 1][1])
            
        # Calculate next link info
        next_html_info = None
        if i < len(files_to_compile) - 1:
            next_html_info = (files_to_compile[i + 1][3], files_to_compile[i + 1][1])
            
        if os.path.exists(src):
            compile_file(src, dest, depth, prev_info, next_html_info)
            print(f"Successfully compiled {rel_src} with prev/next navigation.")
        else:
            print(f"Error: Source file {src} not found!", file=sys.stderr)
            raise SystemExit(1)

if __name__ == '__main__':
    main()
