# Step-by-Step Guide: Senior Metrics + AI Product Portfolio Update

This package updates your portfolio to make it look more senior-level and to integrate your Car Marketing AI product draft.

## Files Included

- index.html
- style.css
- README.md
- CAR_MARKETING_AI_CASE_STUDY.md
- SENIOR_METRICS_COPY.md
- STEP_BY_STEP_GUIDE.md

## Step 1: Back up your current portfolio

Go to:

```text
https://github.com/PaperCrane-Design/kayla-greavu-portfolio
```

Download a backup:

```text
Code > Download ZIP
```

Or clone locally:

```bash
git clone https://github.com/PaperCrane-Design/kayla-greavu-portfolio.git
cd kayla-greavu-portfolio
```

## Step 2: Create an update branch

```bash
git checkout -b senior-metrics-ai-update
```

## Step 3: Replace index.html

Replace your current `index.html` with the included new version.

This adds:

- Stronger senior-level hero language
- New quantified metrics section
- Dedicated Car Marketing AI product section
- AI product roadmap
- Technical architecture card
- Stronger decision-support and product-strategy language
- More senior framing for case studies

## Step 4: Replace style.css

Replace your current `style.css` with the included new version.

This adds:

- Stronger visual hierarchy
- Metrics cards
- AI product section styling
- Architecture cards
- Product roadmap cards
- Improved spacing and responsive layout

## Step 5: Upload your AI draft PDF

Upload your PDF to the root of the portfolio repository with this exact file name:

```text
Car_Marketing_AI_-_Draft(1).pdf
```

The new HTML already links to it here:

```html
<a href="Car_Marketing_AI_-_Draft(1).pdf" target="_blank">View Draft PDF</a>
```

## Step 6: Replace README.md

Replace your current `README.md` with the included new version.

This updates your GitHub repo to match your senior-level portfolio positioning.

## Step 7: Commit and push

```bash
git add .
git commit -m "Add senior metrics and Car Marketing AI product case study"
git push origin senior-metrics-ai-update
```

## Step 8: Merge into main

```bash
git checkout main
git merge senior-metrics-ai-update
git push origin main
```

## Step 9: Confirm GitHub Pages

Go to:

```text
Repository > Settings > Pages
```

Confirm:

```text
Source: Deploy from branch
Branch: main
Folder: /root
```

## Step 10: Test the live site

Visit:

```text
https://papercrane-design.github.io/kayla-greavu-portfolio/
```

Check:

- The metrics section appears
- The AI Product section appears
- The AI draft PDF opens
- Dashboard links work
- Resume link works
- Mobile layout looks clean
- Light/dark toggle still works

## Recommended Next Improvements

1. Rename the AI draft PDF to a cleaner filename.
2. Add screenshots or wireframes of the Car Marketing AI dashboard.
3. Build a simple working prototype page for the AI product.
4. Add a SQL case study to strengthen the technical evidence.
5. Add a one-page product brief PDF for recruiters.
