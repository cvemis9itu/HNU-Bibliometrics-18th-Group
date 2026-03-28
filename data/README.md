
## 2. 数据来源
- **数据库**：Web of Science 
- **检索时间**：2026-03-28
- **检索式**：`TS=("2D transition metal oxide heterostructure*" OR "two-dimensional transition metal oxide heterostructure*" OR "2D TMO heterostructure*") AND PY=2015-2025 AND DT=("Article" OR "Review")`
- **导出字段**：标题、作者、来源出版物、年份、卷期页、DOI、摘要、作者关键词、WOS被引次数、作者机构、基金资助信息

## 3. 数据处理流程
1.  **去重**：依据 DOI 字段去重，(共删除 112 条重复文献记录)
2.  **主题筛选**：人工复核摘要，(排除 76 条与“二维过渡金属氧化物异质结”无关的条目)
3.  **格式标准化**：
  - 统一作者名格式为「姓, 名首字母」
  - 期刊名统一为全称
  - 年份、卷期页格式规范化
4.  **缺失值处理**：删除无 DOI 或无摘要的无效条目
5.  **字段补充**：新增 `first_author_affiliation` 字段，提取第一作者所属机构

## 4. 字段说明
| 字段名               | 含义                                   |
|----------------------|----------------------------------------|
| `title`              | 文献标题                               |
| `authors`            | 作者列表（分号分隔）                   |
| `journal`            | 期刊全称                               |
| `year`               | 发表年份                               |
| `volume`             | 期刊卷号                               |
| `issue`              | 期刊期号                               |
| `pages`              | 页码范围                               |
| `doi`                | 文献唯一标识 DOI                       |
| `abstract`           | 文献摘要                               |
| `keywords`           | 作者关键词（分号分隔）                 |
| `citations`          | WOS 数据库统计的被引次数               |
| `affiliations`       | 所有作者所属机构（分号分隔）           |
| `first_author_affil` | 第一作者所属机构                       |
| `funding`            | 基金资助信息（分号分隔）               |

## 5. 使用说明
- 本数据适用于**二维过渡金属氧化物异质结**领域的文献计量分析，包括：研究趋势演化、合作网络、关键词共现、热点主题挖掘等
- 推荐使用 Python `pandas` 库读取 `processed/cleaned_2d_tmo_heterostructure.csv`
- 原始数据 `raw/` 目录下的文件保留完整导出信息，可用于重新处理或验证
- 数据仅限学术研究用途，禁止商用
