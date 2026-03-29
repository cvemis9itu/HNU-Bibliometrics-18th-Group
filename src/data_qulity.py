#导入
import pandas as pd
file_path = "F:/文献计量学/data/raw/raw_data_v0.xlsx"
df = pd.read_excel(file_path, engine="openpyxl")

#检查缺失率

#检查九个字段
target_cols = [
    "Article Title",       # 标题
    "Authors",             # 作者
    "Affiliations",        # 机构
    "Publication Year",    # 年份
    "Document Type",        # 期刊/会议
    "Abstract",            # 摘要
    "Cited Reference Count",    # 参考文献
    "DOI"                  # DOI
]

keyword_mask = df["Author Keywords"].notna() | df["Keywords Plus"].notna()
keyword_missing_rate = 100 - (keyword_mask.sum() / len(df) * 100)

missing_rate_8 = df[target_cols].isnull().mean() * 100

missing_rate_9 = pd.concat([missing_rate_8, pd.Series({"Keywords (合并)": keyword_missing_rate})])

# 输出（保留2位小数）
print("===== 缺失率检测 ====") 
print(missing_rate_9.round(2))

#检查重复率

total = len(df)

#根据 DOI 判断重复（有DOI的用DOI，没有的用标题+作者+年份）
duplicate_count = df.duplicated(subset=["DOI"]).sum()

duplicate_rate = (duplicate_count / total) * 100

# 输出结果
print("===== 重复率检测 =====")
print(f"总文献数量：{total} 篇")
print(f"重复文献数量：{duplicate_count} 篇")
print(f"重复率：{duplicate_rate:.2f} %")

#歧义率检测、

#1.作者歧义（判断是否有缩写形式，如 Li Y / Li Yu）
def has_ambiguous_author(authors_str):
    if pd.isna(authors_str):
        return True
    # 包含逗号分隔且有缩写（如 Y. Li / Li Y）视为歧义
    return "." in authors_str or len(authors_str.split()) < 3

author_ambiguous = df["Authors"].apply(has_ambiguous_author).sum()

# 2. 机构歧义（空、不完整、简写都算）
def has_ambiguous_affiliation(aff_str):
    if pd.isna(aff_str):
        return True
    return len(str(aff_str).strip()) < 5  # 太短说明不完整

aff_ambiguous = df["Affiliations"].apply(has_ambiguous_affiliation).sum()

# 3. 综合歧义率（有任意一个歧义就算歧义）
total_ambiguous = df.apply(
    lambda row: has_ambiguous_author(row["Authors"]) or has_ambiguous_affiliation(row["Affiliations"]),
    axis=1
).sum()

ambiguous_rate = (total_ambiguous / total) * 100

print("===== 歧义率检测 =====")
print(f"总文献数量：{total} 篇")
print(f"存在歧义的文献：{total_ambiguous} 篇")
print(f"歧义率：{ambiguous_rate:.2f} %")

# 生成Markdown格式的检测报告

def generate_quality_md_report():
    # 1. 整理所有检测结果数据
    # 缺失率数据格式化（保留2位小数）
    missing_data = missing_rate_9.round(2).to_dict()
    missing_lines = []
    for col, rate in missing_data.items():
        missing_lines.append(f"- {col}：{rate}%")
    
    # 2. 构造Markdown内容
    md_content = f"""# 文献数据质量检测报告
## 检测时间
{pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

## 1. 缺失率检测
总文献数量：{total} 篇
{chr(10).join(missing_lines)}

## 2. 重复率检测
- 重复文献数量：{duplicate_count} 篇
- 重复率：{duplicate_rate:.2f} %

## 3. 歧义率检测
- 作者歧义文献数量：{author_ambiguous} 篇
- 机构歧义文献数量：{aff_ambiguous} 篇
- 综合歧义文献数量：{total_ambiguous} 篇
- 综合歧义率：{ambiguous_rate:.2f} %

---
*检测文件：raw_data_v0.xlsx*
*检测脚本：data_qulity.py*
"""
    
    # 3. 写入Markdown文件
    md_file_path = "F:/文献计量学/reports/data_quality_V0.md"
    with open(md_file_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    
    print(f"\n✅ 检测报告已生成至：{md_file_path}")
    print("📄 Markdown报告包含：缺失率、重复率、歧义率完整检测结果")
generate_quality_md_report()

def generate_field_dictionary_md():
    # 构造字段字典Markdown头部
    field_dict_content = """# 字段字典（Field Dictionary_）
## 说明
本字典仅包含核心9个文献字段的关键信息

| 字段名 | 数据类型 | 示例值 | 缺失率（%） |
|--------|----------|--------|-------------|
"""

    # 遍历指定的9个字段（包含Keywords (合并)）
    # 先处理前8个目标字段，再处理合并关键词字段
    for col in missing_rate_9.index:  # missing_rate_9 正好包含9个目标字段
        # 1. 字段名
        col_name = col
        
        # 2. 数据类型（特殊处理合并关键词字段）
        if col == "Keywords (合并)":
            dtype = "bool/string"  # 合并字段的类型说明
        else:
            dtype = str(df[col].dtype)
        
        # 3. 示例值（取第一个非空值，截断过长内容，处理特殊字符）
        if col == "Keywords (合并)":
            # 合并关键词字段取Author Keywords的示例
            sample_val = df["Author Keywords"].dropna().iloc[0] if not df["Author Keywords"].dropna().empty else "无数据"
        else:
            sample_val = df[col].dropna().iloc[0] if not df[col].dropna().empty else "无数据"
        
        sample_val = str(sample_val)[:50].replace("|", "｜").replace("\n", " ")  # 处理表格冲突字符
        
        # 4. 缺失率（直接从已计算的missing_rate_9获取）
        missing_rate = missing_rate_9[col].round(2)
        
        # 拼接表格行
        field_dict_content += f"| {col_name} | {dtype} | {sample_val} | {missing_rate} |\n"

    # 补充统计信息
    field_dict_content += f"""
## 统计信息
- 核心字段数量：{len(missing_rate_9)} 个
- 生成时间：{pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
- 数据来源：raw_data_v0.xlsx
"""
    
    # 写入Markdown文件（使用绝对路径，避免路径错误）
    field_dict_path = "F:/文献计量学/data/field_dictionary_V0.md"
    with open(field_dict_path, "w", encoding="utf-8") as f:
        f.write(field_dict_content)
    
    print(f"\n✅ 字段字典报告已生成至：{field_dict_path}")
    print(f"📊 字典仅包含 {len(missing_rate_9)} 个核心字段的信息")

# 执行生成字段字典函数
generate_field_dictionary_md()