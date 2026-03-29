import pandas as pd

# 读取原始数据
df = pd.read_excel("F:/文献计量学/data/raw/raw_data_v0.xlsx")

# 1. 按年份筛选（比如 2020-2025）
df = df[(df["Publication Year"] >= 2020) & (df["Publication Year"] <= 2025)]

# 2. 按文献类型筛选（只保留 Article/Review）
df = df[df["Document Type"].isin(["Article", "Review"])]

#第四部分需要详细的关键词，之后再考虑
# 4. 按主题关键词筛选（标题/摘要包含你的研究主题）
#keywords = ["2D transition metal oxide heterostructure", "two-dimensional transition metal oxide heterostructure*", "2D TMO heterostructure*"]
#keyword_pattern = "|".join(keywords)  # 拼接成正则表达式 '|'的意思是或者

# 筛选标题或摘要包含关键词的文献
#df = df[
#    df["Abstract"].str.contains(keyword_pattern, case=False, na=False)
#]

# 输出初筛结果
print(f"初筛后剩余：{len(df)} 篇文献")
df.to_excel("F:/文献计量学/data/processed/screening_data.xlsx", index=False)