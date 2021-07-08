# @Site   :  https://github.com/pynote/investnote
# @Author :  老涂数据投研(py_invest_note)

import pickle
import matplotlib.pyplot as plt


def load_obj(name):
    with open('{}.pkl'.format(name), 'rb') as f:
        return pickle.load(f)


plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.size'] = 20

d = load_obj('retreat')
print(d)
fig = plt.figure(figsize=(16, 9))
plt.bar(d.keys(), d.values())
plt.title('白马股今年来回撤 %')
plt.xticks(rotation=60)
fig.text(0.5, 0.5, '老涂数据投研(py_invest_note)',
         fontsize=28, color='gray', alpha=0.5,
         ha='center', va='center', rotation='30')
plt.savefig(
    fname='retreat.jpg', bbox_inches='tight')
