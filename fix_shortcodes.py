#!/usr/bin/env python3
"""Fix Octopress shortcodes in migrated Hugo posts."""
import re
import os
import glob

POSTS_DIR = "/home/gokr/git/roadslesstaken/content/posts"

def fix_codeblocks(content):
    """Convert {% codeblock title lang:xxx %} ... {% endcodeblock %} to ```xxx ... ```"""
    pattern = re.compile(
        r'\{%\s*codeblock\s+([^%]*?)\s*%\}\s*\n(.*?)\{%\s*endcodeblock\s*%\}',
        re.DOTALL
    )

    def replacer(m):
        params = m.group(1).strip()
        code = m.group(2)

        # Extract lang from "lang:xxx" parameter
        lang = ''
        for part in params.split():
            if part.startswith('lang:'):
                lang = part[5:]

        # Clean up trailing newlines in code
        code = code.rstrip('\n')

        return f'```{lang}\n{code}\n```'

    return pattern.sub(replacer, content)


def fix_images(content):
    """Convert {% img class /path/to/img [width [height]] title %} to ![title](/path/to/img)"""
    # Pattern: {% img [class] /path [width] [height] title %}
    # The class can be: left, right, center
    # title may be quoted with single quotes
    pattern = re.compile(
        r'\{%\s*img\s+([^%]+?)\s*%\}'
    )

    def replacer(m):
        raw = m.group(1).strip()

        # Split by whitespace but respect single-quoted strings
        parts = []
        current = ''
        in_quote = False
        quote_char = None
        for ch in raw:
            if ch in ("'", '"') and not in_quote:
                in_quote = True
                quote_char = ch
                continue
            elif ch == quote_char and in_quote:
                in_quote = False
                quote_char = None
                continue
            elif ch == ' ' and not in_quote:
                if current:
                    parts.append(current)
                    current = ''
                continue
            current += ch
        if current:
            parts.append(current)

        # First part might be class (left/right/center) or a path
        idx = 0
        if parts and parts[0] in ('left', 'right', 'center'):
            cls = parts[0]
            idx = 1
        else:
            cls = None

        # Next is path (starts with / or http)
        path = parts[idx] if idx < len(parts) else ''
        idx += 1

        # Remaining parts: could be width, height, title
        # Width and height are numeric
        title = ''
        while idx < len(parts):
            p = parts[idx]
            if p.isdigit():
                idx += 1
                continue
            if not title:
                title = p
            idx += 1

        if cls == 'left':
            style = ' style="float:left; margin:0 1em 1em 0;"'
        elif cls == 'right':
            style = ' style="float:right; margin:0 0 1em 1em;"'
        elif cls == 'center':
            style = ' style="display:block; margin:0 auto;"'
        else:
            style = ''

        alt = title if title else os.path.splitext(os.path.basename(path))[0]
        return f'![{alt}]({path}){{{style}}}'

    return pattern.sub(replacer, content)


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    content = fix_codeblocks(content)
    content = fix_images(content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


if __name__ == '__main__':
    changed = 0
    for filepath in sorted(glob.glob(os.path.join(POSTS_DIR, '*.md'))):
        if process_file(filepath):
            print(f"  Fixed: {os.path.basename(filepath)}")
            changed += 1
    print(f"\nFixed {changed} files")
