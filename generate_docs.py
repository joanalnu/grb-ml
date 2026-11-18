"""Generate NumPy/Pandas-style API reference pages for an Astro Starlight site.

Requires:  pip install numpydoc
Usage:     python generate_docs.py [package ...]      (default: PACKAGES below)

Docstrings must be NumPy-style (Parameters / Returns / Raises / See Also /
Notes / Examples sections with ---- underlines).
"""
import html
import importlib
import inspect
import os
import re
import pkgutil
import shutil
import sys
from pathlib import Path

from numpydoc.docscrape import NumpyDocString

PACKAGES = ["grb_ml"]  # <- your package name(s)
DOCS_DIR = Path("docs/src/content/docs/reference")
REPO_URL = os.environ.get("REPO_URL", "")  # e.g. https://github.com/org/repo/blob/main


# --------------------------------------------------------------------------
# Discovery
# --------------------------------------------------------------------------
def get_package_modules(package_name):
    try:
        package = importlib.import_module(package_name)
    except ImportError as e:
        print(f"Skipping {package_name}: {e}")
        return []
    modules = [package.__name__]
    if hasattr(package, "__path__"):
        for _, name, _ in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
            modules.append(name)
    return modules


def extract_members(module_name):
    """Public classes/functions *defined* in the module, in source order."""
    try:
        module = importlib.import_module(module_name)
    except ImportError:
        return []
    members = []
    for name, obj in inspect.getmembers(module):
        if name.startswith("_") or inspect.ismodule(obj):
            continue
        if getattr(obj, "__module__", None) != module_name:
            continue
        if inspect.isclass(obj):
            members.append((name, "class", obj))
        elif inspect.isfunction(obj):
            members.append((name, "function", obj))

    def lineno(m):
        try:
            return inspect.getsourcelines(m[2])[1]
        except (OSError, TypeError):
            return 0

    return sorted(members, key=lineno)


# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------
def parse(obj):
    return NumpyDocString(inspect.getdoc(obj) or "")


def rst_to_md(text):
    """Convert reST math (``.. math::`` / ``:math:``) to $$..$$ / $..$ for remark-math."""
    text = re.sub(r":math:`([^`]+)`", r"$\1$", text)
    text = re.sub(r"^\.\. math::\s*(.+)$", r"$$\1$$", text, flags=re.M)
    return text


def join(lines):
    return rst_to_md("\n".join(lines).strip())


def first_sentence(obj):
    summary = join(parse(obj)["Summary"])
    return (summary or "No description available.").replace("|", "\\|")


def signature(obj, name):
    try:
        sig = str(inspect.signature(obj))
    except (ValueError, TypeError):
        sig = "(...)"
    return f"{name}{sig}"


def source_link(obj):
    if not REPO_URL:
        return ""
    try:
        path = Path(inspect.getsourcefile(obj)).resolve().relative_to(Path.cwd().resolve())
        lines, start = inspect.getsourcelines(obj)
        return f"[source]({REPO_URL}/{path.as_posix()}#L{start}-L{start + len(lines) - 1})"
    except Exception:
        return ""


# --------------------------------------------------------------------------
# Section renderers
# --------------------------------------------------------------------------
def label(text, level):
    """Top-level objects get real headings (-> Starlight TOC); methods get a styled label."""
    if level:
        return f"{'#' * level} {text}\n"
    return f'<p class="api-label">{text}</p>\n'


def render_params(items, kind):
    """items: numpydoc Parameter tuples. kind: 'params' | 'returns'."""
    out = ['<dl class="api-params">']
    for p in items:
        name = f"<dt><code>{html.escape(p.name)}</code>" if p.name else "<dt>"
        typ = f' <span class="api-type">{html.escape(p.type)}</span>' if p.type else ""
        out.append(f"{name}{typ}</dt>")
        out.append("<dd>\n")
        out.append(join(p.desc) or "")
        out.append("\n</dd>")
    out.append("</dl>\n")
    return "\n".join(out)


def render_see_also(items, local_names):
    links = []
    for funcs, desc in items:
        for fname, _role in funcs:
            short = fname.split(".")[-1]
            target = f"[`{short}`](../{short}/)" if short in local_names else f"`{fname}`"
            d = join(desc)
            links.append(f"- {target}" + (f" — {d}" if d else ""))
    return "\n".join(links) + "\n"


def render_examples(lines):
    text = join(lines)
    if ">>>" in text:
        return f"```pycon\n{text}\n```\n"
    return text + "\n"


