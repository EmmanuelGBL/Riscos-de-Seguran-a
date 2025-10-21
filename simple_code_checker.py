# simple_code_checker.py
import re
import sys
from pathlib import Path

PATTERNS = [
    ("__name_misspelled", re.compile(r"\b_name_\b|\b_if\s+_name_\b", re.IGNORECASE)),
    (
        "render_template_string_used",
        re.compile(r"\brender_template_string\(", re.IGNORECASE),
    ),
    ("debug_true", re.compile(r"app\.run\([^)]*debug\s*=\s*True", re.IGNORECASE)),
    (
        "hardcoded_passwords",
        re.compile(
            r"['\"](?:senha|password|pass|pwd)['\"]\s*:\s*['\"][^'\"]+['\"]",
            re.IGNORECASE,
        ),
    ),
    (
        "secret_key_hardcoded",
        re.compile(r"app\.secret_key\s*=\s*['\"][^'\"]+['\"]", re.IGNORECASE),
    ),
]


def analyze(file_path):
    text = Path(file_path).read_text(encoding="utf-8")
    findings = []
    for name, pat in PATTERNS:
        m = pat.search(text)
        if m:
            findings.append((name, m.group(0), m.start()))
    return findings


def main():
    if len(sys.argv) < 2:
        print("Usage: python simple_code_checker.py <file.py>")
        sys.exit(1)
    file = sys.argv[1]
    findings = analyze(file)
    if not findings:
        print("Nenhuma issue simples encontrada.")
    else:
        print("Relatório de checagem simples:")
        for f in findings:
            print(f"- {f[0]} -> trecho: {f[1]!r} (pos {f[2]})")


if __name__ == "__main__":
    main()
