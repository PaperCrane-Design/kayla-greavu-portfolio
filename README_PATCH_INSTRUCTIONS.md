# Mission Risk Analytics Patch

The live portfolio is still showing the earlier version without the new mission-risk section. Use these two files as a direct patch.

## How to apply

1. Open `index.html` in GitHub.
2. Add the nav link from `INDEX_PATCH.html`.
3. Paste the full `risk-analytics` section after your current Leadership Impact section.
4. Replace the older IT Risk Analyst paragraph with the updated paragraph in `INDEX_PATCH.html`.
5. Open `style.css`.
6. Paste everything from `STYLE_PATCH.css` at the very bottom.
7. Commit changes to the branch GitHub Pages uses, usually `main`.

## Commit message

```bash
git add .
git commit -m "Add sanitized cyber risk analytics case study"
git push
```
