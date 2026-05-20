# Step-by-Step Guide to Strengthen Kayla Greavu's Portfolio

This package updates the portfolio so it better matches a senior-level analytics and data science resume.

## Files Included

- index.html
- style.css
- README.md
- CASE_STUDY_TEMPLATE.md
- DASHBOARD_CASE_STUDIES.md
- GITHUB_PROFILE_README.md
- STEP_BY_STEP_GUIDE.md

## Step 1: Back up your current portfolio

Go to your repository:

```text
https://github.com/PaperCrane-Design/kayla-greavu-portfolio
```

Download the current version:

```text
Code > Download ZIP
```

Or clone it locally:

```bash
git clone https://github.com/PaperCrane-Design/kayla-greavu-portfolio.git
cd kayla-greavu-portfolio
```

## Step 2: Create a new branch

```bash
git checkout -b recruiter-strengthening-update
```

If editing directly in GitHub, you can skip this step.

## Step 3: Replace index.html

Replace your current:

```text
index.html
```

with the included new:

```text
index.html
```

This adds:

- Senior Data Scientist positioning
- Recruiter-focused hero section
- Impact metrics
- About section aligned to your resume
- Selected experience section
- AI and analytics case studies
- Tableau dashboard section
- Core competencies
- Certifications
- Tableau Public link

## Step 4: Replace style.css

Replace your current:

```text
style.css
```

with the included new:

```text
style.css
```

This adds:

- Better contrast
- More polished enterprise-style layout
- Improved dark/light theme
- Responsive project cards
- Stronger hero banner readability
- Better mobile layout

## Step 5: Replace README.md

Replace your current:

```text
README.md
```

with the included new:

```text
README.md
```

This makes the GitHub repository itself sound more professional.

## Step 6: Add your resume PDF

Export your resume as:

```text
Kayla_Greavu_Resume_2026.pdf
```

Upload it to the root of the repo.

The resume button in the HTML points here:

```html
<a class="button secondary" href="Kayla_Greavu_Resume_2026.pdf" target="_blank">Download Resume</a>
```

If you want a different file name, update that link.

## Step 7: Update your LinkedIn URL

In `index.html`, find:

```html
<a href="https://www.linkedin.com/" target="_blank">LinkedIn</a>
```

Replace it with your actual LinkedIn profile link.

## Step 8: Confirm project file names

The HTML links to:

```text
DSC680_Milestone3_Presentation_v2.mp4
DSC680_Milestone3_WhitePaper_KaylaGreavu.docx
DSC680_Milestone3_KaylaGreavu.ipynb
```

Make sure those files still exist in your repo.

## Step 9: Commit and push

```bash
git add .
git commit -m "Strengthen portfolio for senior data science recruiters"
git push origin recruiter-strengthening-update
```

## Step 10: Merge into main

```bash
git checkout main
git merge recruiter-strengthening-update
git push origin main
```

## Step 11: Confirm GitHub Pages

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

Your portfolio should update at:

```text
https://papercrane-design.github.io/kayla-greavu-portfolio/
```

## Step 12: Review the live site

Check:

- Hero banner is readable
- Resume button works
- Tableau dashboard buttons work
- Project files open correctly
- Mobile layout looks clean
- Light/dark mode works
- Your email is correct
- LinkedIn link is updated

## Step 13: Recommended next additions

Add these next:

1. One SQL case study
2. One Power BI or Tableau dashboard screenshot gallery
3. A dedicated case study page for the AI Marketing Assistant
4. A sanitized operational analytics case study
5. A GitHub profile README using the included template
