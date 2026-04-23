#!/usr/bin/env python3
"""Migrate Octopress posts to Hugo format."""
import os
import re
import sys
import shutil
import yaml

SRC_POSTS = "/home/gokr/git/octopress/source/_posts"
DST_POSTS = "/home/gokr/git/roadslesstaken/content/posts"
SRC_PAGES = "/home/gokr/git/octopress/source"
DST_PAGES = "/home/gokr/git/roadslesstaken/content"
SRC_STATIC = "/home/gokr/git/octopress/source"
DST_STATIC = "/home/gokr/git/roadslesstaken/static"

os.makedirs(DST_POSTS, exist_ok=True)

def convert_front_matter(src_path, dst_path, is_page=False):
    with open(src_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # Split front matter
    if not content.startswith('---'):
        # No front matter - just copy with minimal Hugo FM
        fm = {'title': '', 'date': '2009-01-01'}
        if is_page:
            fm['draft'] = False
        new_content = '---\n' + yaml.dump(fm, default_flow_style=False, allow_unicode=True).strip() + '\n---\n' + content
        with open(dst_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return

    parts = content.split('---', 2)
    if len(parts) < 3:
        print(f"  WARNING: could not parse front matter in {src_path}")
        return

    raw_fm = parts[1]
    body = parts[2]

    try:
        fm = yaml.safe_load(raw_fm)
    except Exception as e:
        print(f"  WARNING: YAML parse error in {src_path}: {e}")
        return

    if not isinstance(fm, dict):
        print(f"  WARNING: front matter not a dict in {src_path}")
        return

    # Build new Hugo front matter
    new_fm = {}

    # Title
    if 'title' in fm:
        new_fm['title'] = fm['title']

    # Date
    if 'date' in fm:
        d = fm['date']
        if isinstance(d, str):
            # Normalize date format
            d = d.strip()
            # Handle "2011-03-12 00:24:07" format
            if re.match(r'^\d{4}-\d{2}-\d{2}\s', d):
                d = d.split()[0]
            # Handle other odd formats
            d = re.sub(r'[^0-9T:.-]', '', d[:19])
        new_fm['date'] = str(d)

    # Slug → used for URL
    if 'slug' in fm:
        new_fm['slug'] = fm['slug']

    # Categories → keep as categories
    if 'categories' in fm:
        cats = fm['categories']
        if isinstance(cats, str):
            cats = [c.strip() for c in cats.split(',')]
        new_fm['categories'] = cats

    # Tags (if present)
    if 'tags' in fm and fm['tags']:
        tags = fm['tags']
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(',')]
        if tags:
            new_fm['tags'] = tags

    # Published / draft
    if 'published' in fm and fm['published'] is False:
        new_fm['draft'] = True

    # Remove Octopress-specific keys
    # (layout, comments, wordpress_id, slug is kept)

    # Write Hugo file
    new_content = '---\n' + yaml.dump(new_fm, default_flow_style=False, allow_unicode=True, sort_keys=False).strip() + '\n---\n' + body.lstrip('\n')

    with open(dst_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    status = "DRAFT" if new_fm.get('draft') else "OK"
    print(f"  [{status}] {os.path.basename(dst_path)}")


def migrate_posts():
    print("=== Migrating posts ===")
    for fname in sorted(os.listdir(SRC_POSTS)):
        if fname.endswith('~'):
            continue
        src = os.path.join(SRC_POSTS, fname)
        if not os.path.isfile(src):
            continue

        # Hugo uses the filename for date+slug, but since Octopress already
        # has YYYY-MM-DD-slug format, we just rename .markdown → .md
        base = fname
        if base.endswith('.markdown'):
            base = base[:-len('.markdown')] + '.md'
        elif base.endswith('.textile'):
            base = base[:-len('.textile')] + '.md'

        dst = os.path.join(DST_POSTS, base)

        # Special case: ni-in-depth.md has no date prefix
        if not re.match(r'^\d{4}-\d{2}-\d{2}', base):
            print(f"  FIXING: {base} has no date prefix, adding 2015-09-22")
            base = '2015-09-22-' + base

        dst = os.path.join(DST_POSTS, base)
        convert_front_matter(src, dst)


def migrate_pages():
    print("\n=== Migrating pages ===")
    page_dirs = ['about', 'smalltalk', 'spry', 'dart', 'nim', 'ni', 'evothings', 'messaging']
    for dirname in page_dirs:
        src_dir = os.path.join(SRC_PAGES, dirname)
        if not os.path.isdir(src_dir):
            continue

        dst_dir = os.path.join(DST_PAGES, dirname)
        os.makedirs(dst_dir, exist_ok=True)

        # Look for index.markdown or index.md
        for ext in ['markdown', 'md', 'html']:
            idx = os.path.join(src_dir, f'index.{ext}')
            if os.path.isfile(idx):
                dst_idx = os.path.join(dst_dir, 'index.md')
                convert_front_matter(idx, dst_idx, is_page=True)
                break
            # Also try _index for Hugo bundle
        else:
            # Create a simple index if no source found
            print(f"  No index found for {dirname}, creating placeholder")
            with open(os.path.join(dst_dir, 'index.md'), 'w') as f:
                f.write(f'---\ntitle: "{dirname.capitalize()}"\n---\n')

        # Copy images from page dirs
        for f in os.listdir(src_dir):
            src_f = os.path.join(src_dir, f)
            if os.path.isfile(src_f) and not f.startswith('index.'):
                dst_f = os.path.join(dst_dir, f)
                static_dst = os.path.join(DST_STATIC, dirname, f)
                os.makedirs(os.path.dirname(static_dst), exist_ok=True)
                shutil.copy2(src_f, static_dst)
                print(f"  Copied asset: {dirname}/{f}")


def migrate_static():
    print("\n=== Migrating static assets ===")
    # Copy /images, /pics, /files, /assets, /javascripts
    for dirname in ['images', 'pics', 'files', 'assets', 'javascripts']:
        src_dir = os.path.join(SRC_STATIC, dirname)
        if os.path.isdir(src_dir):
            dst_dir = os.path.join(DST_STATIC, dirname)
            if os.path.exists(dst_dir):
                shutil.rmtree(dst_dir)
            shutil.copytree(src_dir, dst_dir)
            count = sum(1 for _ in os.walk(dst_dir) for f in _[2])
            print(f"  Copied {dirname}/ ({count} files)")

    # Copy favicon
    favicon = os.path.join(SRC_STATIC, 'favicon.png')
    if os.path.isfile(favicon):
        shutil.copy2(favicon, os.path.join(DST_STATIC, 'favicon.png'))
        print("  Copied favicon.png")

    # Copy robots.txt
    robots = os.path.join(SRC_STATIC, 'robots.txt')
    if os.path.isfile(robots):
        shutil.copy2(robots, os.path.join(DST_STATIC, 'robots.txt'))
        print("  Copied robots.txt")

    # Copy /a directory (likely old wordpress uploads)
    a_dir = os.path.join(SRC_STATIC, 'a')
    if os.path.isdir(a_dir):
        dst = os.path.join(DST_STATIC, 'a')
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(a_dir, dst)
        count = sum(1 for _ in os.walk(dst) for f in _[2])
        print(f"  Copied a/ ({count} files)")


if __name__ == '__main__':
    migrate_posts()
    migrate_pages()
    migrate_static()
    print("\nMigration complete!")
