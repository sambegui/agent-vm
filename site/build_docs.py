#!/usr/bin/env python3
import os
import re
import sys

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
  <title>{title} · agent-vm specs</title>
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
      max-width: 800px;
      margin: 0 auto;
      padding: clamp(1.5rem, 5vw, 4rem) 1.5rem;
    }}

    header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 2.5rem;
      border-bottom: 1px solid var(--line);
      padding-bottom: 1rem;
    }}

    .back-link {{
      color: var(--cyan);
      text-decoration: none;
      font-family: var(--font-mono);
      font-size: 0.9rem;
      transition: color 0.2s;
    }}

    .back-link:hover {{
      color: var(--text);
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

    footer {{
      margin-top: 4rem;
      border-top: 1px solid var(--line);
      padding-top: 1.5rem;
      text-align: center;
      color: var(--dim);
      font-family: var(--font-mono);
      font-size: 0.85rem;
    }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <a class="back-link" href="{back_depth}index.html">← Back to Console</a>
      <span style="color: var(--dim); font-family: var(--font-mono); font-size: 0.85rem;">spec v1.0</span>
    </header>
    <main>
      {content}
    </main>
    <footer>
      agent-vm security substrate · open-source verification receipt
    </footer>
  </div>
</body>
</html>
"""

def extract_title(html_content, default="spec"):
    # Find the first h1 and extract its text
    match = re.search(r'<h1>(.*?)</h1>', html_content, re.IGNORECASE)
    if match:
        # Strip html tags if any
        return re.sub('<[^<]+?>', '', match.group(1)).strip()
    return default

def compile_file(src_path, dest_path, back_depth):
    print(f"Compiling {src_path} -> {dest_path}")
    with open(src_path, 'r', encoding='utf-8') as f:
        md_text = f.read()
    
    # Simple conversion of raw github blob links inside documentation to relative html links
    # For example: https://github.com/sambegui/agent-vm/blob/main/docs/architecture/00-overview.md -> 00-overview.html
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

    # Resolve local relative markdown links to relative html links as well
    md_text = re.sub(r'(\d+)-([a-zA-Z0-9_-]+)\.md', r'\1-\2.html', md_text)
    md_text = re.sub(r'(?<!/)(?<![a-zA-Z0-9_-])([a-zA-Z0-9_-]+)\.md', r'\1.html', md_text)

    # Convert Markdown to HTML
    html_body = markdown.markdown(md_text, extensions=['tables', 'fenced_code', 'toc'])
    
    title = extract_title(html_body)
    full_html = TEMPLATE.format(
        title=title,
        content=html_body,
        back_depth=back_depth
    )
    
    # Ensure destination directories exist
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(full_html)

def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    site_dir = os.path.join(repo_root, 'site')
    docs_dir = os.path.join(repo_root, 'docs')
    
    # Map sources under docs/ to destinations under site/docs/
    # format: (source_path, dest_path_under_site_docs, back_depth_to_site_root)
    files_to_compile = [
        ('architecture/00-overview.md', 'docs/architecture/00-overview.html', '../../'),
        ('architecture/01-isolation-substrate.md', 'docs/architecture/01-isolation-substrate.html', '../../'),
        ('architecture/02-promotion-control-plane.md', 'docs/architecture/02-promotion-control-plane.html', '../../'),
        ('architecture/03-gateway-runtime-layout.md', 'docs/architecture/03-gateway-runtime-layout.html', '../../'),
        ('architecture/04-production-governance.md', 'docs/architecture/04-production-governance.html', '../../'),
        ('architecture/05-secure-gated-agent-preview-access.md', 'docs/architecture/05-secure-gated-agent-preview-access.html', '../../'),
        ('security-methodology.md', 'docs/security-methodology.html', '../'),
        ('threat-model.md', 'docs/threat-model.html', '../'),
        ('verification.md', 'docs/verification.html', '../'),
        ('evidence/substrate-validation-receipt.md', 'docs/evidence/substrate-validation-receipt.html', '../../')
    ]
    
    for rel_src, rel_dest, depth in files_to_compile:
        src = os.path.join(docs_dir, rel_src)
        dest = os.path.join(site_dir, rel_dest)
        if os.path.exists(src):
            compile_file(src, dest, depth)
        else:
            print(f"Warning: Source file {src} not found!")

if __name__ == '__main__':
    main()