def render_doc(obj, level, local_names, skip=()):
    """Render all docstring sections of obj. `level`=2 for pages, 0 for methods."""
    doc = parse(obj)
    out = []
    ext = join(doc["Extended Summary"])
    if ext:
        out.append(ext + "\n")

    for section, kind in (("Parameters", "params"), ("Attributes", "params"),
                          ("Returns", "returns"), ("Yields", "returns"),
                          ("Raises", "params")):
        if section in skip or not doc[section]:
            continue
        out.append(label(section, level))
        out.append(render_params(doc[section], kind))

    if doc["See Also"]:
        out.append(label("See Also", level))
        out.append(render_see_also(doc["See Also"], local_names))
    for section in ("Notes", "References"):
        if doc[section]:
            out.append(label(section, level))
            out.append(join(doc[section]) + "\n")
    if doc["Examples"]:
        out.append(label("Examples", level))
        out.append(render_examples(doc["Examples"]))
    return "\n".join(out)


def class_tables(cls):
    props, methods = [], []
    for name, member in inspect.getmembers(cls):
        if name.startswith("_"):
            continue
        if isinstance(member, property):
            props.append((name, first_sentence(member.fget) if member.fget else ""))
        elif inspect.isfunction(member) or inspect.ismethod(member):
            methods.append((name, member))
    out = []
    if props:
        out += ["## Properties\n", "| Property | Description |", "| :--- | :--- |"]
        out += [f"| `{n}` | {d} |" for n, d in props] + [""]
    if methods:
        out += ["## Methods\n", "| Method | Description |", "| :--- | :--- |"]
        out += [f"| [`{n}`](#{n.lower()}) | {first_sentence(m)} |" for n, m in methods] + [""]
    return "\n".join(out), methods


# --------------------------------------------------------------------------
# Page writers
# --------------------------------------------------------------------------
def write_page(module_name, name, kind, obj, module_dir, local_names):
    full = f"{module_name}.{name}"
    badge = "class" if kind == "class" else "function"
    meta = f'<p class="api-meta"><span class="api-badge api-badge-{badge}">{badge}</span> '
    meta += f"<code>{module_name}</code>"
    link = source_link(obj)
    meta += f" · {link}" if link else ""
    meta += "</p>"
    # a markdown link inside raw HTML isn't parsed: use an <a> instead
    if link:
        url = link[link.index("(") + 1:-1]
        meta = meta.replace(link, f'<a href="{url}">source</a>')

    parts = [
        f"---\ntitle: {name}\ndescription: {first_sentence(obj)}\n---\n",
        meta + "\n",
        f"```python\n{'class ' if kind == 'class' else ''}{signature(obj, full)}\n```\n",
        first_sentence(obj) + "\n",
        render_doc(obj, 2, local_names),
    ]

    if kind == "class":
        tables, methods = class_tables(obj)
        parts.append(tables)
        for mname, m in methods:
            parts.append(f"### {mname}\n")
            parts.append(f"```python\n{signature(m, f'{name}.{mname}')}\n```\n")
            parts.append(first_sentence(m) + "\n")
            parts.append(render_doc(m, 0, local_names))

    (module_dir / f"{name}.md").write_text("\n".join(parts), encoding="utf-8")
    print(f"  Created: {module_dir / (name + '.md')}")


def write_index(module_name, members, module_dir):
    module = importlib.import_module(module_name)
    mod_doc = inspect.getdoc(module) or f"API reference for `{module_name}`."
    lines = ["---", f"title: {module_name}", f"description: Overview of {module_name}",
             "sidebar:", "  order: 0", "---", "", mod_doc, ""]
    for heading, kind in (("Classes", "class"), ("Functions", "function")):
        rows = [(n, o) for n, k, o in members if k == kind]
        if rows:
            lines += [f"## {heading}", "", f"| {kind.title()} | Description |", "| :--- | :--- |"]
            lines += [f"| [`{n}`](./{n}/) | {first_sentence(o)} |" for n, o in rows] + [""]
    (module_dir / "index.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"  Created Module Index: {module_dir / 'index.md'}")


def main():
    packages = sys.argv[1:] or PACKAGES
    if DOCS_DIR.exists():
        shutil.rmtree(DOCS_DIR)  # drop stale pages for removed/renamed objects
    DOCS_DIR.mkdir(parents=True)

    for pkg in packages:
        pkg_name = pkg.replace("-", "_")
        print(f"\nScanning package: {pkg_name}...")
        for module_name in get_package_modules(pkg_name):
            members = extract_members(module_name)
            if not members:
                continue
            module_dir = DOCS_DIR / Path(*module_name.split("."))
            module_dir.mkdir(parents=True, exist_ok=True)
            write_index(module_name, members, module_dir)
            local_names = {n for n, _, _ in members}
            for name, kind, obj in members:
                write_page(module_name, name, kind, obj, module_dir, local_names)


if __name__ == "__main__":
    main()
