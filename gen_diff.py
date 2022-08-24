# -*- coding=utf-8 -*-
# !/usr/bin/env python3


import difflib
import yaml

with open(r'combine_gen.yaml', 'r', encoding='utf8') as f:
    df_list = yaml.safe_load(f)

# 保存所有组合基因
all_parent_gen_set = set([j for i in df_list for j in i['基因']])

with open(r'base_gen.yaml', 'r', encoding='utf8') as f:
    base_gen_map = yaml.safe_load(f)

# 保存所有基础基因
all_base_gen_set = set([j for i in base_gen_map.values() for j in i])

# 基础基因对应组合的字典
# 形如 {
#   '可可爱爱': ['大吃一惊', '嘟嘟嘴', '傲娇', '痞里痞气']
# }
base_to_combine = {}
for k, v in base_gen_map.items():
    for i in v:
        base_to_combine.setdefault(i, [])
        base_to_combine[i].append(k)


def diff_ratio(gen_list):
    """
    获取gen_list与各主题基因的相似度
    :param gen_list: 要对比的基因列表，即猫球的基因列表
    :return: 返回前10项相似度不为0的主题基因
    """
    for i in df_list:
        real_gen_list = get_real_gen(i['基因'], gen_list)
        # print(f'{i["名称"]}:', real_gen_list, gen_list)
        sm = difflib.SequenceMatcher(None, gen_list, real_gen_list)
        i['ratio'] = sm.ratio()
        i['op'] = sm.get_opcodes()
    yield from list(filter(lambda x: x['ratio'] > 0, sorted(df_list, key=lambda x: x['ratio'], reverse=True)))[:10]


def get_real_gen(parent_gen_list, enter_gen_list):
    """
    组合基因由两个基本基因组合而成，获取主题基因对应的基础基因
    :param parent_gen_list: 主题基因列表
    :param enter_gen_list: 要对比的基因列表，即猫球的基因列表
    :return: 真正要对比的主题基因列表
    """
    for i in enter_gen_list:
        if i in parent_gen_list:
            continue
        if i not in all_base_gen_set:
            continue
        combine_gen_list = base_to_combine.get(i)
        # 存在基础基因，可以合成
        if set(combine_gen_list) & set(parent_gen_list):
            combine_gen = list(set(combine_gen_list) & set(parent_gen_list))[0]
            index = parent_gen_list.index(combine_gen)
            parent_gen_list.pop(index)
            for j in base_gen_map.get(combine_gen):
                parent_gen_list.insert(index, j)

    return parent_gen_list


if __name__ == '__main__':
    a = ['灵动妩媚', '不可思议', '阴阳双生', '红豆奶茶', '烤可可豆', '蜂蜜奶油']
    for i in diff_ratio(a):
        print(i.get('名称'), i.get('ratio'))
        b = i.get('基因')
        for j in i.get('op'):
            tag, i1, i2, j1, j2 = j
            print('{:7} {!r:>8} --> {!r}'.format(tag, a[i1:i2], b[j1:j2]))
