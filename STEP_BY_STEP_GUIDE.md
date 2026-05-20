# Step-by-Step Guide to Update Kayla Greavu's Portfolio

This guide updates the portfolio from a student-style analytics portfolio into a senior data science and analytics leadership portfolio.

## Step 1: Download your current repository

Go to:

```text
https://github.com/PaperCrane-Design/kayla-greavu-portfolio
```

Click:

```text
Code > Download ZIP
```

Or clone it locally:

```bash
git clone https://github.com/PaperCrane-Design/kayla-greavu-portfolio.git
cd kayla-greavu-portfolio
```

## Step 2: Create a safe update branch

```bash
git checkout -b senior-portfolio-update
```

## Step 3: Replace your homepage file

Replace your current `index.html` with the included `index.html`.

This adds senior positioning, experience highlights, business impact, case studies, competencies, and certifications.

## Step 4: Replace your CSS file

Replace your current `style.css` with the included `style.css`.

This fixes the banner contrast issue and adds a more mature dark/light executive-style design.

## Step 5: Add your resume PDF

Export your resume as PDF and name it exactly:

```text
Kayla_Greavu_Resume_2026.pdf
```

Put it in the root folder of the portfolio repository.

The homepage button already links to this file:

```html
<a class="button secondary" href="Kayla_Greavu_Resume_2026.pdf" target="_blank">Download Resume</a>
```

## Step 6: Replace your repository README

Replace the current `README.md` with the included `README.md`.

## Step 7: Confirm existing project files still match

The HTML links to these project files:

```text
DSC680_Milestone3_Presentation_v2.mp4
DSC680_Milestone3_WhitePaper_KaylaGreavu.docx
DSC680_Milestone3_KaylaGreavu.ipynb
```

Make sure those files still exist in your repo.

## Step 8: Update LinkedIn link

In `index.html`, find:

```html
<a href="https://www.linkedin.com/" target="_blank">LinkedIn</a>
```

Replace it with your actual LinkedIn URL.

## Step 9: Check your email

The files use:

```text
greavukayla@gmail.com
```

Update this if you want a different professional email.

## Step 10: Commit and push changes

```bash
git add .
git commit -m "Update portfolio for senior data scientist positioning"
git push origin senior-portfolio-update
```

## Step 11: Merge into main

```bash
git checkout main
git merge senior-portfolio-update
git push origin main
```

## Step 12: Confirm GitHub Pages settings

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

Your live site should update at:

```text
https://papercrane-design.github.io/kayla-greavu-portfolio/
```

## Step 13: Review the live site

Check:

- Hero text is readable
- Resume download works
- Project links work
- Contact links work
- Mobile layout looks good
- Light/dark toggle works

## Step 14: Recommended next improvements

1. Add a dedicated case study page for the AI Marketing Assistant
2. Add a SQL analytics project
3. Add a dashboard screenshot section
4. Add a professional LinkedIn link
5. Add a GitHub profile README matching this branding
6. Add sanitized professional case studies from military experience without exposing sensitive details

## Step 15: Phrase military experience safely

Use:

```text
Led analytics initiatives supporting global real-time operational decision systems.
```

Avoid mission names, system names, classified details, sensitive datasets, or internal architecture.

## Step 16: Keep this positioning consistent

Use:

```text
Senior Data Scientist | Analytics Strategist | Generative AI & Predictive Modeling
```

Do not use:

```text
Junior Data Analyst
Aspiring Data Scientist
Student Portfolio
Entry-Level Analyst
```
