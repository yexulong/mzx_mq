# -*- coding=utf-8 -*-
# !/usr/bin/env python3


from tkinter import *
from tkinter import ttk

# 导入re正则
import re
import pandas as pd

from gen_diff import *

df = pd.read_excel(r'基因.xlsx')

df1 = pd.read_excel(r'基因.xlsx', 1)


# 定义一个对象
class ReDemo:
    # 初始化属性，其中参数self是默认的参数
    def __init__(self, master):
        self.master = master
        self.master.rowconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=1)
        self.master.rowconfigure(2, weight=1)
        self.master.columnconfigure(0, weight=1)

        self.addcombinebox()

        self.notebook_frame = Frame(self.master)
        self.notebook = ttk.Notebook(self.notebook_frame)
        self.notebook_frame.rowconfigure(0, weight=1)
        self.notebook_frame.rowconfigure(1, weight=1)
        self.notebook_frame.rowconfigure(2, weight=1)
        self.notebook_frame.columnconfigure(0, weight=1)
        self.notebook_frame.grid()
        self.notebook.grid()

        Button(self.master, text='计算', command=self.get_result).grid(sticky="S", padx=10, pady=5)
        combostyle = ttk.Style()
        combostyle.theme_create('combostyle', parent='alt',
                                settings={
                                    'TCombobox': {
                                        'configure':
                                            {
                                                'foreground': 'blue',  # 前景色
                                                'fieldbackground': 'white',  # 下拉框颜色
                                            }
                                    }
                                })
        combostyle.theme_use('combostyle')

    def addcombinebox(self):
        self.combox_frame = Frame(self.master)
        self.combox_frame.rowconfigure(0, weight=1)
        self.combox_frame.columnconfigure(0, weight=1)
        self.combox_frame.rowconfigure(1, weight=1)
        self.combox_frame.columnconfigure(1, weight=1)
        self.combox_frame.rowconfigure(2, weight=1)
        self.combox_frame.columnconfigure(2, weight=1)
        self.combox_frame.grid()
        self.comboxs_dict = {}
        combox_list = df.columns.to_list()
        for index, combox in enumerate(combox_list):
            combox_label = Label(self.combox_frame, text=f"{combox}:")
            combobox = ttk.Combobox(self.combox_frame)

            df3 = df.merge(df1, left_on=combox, right_on='名称')
            combobox['value'] = list(set(df[combox].to_list())) + list(
                set(list(df3.子基因1.unique()) + list(df3.子基因2.unique())))
            row = int(index / 2)
            combox_label.rowconfigure(row, weight=1)
            combox_label.columnconfigure(index % 2 * 2, weight=1)
            combobox.rowconfigure(row, weight=1)
            combobox.columnconfigure(index % 2 * 2 + 1, weight=1)
            combox_label.grid(row=row, column=index % 2 * 2)
            combobox.grid(row=row, column=index % 2 * 2 + 1)
            if combox == '主题名称':
                combobox.bind("<<ComboboxSelected>>", self.refresh)
            else:
                combobox.bind("<<ComboboxSelected>>", self.set_null)
            self.comboxs_dict[combox] = combobox

    def refresh(self, *args, **kwargs):
        name = self.comboxs_dict.get('主题名称').get()
        _attr = df[df['主题名称'].str.contains(name)]
        for key, combobox in self.comboxs_dict.items():
            value = _attr[key].values[0]
            combobox.set(value)

    def set_null(self, *args, **kwargs):
        self.comboxs_dict.get('主题名称').set('')

    def get_result(self, *args, **kwargs):
        a = [v.get() for k, v in self.comboxs_dict.items() if k not in ('主题名称', '猫种')]
        for i in self.notebook.tabs():
            self.notebook.forget(i)
        for i in diff_ratio(a):
            result_str = ''
            result_str += f"{i.get('名称')} {i.get('ratio')}\n"
            frame = Frame(self.notebook)
            frame.rowconfigure(0, weight=1)
            frame.rowconfigure(1, weight=1)
            frame.columnconfigure(0, weight=1)
            frame.grid()
            resultdisplay = Text(frame)
            resultdisplay.rowconfigure(0, weight=1)
            resultdisplay.columnconfigure(0, weight=1)
            resultdisplay.grid()
            self.notebook.add(frame, text=f"{i.get('名称')}")
            b = i.get('基因')
            for j in i.get('op'):
                tag, i1, i2, j1, j2 = j
                result_str += '{:7} {!r:>8} --> {!r}\n'.format(tag, a[i1:i2], b[j1:j2])
            resultdisplay.insert(INSERT, result_str)


def main():
    pass
    root = Tk()
    demo = ReDemo(root)
    root.title('猫之城基因计算器')
    root.protocol('WM_DELETE_WINDOW', root.quit)
    root.mainloop()


if __name__ == '__main__':
    main()
