import yaml
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
with open("query.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
print('数据库:',config['database'])
print('时间范围:',config['time_window']['start'],'-',config['time_window']['end'])
print("检索关键词：")
for kw in config["keywords"]:
        print(kw)
print("分析方法：")
for am in config["analysis_methods"]:
    print(am)
