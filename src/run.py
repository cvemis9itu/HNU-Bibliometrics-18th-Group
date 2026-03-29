import yaml
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
with open("query.yaml", "r", encoding="utf-8") as f:
        config1 = yaml.safe_load(f)
with open("query.yaml", "r", encoding="utf-8") as g:
        config2 = yaml.safe_load(g)
print('object',config1['query']['object'])
print('time',config1['query']['constraint']['time']['start'],'-',config1['query']['constraint']['time']['end'])
print('method',config1['query']['method'])
print('context',config1['query']['context'])
print('document_type',config1['query']['constraint']["document_type"])

