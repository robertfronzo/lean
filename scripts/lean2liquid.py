#!/usr/bin/env python3
# lean (.lean) -> liquid (.liquid) micro-transpiler
# credit: robert julian fronzo 2025

import sys, re

def fix_filters(s: str) -> str:
    return s.replace("|>", "|")

def render_line(s: str):
    m = re.match(r"^\s*render\s+(.+)$", s)
    if not m: return None
    rest = m.group(1).strip()
    snippet, args = rest, ""
    if "," in rest:
        i = rest.index(",")
        snippet = rest[:i].strip()
        args = rest[i+1:].strip()
    if args:
        parts = []
        for p in args.split(","):
            if ":" in p:
                k, v = p.split(":", 1)
                parts.append(f"{k.strip()}: {v.strip()}")
            else:
                parts.append(p.strip())
        return "{% render " + snippet + ", " + ", ".join(parts) + " %}"
    return "{% render " + snippet + " %}"

def assign_line(s: str):
    m = re.match(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:=\s*(.+)$", s)
    if not m: return None
    name, val = m.group(1), fix_filters(m.group(2).strip())
    return "{% assign " + name + " = " + val + " %}"

def equals_output_line(s: str):
    s_strip = s.strip()
    if s_strip.startswith("="):
        expr = s_strip[1:].strip()
        return "{{ " + fix_filters(expr) + " }}"
    return None

def comment_line(s: str):
    s_strip = s.strip()
    if s_strip.startswith("//"):
        body = s_strip[2:].strip()
        return "{% comment %}" + body + "{% endcomment %}"
    return None

OPENERS = [
    (re.compile(r"^\s*if\s+(.+):\s*$"), lambda g: "{% if " + fix_filters(g[0].strip()) + " %}", "if"),
    (re.compile(r"^\s*elsif\s+(.+):\s*$"), lambda g: "{% elsif " + fix_filters(g[0].strip()) + " %}", "elsif"),
    (re.compile(r"^\s*else:\s*$"), lambda g: "{% else %}", "else"),
    (re.compile(r"^\s*for\s+([A-Za-z_][A-Za-z0-9_]*)\s+in\s+(.+):\s*$"), lambda g: "{% for " + g[0] + " in " + fix_filters(g[1].strip()) + " %}", "for"),
    (re.compile(r"^\s*case\s+(.+):\s*$"), lambda g: "{% case " + fix_filters(g[0].strip()) + " %}", "case"),
    (re.compile(r"^\s*when\s+(.+):\s*$"), lambda g: "{% when " + fix_filters(g[0].strip()) + " %}", "when"),
    (re.compile(r"^\s*capture\s+([A-Za-z_][A-Za-z0-9_]*):\s*$"), lambda g: "{% capture " + g[0] + " %}", "capture"),
]

CLOSE_FOR = {
    "if": "{% endif %}",
    "for": "{% endfor %}",
    "case": "{% endcase %}",
    "capture": "{% endcapture %}",
}

def try_open(line: str):
    for rx, fn, kind in OPENERS:
        m = rx.match(line)
        if m:
            return fn(m.groups()), kind
    return None, None

def transpile(src: str) -> str:
    out = []
    stack = []
    lines = src.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]

        # schema passthrough: "schema:" ... "endschema"
        if line.strip().startswith("schema:"):
            # inline or block
            json_part = line.split("schema:", 1)[1].lstrip()
            if json_part:
                out.append("{% schema %}")
                out.append(json_part)
                i += 1
                while i < len(lines) and lines[i].strip().lower() != "endschema":
                    out.append(lines[i]); i += 1
                out.append("{% endschema %}")
                if i < len(lines) and lines[i].strip().lower() == "endschema":
                    i += 1
                continue
            else:
                i += 1
                buf = []
                while i < len(lines) and lines[i].strip().lower() != "endschema":
                    buf.append(lines[i]); i += 1
                out.append("{% schema %}")
                out.extend(buf)
                out.append("{% endschema %}")
                if i < len(lines) and lines[i].strip().lower() == "endschema":
                    i += 1
                continue

        if line.strip().lower() == "end":
            # close last proper block, skipping transient tokens
            while stack and stack[-1] in ("elsif","else","when"):
                stack.pop()
            if stack:
                out.append(CLOSE_FOR.get(stack.pop(), "{% endraw %}"))
            i += 1
            continue

        c = comment_line(line)
        if c:
            out.append(c); i += 1; continue

        eo = equals_output_line(line)
        if eo:
            out.append(eo); i += 1; continue

        al = assign_line(line)
        if al:
            out.append(al); i += 1; continue

        rl = render_line(line)
        if rl:
            out.append(rl); i += 1; continue

        op, kind = try_open(line)
        if op:
            out.append(op)
            stack.append(kind)
            i += 1
            continue

        out.append(fix_filters(line))
        i += 1

    while stack:
        k = stack.pop()
        if k in CLOSE_FOR:
            out.append(CLOSE_FOR[k])
    return "\n".join(out)

def main():
    if len(sys.argv) < 2:
        print("usage: lean2liquid.py input.lean > output.liquid", file=sys.stderr)
        sys.exit(1)
    src = open(sys.argv[1], "r", encoding="utf-8").read()
    print(transpile(src))

if __name__ == "__main__":
    main()
