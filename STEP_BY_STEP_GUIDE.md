# Step-by-Step Guide: Revamp Kayla Greavu's GitHub Portfolio

## Step 1: Back up the current portfolio

Before changing anything, download or copy the current files:

- index.html
- style.css
- README.md

You can also create a new Git branch:

```bash
git checkout -b portfolio-redesign
```

## Step 2: Replace index.html

Copy the included `index.html` file into the root of the repository.

This creates:
- A professional hero section
- Recruiter-friendly About section
- Better project cards
- Skills matrix
- Portfolio roadmap
- Contact section
- Dark/light theme toggle

## Step 3: Replace style.css

Copy the included `style.css` file into the root of the repository.

This adds:
- Modern dark/light palette
- Responsive cards
- Better spacing
- Recruiter-friendly layout
- Mobile-friendly design

## Step 4: Add your resume

Export your resume as:

```text
resume.pdf
```

Place it in the root of the repository.

The homepage button already links to:

```html
<a class="button secondary" href="resume.pdf" target="_blank">Download Resume</a>
```

## Step 5: Update project links

In `index.html`, check these lines and make sure the file names match your repository exactly:

```html
<a href="DSC680_Milestone3_KaylaGreavu.ipynb" target="_blank">View Notebook</a>
<a href="DSC680_Milestone3_WhitePaper_KaylaGreavu.docx" target="_blank">Read Report</a>
<a href="DSC680_Milestone3_Presentation_v2.mp4" target="_blank">Watch Presentation</a>
```

## Step 6: Replace README.md

Copy the included `README.md` into your repository root.

This makes the GitHub repo itself look more professional.

## Step 7: Create better project README files

For each major project, create a separate folder later:

```text
projects/
├── student-performance-prediction/
├── marketing-content-generator/
├── sql-sales-analysis/
└── weather-api-dashboard/
```

Inside each folder, use the included `PROJECT_README_TEMPLATE.md`.

## Step 8: Improve your GitHub profile

Create a new repository with the exact same name as your GitHub username or organization.

For your visible GitHub account, that may be:

```text
PaperCrane-Design
```

Then add the included `GITHUB_PROFILE_README.md` as the README.md file.

## Step 9: Commit your changes

```bash
git add .
git commit -m "Revamp portfolio with professional analytics layout"
git push origin portfolio-redesign
```

If you are editing directly on GitHub, use the green “Commit changes” button.

## Step 10: Merge to main

Once it looks good:

```bash
git checkout main
git merge portfolio-redesign
git push origin main
```

## Step 11: Check GitHub Pages

Go to:

```text
Settings > Pages
```

Confirm:
- Source is Deploy from branch
- Branch is main
- Folder is /root

Your live site should update at:

```text
https://papercrane-design.github.io/kayla-greavu-portfolio/
```

## Step 12: Add portfolio projects next

Recommended order:

1. Student Performance Prediction
2. AI-Powered Marketing Content Generator
3. SQL Sales Analysis
4. Weather API Dashboard
5. Social Media and Mental Health Analysis
6. Tableau or Power BI Dashboard

## Step 13: Rename coursework professionally

Avoid assignment-style names.

Use these instead:

- Week 4 Pandas Assignment → Retail Sales Performance Analysis
- Statistics Homework → Comparative Statistical Analysis
- API Project → Real-Time Weather Analytics Dashboard
- R Markdown Report → Business Intelligence Analytics Report
- Final Notebook → Student Performance Prediction

## Step 14: Add visuals

For every project, include:
- One chart screenshot
- One summary graphic
- One paragraph explaining the insight
- One recommendation section

## Step 15: Make recruiters' lives easy

Every project should answer:

- What problem did you solve?
- What tools did you use?
- What did you find?
- Why does it matter?
- Where can I see the code?
