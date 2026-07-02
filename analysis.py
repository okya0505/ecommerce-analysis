import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('ecommerce_sales_clean.csv')
pd.set_option('display.max_columns',None)
df['Order Date']=pd.to_datetime(df['Order Date'])
# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

print(df.head())

#数字型字段的总体分布
num_cols=['Sales', 'Profit', 'Quantity', 'Discount', 'Unit Price']
df[num_cols].hist(bins=30,figsize=(12,8))
plt.suptitle('数值字段分布直方图')
plt.savefig('hist_num_cols.png',dpi=150,bbox_inches='tight')
plt.show()

#各类型占比
cat_cols = ['Region', 'Category', 'Payment Mode', 'Season']
for col in cat_cols:
    plt.figure(figsize=(10,6))
    df[col].value_counts().plot(kind='bar')
    plt.title(col)
    plt.xticks(rotation=0)
    plt.savefig(f'bar_{col}.png',dpi=150,bbox_inches='tight')
    plt.show()

#销售额与利润的关系
plt.figure()
plt.scatter(df['Sales'],df['Profit'],alpha=0.3)
plt.title('Sales vs Profit')
plt.xlabel('Sales')
plt.ylabel('Profit')
plt.savefig('scatter_sales_profit.png',dpi=150,bbox_inches='tight')
plt.show()

#不同地区销售额
plt.figure()
df.groupby('Region')['Sales'].sum().sort_values().plot(kind='bar')
plt.title('Total Sales by Region')
plt.xticks(rotation=0)
plt.ylabel('Sales')
plt.savefig('bar_sales_by_region.png',dpi=150,bbox_inches='tight')
plt.show()

#不同产品类别销售额占比
plt.figure()
df.groupby('Category')['Sales'].sum().plot(kind='pie',autopct='%.1f%%')
plt.title('Sales by Category')
plt.savefig('pie_sales_by_category.png',dpi=150,bbox_inches='tight')
plt.show()

#按月汇总销售额
plt.figure()
month_sales=df.groupby('Order_Month')['Sales'].sum()
month_sales.plot(kind='line',marker='o')
plt.title('Month Sales Trend')
plt.ylabel('Sales')
plt.xticks(rotation=0)
plt.savefig('line_month_sales_trend.png',dpi=150,bbox_inches='tight')
plt.show()

#客户RFM
reference_date=df['Order Date'].max()
rfm=df.groupby('Customer Name').agg({'Order Date':lambda x:(reference_date-x.max()).days,
                                     'Order ID':'count',
                                     'Sales':'sum'}).rename(columns={'Order Date':'Recency',
                                                                     'Order ID':'Frequency',
                                                                     'Sales':'Monetary'})

rfm['R_Score']=pd.qcut(rfm['Recency'],4,labels=[4,3,2,1])
rfm['F_Score'] = rfm['Frequency'].apply(lambda x: 1 if x==1 else (2 if x==2 else 3))

def get_m_score(amount):
    if amount < 50000:
        return 1  # 普通消费：5万以下（单件小额）
    elif amount < 150000:
        return 2  # 中等消费：5万 - 15万（单件或低折扣两件）
    elif amount < 300000:
        return 3  # 高消费：15万 - 30万（真正的高客单价）
    else:
        return 4  # 极高价值：30万以上（绝对头部大单）

rfm['M_Score'] = rfm['Monetary'].apply(get_m_score)

rfm['RFM_Score']=rfm['R_Score'].astype(str)+rfm['F_Score'].astype(str)+rfm['M_Score'].astype(str)

def segment(r):
    if r['R_Score']>=3 and r['F_Score']>=2 and r['M_Score']>=3:
        return '高价值客户'
    elif r['F_Score']>=2:
        return '忠诚客户'
    elif r['M_Score']>=3:
        return '高消费客户'
    else:
        return '普通客户'

rfm['Segment']=rfm.apply(segment,axis=1)
segment_counts=rfm['Segment'].value_counts().reindex(['普通客户', '高消费客户', '忠诚客户', '高价值客户'])

plt.figure()
a=segment_counts.plot(kind='bar')
plt.title('客户群体分布')
plt.xlabel('客户类型')
plt.ylabel('客户数量')
plt.xticks(rotation=0)
for i,v in enumerate(segment_counts):
    a.text(i,v+5,str(v),ha='center',va='bottom')
plt.savefig('bar_customer_segments.png',dpi=150,bbox_inches='tight')
plt.show()
rfm.to_csv('rfm_result.csv', index=True)









