done
159 original text blocks preserved
Review http://94.130.99.148:8088/ for visual approval.

- GitHub: https://github.com/danechkabe/mos-numerology
- Isolated nginx port 8088, existing port 80 site byte-identical.
- HTML, CSS and 3 deployed images match repository files exactly.
- Desktop browser 1280 × 767 CSS px: no overflow, service link opens detail panel.
- Mobile iframe 390 × 844 CSS px: no overflow, responsive heading 48 px.
- HTTP preview only, domain and TLS not configured.
- Full validation: `python3 verify.py`.

Task SSH credential reference: Jcode-managed secrets/mos-numerology-server.password. Credential value excluded from Git.
