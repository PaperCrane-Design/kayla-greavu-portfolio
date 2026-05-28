import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import accuracy_score, roc_auc_score, r2_score, mean_absolute_error
from sklearn.inspection import permutation_importance

BASE = Path('/mnt/data/week11_procurement_project')
FIG = BASE/'figures'
FIG.mkdir(exist_ok=True, parents=True)
DATA = Path('/mnt/data/Dataset_Procurement(2).xlsx')

df = pd.read_excel(DATA, sheet_name='Data')
# Clean/prepare
for c in ['PO Date','Requested Delivery','Actual Delivery','Contract Start','Contract End']:
    df[c] = pd.to_datetime(df[c], dayfirst=True, errors='coerce')
for c in ['On Time Delivery','Maverick Spend','Preferred Supplier','Single Source Flag']:
    df[c] = df[c].astype(str).str.strip().str.title()

df['on_time_flag'] = (df['On Time Delivery'] == 'Yes').astype(int)
df['late_flag'] = (df['Days Late'] > 0).astype(int)
df['maverick_flag'] = (df['Maverick Spend'] == 'Yes').astype(int)
df['preferred_flag'] = (df['Preferred Supplier'] == 'Yes').astype(int)
df['single_source_flag'] = (df['Single Source Flag'] == 'Yes').astype(int)
risk_order = {'Low': 1, 'Medium': 2, 'High': 3}
df['risk_score'] = df['Supplier Risk'].map(risk_order)

# KPIs
kpis = {
    'Procurement records': len(df),
    'Suppliers': df['Supplier Name'].nunique(),
    'Total net spend': df['Line Net'].sum(),
    'Total spend including tax': df['Line Total Inc Tax'].sum(),
    'Total savings': df['Savings Amount'].sum(),
    'Average savings percent': df['Savings Pct'].mean(),
    'On-time delivery rate': df['on_time_flag'].mean(),
    'Average days late': df['Days Late'].mean(),
    'Maverick spend rate': df['maverick_flag'].mean(),
    'Maverick net spend': df.loc[df['maverick_flag']==1, 'Line Net'].sum(),
}
pd.Series(kpis).to_csv(BASE/'kpi_summary.csv')

preferred_summary = df.groupby('Preferred Supplier').agg(
    records=('PO Number','count'),
    on_time_rate=('on_time_flag','mean'),
    average_days_late=('Days Late','mean'),
    average_savings_pct=('Savings Pct','mean'),
    total_savings=('Savings Amount','sum'),
    net_spend=('Line Net','sum')
).reset_index()
preferred_summary.to_csv(BASE/'preferred_supplier_summary.csv', index=False)

risk_summary = df.groupby('Supplier Risk').agg(
    records=('PO Number','count'),
    on_time_rate=('on_time_flag','mean'),
    late_rate=('late_flag','mean'),
    average_days_late=('Days Late','mean'),
    average_savings_pct=('Savings Pct','mean'),
    net_spend=('Line Net','sum')
).reindex(['Low','Medium','High']).reset_index()
risk_summary.to_csv(BASE/'supplier_risk_summary.csv', index=False)

maverick_summary = df.groupby('Maverick Spend').agg(
    records=('PO Number','count'),
    share_of_records=('PO Number', lambda s: len(s)/len(df)),
    net_spend=('Line Net','sum'),
    average_line_net=('Line Net','mean'),
    average_days_late=('Days Late','mean'),
    average_savings_pct=('Savings Pct','mean')
).reset_index()
maverick_summary.to_csv(BASE/'maverick_spend_summary.csv', index=False)

supplier = df.groupby('Supplier Name').agg(
    records=('PO Number','count'),
    on_time_rate=('on_time_flag','mean'),
    average_days_late=('Days Late','mean'),
    savings=('Savings Amount','sum'),
    average_savings_pct=('Savings Pct','mean'),
    average_esg_score=('Supplier ESG Score','mean'),
    average_risk_score=('risk_score','mean'),
    net_spend=('Line Net','sum')
).reset_index()
# Weighted score: reliability, savings, ESG, lower risk. Used as a business ranking aid, not a causal measure.
positive_savings_pct = supplier['average_savings_pct'].clip(lower=0)
supplier['performance_score'] = (
    supplier['on_time_rate'] * 40 +
    (positive_savings_pct / positive_savings_pct.max()) * 30 +
    (supplier['average_esg_score'] / 100) * 20 +
    ((3 - supplier['average_risk_score']) / 2) * 10
)
supplier = supplier.sort_values('performance_score', ascending=False)
supplier.to_csv(BASE/'supplier_performance_scorecard.csv', index=False)

category = df.groupby('Category').agg(
    net_spend=('Line Net','sum'),
    savings=('Savings Amount','sum'),
    on_time_rate=('on_time_flag','mean'),
    average_days_late=('Days Late','mean'),
    records=('PO Number','count')
).sort_values('net_spend', ascending=False).reset_index()
category.to_csv(BASE/'category_summary.csv', index=False)

