import  pandas as pd

df = pd.read_csv(r"C:\Users\21882\OneDrive\桌面\Ecommerce_Sales_Data_2024_2025.csv")
df_raw=df.copy()
pd.set_option('display.max_columns',None)

print("数据形状（行数，列数）：", df.shape)
print("\n前5行数据：")
print(df.head())
print("\n数据基本信息：")
print(df.info())

duplicate_rows=df.duplicated().sum()
print(f'重复行数：{duplicate_rows}')

print(df.describe())

df['Order Date']=pd.to_datetime(df['Order Date'],format='%Y/%m/%d')
print(df['Order Date'].isna().sum())

#折扣率
df['Discount_Rate']=df['Discount']/100
df['calculated_sales']=df['Quantity']*df['Unit Price']*(1-df['Discount_Rate'])
df['sales_diff']=abs(df['Sales']-df['calculated_sales'])
print('----')
print(df['sales_diff'].describe())

categorical_cols=['Region','City','Category','Sub-Category','Customer Name','Payment Mode']
for col in categorical_cols:
    df[col]=df[col].str.strip().str.title()

#利润率
df['Profit_Margin']=df['Profit']/df['Sales']
#年月日
df['Order_Year']=df['Order Date'].dt.year
df['Order_Month']=df['Order Date'].dt.month
df['Order_Day']=df['Order Date'].dt.day
df['Order_Weekday']=df['Order Date'].dt.dayofweek

#季节
def get_season(month):
    if month in [3,4,5]:
        return 'Spring'
    elif month in [6,7,8]:
        return 'Summer'
    elif month in [9,10,11]:
        return 'Fall'
    else:
        return 'winter'
df['Season']=df['Order_Month'].apply(get_season)

print('---------------------------')
print(df.info())
print(df.head())
print(df.describe())
df.to_csv('ecommerce_sales_clean.csv',index=False)