# Regression and classification
features_num = ['Lead Time Days', 'Savings Pct', 'Line Net', 'Supplier ESG Score', 'preferred_flag', 'maverick_flag', 'single_source_flag', 'risk_score']
features_cat = ['Supplier Risk', 'Contract Type', 'Local International', 'Category', 'Payment Status']
features = features_num + features_cat
X = df[features].copy()
y_class = df['late_flag']
num_transformer = Pipeline(steps=[('scaler', StandardScaler())])
cat_transformer = Pipeline(steps=[('onehot', OneHotEncoder(handle_unknown='ignore'))])
preprocess = ColumnTransformer(transformers=[('num', num_transformer, features_num),('cat', cat_transformer, features_cat)])
clf = Pipeline(steps=[('preprocess', preprocess),('model', LogisticRegression(max_iter=2000, class_weight='balanced'))])
X_train, X_test, y_train, y_test = train_test_split(X, y_class, test_size=0.25, random_state=42, stratify=y_class)
clf.fit(X_train, y_train)
probs = clf.predict_proba(X_test)[:,1]
preds = (probs >= 0.5).astype(int)
classification_metrics = {
    'accuracy': accuracy_score(y_test, preds),
    'roc_auc': roc_auc_score(y_test, probs)
}
# Numeric-only linear model for days late to summarize associations
lin_features = features_num
Xn = df[lin_features].fillna(0)
y_reg = df['Days Late']
Xn_train, Xn_test, yr_train, yr_test = train_test_split(Xn, y_reg, test_size=0.25, random_state=42)
lin = Pipeline(steps=[('scaler', StandardScaler()), ('model', LinearRegression())])
lin.fit(Xn_train, yr_train)
yr_pred = lin.predict(Xn_test)
reg_metrics = {'r2': r2_score(yr_test, yr_pred), 'mae_days': mean_absolute_error(yr_test, yr_pred)}
coef = pd.DataFrame({'feature': lin_features, 'coefficient_standardized': lin.named_steps['model'].coef_}).sort_values('coefficient_standardized', ascending=False)
coef.to_csv(BASE/'delivery_delay_linear_coefficients.csv', index=False)
pd.Series({**classification_metrics, **reg_metrics}).to_csv(BASE/'model_metrics.csv')

# Chart styling helper
plt.rcParams.update({'figure.dpi': 160, 'font.size': 10})

def savefig(name):
    plt.tight_layout()
    plt.savefig(FIG/name, bbox_inches='tight')
    plt.close()

# 1 KPI summary bars preferred vs non preferred
fig, ax = plt.subplots(figsize=(7.5,4.5))
plot_df = preferred_summary.copy()
ax.bar(plot_df['Preferred Supplier'], plot_df['on_time_rate']*100)
ax.set_ylim(0, 100)
ax.set_ylabel('On-time delivery rate (%)')
ax.set_xlabel('Preferred supplier status')
ax.set_title('Preferred Supplier Status vs. On-Time Delivery')
for i, v in enumerate(plot_df['on_time_rate']*100):
    ax.text(i, v+1, f'{v:.1f}%', ha='center')
savefig('fig1_preferred_on_time.png')

# 2 Risk vs days late
fig, ax = plt.subplots(figsize=(7.5,4.5))
risk_plot = risk_summary.copy()
ax.bar(risk_plot['Supplier Risk'], risk_plot['average_days_late'])
ax.set_ylabel('Average days late')
ax.set_xlabel('Supplier risk level')
ax.set_title('Supplier Risk Level and Average Delivery Delay')
for i, v in enumerate(risk_plot['average_days_late']):
    ax.text(i, v+0.04, f'{v:.2f}', ha='center')
savefig('fig2_risk_days_late.png')

# 3 Maverick spend comparison
fig, ax = plt.subplots(figsize=(7.5,4.5))
plot = maverick_summary.set_index('Maverick Spend').loc[['No','Yes']]
ax.bar(plot.index, plot['average_days_late'])
ax.set_ylabel('Average days late')
ax.set_xlabel('Maverick spend')
ax.set_title('Maverick Spend and Delivery Delay')
for i, v in enumerate(plot['average_days_late']):
    ax.text(i, v+0.04, f'{v:.2f}', ha='center')
savefig('fig3_maverick_days_late.png')

# 4 Top suppliers by performance score
fig, ax = plt.subplots(figsize=(8,5))
top = supplier.head(8).sort_values('performance_score')
ax.barh(top['Supplier Name'], top['performance_score'])
ax.set_xlabel('Composite performance score')
ax.set_title('Top Supplier Scorecard: Reliability, Savings, ESG, and Risk')
savefig('fig4_supplier_scorecard.png')

# 5 Spend by category
fig, ax = plt.subplots(figsize=(8,5))
cat = category.head(8).sort_values('net_spend')
ax.barh(cat['Category'], cat['net_spend']/1e6)
ax.set_xlabel('Net spend ($ millions)')
ax.set_title('Highest Procurement Spend by Category')
savefig('fig5_category_spend.png')

# 6 Correlation heatmap-like matrix using imshow
corr_cols = ['Days Late','Lead Time Days','Savings Pct','Line Net','Supplier ESG Score','risk_score','preferred_flag','maverick_flag']
corr = df[corr_cols].corr(numeric_only=True)
fig, ax = plt.subplots(figsize=(7,6))
im = ax.imshow(corr.values, vmin=-1, vmax=1)
ax.set_xticks(range(len(corr_cols)))
ax.set_yticks(range(len(corr_cols)))
ax.set_xticklabels(corr_cols, rotation=45, ha='right')
ax.set_yticklabels(corr_cols)
fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
ax.set_title('Correlation Matrix of Procurement Performance Drivers')
savefig('fig6_correlation_matrix.png')

# 7 Line trend of spend and on-time by year quarter
quarter = df.groupby(['PO Year','PO Quarter']).agg(net_spend=('Line Net','sum'), on_time_rate=('on_time_flag','mean')).reset_index()
quarter['period'] = quarter['PO Year'].astype(str) + ' ' + quarter['PO Quarter']
fig, ax = plt.subplots(figsize=(8,4.5))
ax.plot(quarter['period'], quarter['net_spend']/1e6, marker='o')
ax.set_ylabel('Net spend ($ millions)')
ax.set_xlabel('PO period')
ax.set_title('Procurement Net Spend Trend')
ax.tick_params(axis='x', rotation=45)
savefig('fig7_spend_trend.png')

print('Analysis complete')
