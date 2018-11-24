#!/usr/bin/env python
# coding: utf-8

# # 五王之战分析 - 冰与火之歌

# ## 简介
# 
# 五王之战（War of the Five Kings）是著名严肃奇幻小说《冰与火之歌》中的著名内战。这是一场规模空前、波及七大王国的内乱。顾名思义，前后共有五人在战争中称王：乔佛里、史坦尼斯、蓝礼均声称自己是铁王座的合法继承人。除此之外，罗柏·史塔克被北境众封臣推选为北境之王，巴隆·葛雷乔伊亦再度掀起独立大旗，欲摆脱铁王座的统治，自称为铁群岛之王。
# 
# 

# 本数据集(battles.csv)包含了五王之战期间的战争，它是所有战斗的大集合。该数据是Kaggle中[Game of Thrones](https://www.kaggle.com/mylesoneill/game-of-thrones)的一部分。
# 
# 数据中的变量含义解释：
# ```
# name: 战争的名称，字符变量。
# year: 战争发生的年份，数值变量。
# battle_number: 本数据中的unique id，对应每一场独立的战役，数值变量。
# attacker_king: 攻击方的国王，"/"表示了国王的更换。例如："Joffrey/Tommen Baratheon"意味着Tomen Baratheon继承了Joffrey的王位，分类变量。
# defender_king: 防守方的国王，分类变量。
# attacker_1: 攻击方将领，字符变量。
# attacker_2: 攻击方将领，字符变量。
# attacker_3: 攻击方将领，字符变量。
# attacker_4: 攻击方将领，字符变量。
# defender_1: 防守方将领，字符变量。
# defender_2: 防守方将领，字符变量。
# defender_3: 防守方将领，字符变量。
# defender_4: 防守方将领，字符变量。
# attacker_outcome: 从攻击方角度来看的战争结果，分别有：win, loss, draw，分类变量。
# battle_type: 战争的类别。pitched_battle: 双方军队在一个地点相遇并战斗，这也是最基本的战争类别；ambush: 以隐身或诡计为主要攻击手段的战争；siege: 阵地战；razing: 对未设防位置的攻击。分类变量。
# major_death: 是否有重要人物的死亡，二进制变量。
# major_capture: 是否有重要人物的被捕，二进制变量。
# attacker_size: 攻击方力量的大小，并未对骑兵、步兵等士兵种类有所区分，数值变量。
# defender_size: 防守方力量的大小，并未对骑兵、步兵等士兵种类有所区分，数值变量。
# attacker_commander: 攻击方的主要指挥官。指挥官的名字中并没有包含头衔，不同的指挥官名字用逗号隔开，字符变量。
# defender_commander: 防守方的主要指挥官。指挥官的名字中并没有包含头衔，不同的指挥官名字用逗号隔开，字符变量。
# summer: 战争是否发生于夏天，二进制变量。
# location: 战争发生的地点，字符变量。
# region: 战争发生的地域，包括：Beyond the Wall, The North, The Iron Islands, The Riverlands, The Vale of Arryn, The Westerlands, The Crownlands, The Reach, The Stormlands, Dorne，分类变量。
# note: 注释，字符变量。
# 
# ```

# ## 项目完成指南
# 
# 
# 
# 本项目中的数据分析流程已经给出，但代码将完全由你自己进行书写，如果你无法完成本项目，说明你目前的能力并不足以完成 数据分析(进阶)纳米学位，建议先进行 数据分析（入门）纳米学位的学习，掌握进阶课程的先修知识。
# 
# 对于数据分析过程的记录也是数据分析报告的一个重要部分，你可以自己在需要的位置插入Markdown cell，记录你在数据分析中的关键步骤和推理过程。比如：数据有什么样的特点，统计数据的含义是什么，你从可视化中可以得出什么结论，下一步分析是什么，为什么执行这种分析。如果你无法做到这一点，你也无法通过本项目。
# 
# 
# > **小贴士**: 像这样的引用部分旨在为学员提供实用指导，帮助学员了解并使用 Jupyter notebook

# ## 修改
# - 加入语句让df.info()中间部分数据不被隐藏
# - 完善图表信息
# - 使用att_win.add(dff_win,fill_value = 0)语句简化统计过程
# - 使用plt.axis("equal")调整饼状图结构
# - 使用totalForce = attForce.add(defForce,fill_value = 0)语句
# - 使用box chart 对离散变量与连续变量进行可视化

# ## 提出问题
# 
# 在此项目中，你将以一名数据分析师的身份执行数据的探索性分析。你将了解数据分析过程的基本流程。在你分析数据之前，请先思考几个你需要理解的关于这些战斗的问题，例如，哪一个区域发生了最多的战争？哪一个国王获得了最多的胜利？战争的胜利与否受那些关键因素的影响？
# 
# **问题**：
# 
# 1.哪一个区域发生了最多的战争？
# 
# 2.哪一个国王获得了最多的胜利？
# 
# 3.哪位国王发起了最多的进攻？
# 
# 4.哪场战争规模最大？
# 
# 5.战争的胜利与进攻方人数比例有什么关系？
# 
# （为了确保学习的效果，请确保你的数据分析报告中能够包含2幅可视化和1个相关性分析。）
# 
# **答案**：
# 
# 1.The Riverlands 区域发生的战争最多
# 
# 2.Joffrey/Tommen Baratheon 获得了最多的胜利
# 
# 3.Joffrey/Tommen Baratheon 发起的进攻次数最多
# 
# 4.Battle of Castle Black 是规模最大的战役（此处对缺失的attacker_force与defender_force采取了设为0的处理）
# 
# 5.战争的胜利与进攻方人数比例关系不大
# 
# 在提出了问题之后，我们将开始导入数据，并对数据进行探索性分析，来回答上面提出的问题。
# 
# > **小贴士**: 双击上框，文本就会发生变化，所有格式都会被清除，以便你编辑该文本块。该文本块是用 [Markdown](http://daringfireball.net/projects/markdown/syntax)编写的，该语言使用纯文本语法，能用页眉、链接、斜体等来规范文本格式。在纳米学位课程中，你也会用到 Markdown。编辑后，可使用 **Shift** + **Enter** 或 **Shift** + **Return** 运行上该框，使其呈现出编辑好的文本格式。

# ## 数据评估和清理

# > **小贴士**: 运行代码框的方法与编辑上方的 Markdown 框的格式类似，你只需点击代码框，按下键盘快捷键 **Shift** + **Enter** 或 **Shift** + **Return** ，或者你也可先选择代码框，然后点击工具栏的 **运行** 按钮来运行代码。运行代码框时，相应单元左侧的信息会出现星号，即 `In [*]:`，若代码执行完毕，星号则会变为某个数字，如 `In [1]`。如果代码运行后有输出结果，输出将会以 `Out [1]:` 的形式出现，其中的数字将与 "In" 中的数字相对应。

# In[1]:


# TO DO: load pacakges
import pandas as pd
import matplotlib.pyplot as plt

get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


# TO DO: load the dataset
df = pd.read_csv('battles.csv')


# In[3]:


# TO DO: check the dataset general info
df.info()
# Tip1: not hide information in head()
pd.set_option('display.max_columns', None)
df.head()


# **问题**：
# 
# 1.哪一个区域发生了最多的战争？
# 
# 2.哪一个国王获得了最多的胜利？
# 
# 3.哪位国王发起了最多的进攻？
# 
# 4.哪场战争规模最大？
# 
# 5.战争的胜利与进攻方人数比例有什么关系？
# 
# **数据分析**：
# 
# 1.region 没有缺失值
# 
# 2.attacker_king有缺失值，去掉缺失的数据
# 
# 3.去掉同时缺失attacker_king与defender_king的数据
# 
# 4.去掉同时缺失attacker_size与defender_size的数据
# 
# 5.去掉attacker_size或defender_size有缺失的数据

# In[4]:


# TO DO: clean the data (optional: only there are problems)
# Duplicate
print('数据中重复值为：%d' % df.duplicated().sum())

# Transform win/lose into numeric form
dict = {'win':1, 'loss':-1, 'Nan':0}
df['attacker_outcome'] = df['attacker_outcome'].map(dict)

# Nan
# Nan value in col attacker_king
df_attKing = df[~df['attacker_king'].isnull()]
# Nan value in col attacker_king and defender_king
df_attAndDefKing = df[~(df['attacker_king'].isnull() & df['defender_king'].isnull())]
# Nan value in col attacker_size and defender_size
#df_attF = df[~df['attacker_size'].isnull()]
df_attAndDefF = df[~(df['defender_size'].isnull() & df['attacker_size'].isnull())]
df_attAndDefF['attacker_size'].fillna(0, inplace = True)
df_attAndDefF['defender_size'].fillna(0, inplace = True)
# Nan value in col attacker_size or defender_size
df_attOrDefF = df[~(df['defender_size'].isnull() | df['attacker_size'].isnull())]
df_attOrDefF.dropna(axis = 0, how='any', subset = ['attacker_outcome'], inplace = True)

# Exception; ignore this part.


# ## 数据探索分析

# **问题1**：哪一个区域发生了最多的战争
# 
# 需要每个region对应的battle_number数据，找到最大值。
# 
# 可视化：饼状图或柱状图

# In[5]:


# In exploratory data analysis, please make sure of using statistics and visualizations
# Question1: Which region has the most wars
# Data: df
# Plot: pie chart or bar chart
#df_regionBat = df.groupby('region').sum()
# Answer for Q1:
#region = df_regionBat['battle_number'].idxmax()
#print('Region with most battle number is: %s' % region)
# Visualization for Q1:
#df_regionBat['battle_number'].plot(kind = 'bar')
#plt.figure()
#df_regionBat['battle_number'].plot(kind = 'pie')

# Fix1: mis understand of battle_number
# set different color can make chart more straight
print('Region with most battle number is: %s' % df.region.value_counts().idxmax())
plt.figure()
df.region.value_counts().plot(kind='bar', color = ["r","gray","gray","gray","gray","gray","gray","gray"])
plt.title('Region - number of wars')
plt.xlabel('battle name')
plt.ylabel('number of battles')


# **问题1分析**：
# 
# 两种可视化结果都能有效掌握所有区域发生战斗数的情况。
# 
# **问题2**：哪一个国王获得了最多的胜利？
# 
# 需要每位国王对应的战斗胜利数

# In[6]:


# Question2: Which king had won the most battles
# Data: df_attAndDefKing
# Plot: bar chart
# Get number they win when defend/attack
attacker_win = df_attAndDefKing.groupby('attacker_king')['attacker_outcome'].sum()
defender_win = -df_attAndDefKing.groupby('defender_king')['attacker_outcome'].sum()
# Make sure they use same index
total_win = attacker_win.add(defender_win,fill_value = 0)
# Answer for Q2:
print("King %s has won the most wars" % total_win.idxmax())
# Visualization for Q2:
# Since there are negative numbers, bar chart will be a better choice
total_win.plot(kind = 'bar')
plt.title('king - win of wars')
plt.xlabel('King')
plt.ylabel('Win of wars')


# **问题2分析**：
# 
# 通过柱状图的可视化可以清晰看出每位国王的获胜情况
# 
# **问题3**：哪位国王发起了最多的进攻？
# 
# 需要attacker_king的数据，统计battle数，不考虑battle_number

# In[7]:


# Question3: Which king had launch most attack
# Data: df_attKing
# Plot: pie chart or bar chart
attKing_Batt = df_attKing['attacker_king'].value_counts()
# Answer for Q3:
print('King %s has launched the most attack' % attKing_Batt.idxmax())
# Visualization for Q3:
attKing_Batt.plot(kind = 'bar')
plt.title('King - number of attacks')
plt.xlabel('King')
plt.ylabel('number of attacks')
plt.figure()
attKing_Batt.plot(kind = 'pie')
plt.axis("equal")
plt.title('King - number of attacks')


# **问题3分析**：
# 
# 两种可视化结果都能有效掌握国王发起进攻的情况。
# 
# **问题4**：哪场战争规模最大？
# 
# 从attacker_size与defender_size两者总评价战役规模

# In[8]:


# Question4: Which is the most fierce battle
# Data: df_attAndDefF
# Plot: pie chart or bar chart
attForce = df_attAndDefF.groupby('name')['attacker_size'].sum()
defForce = df_attAndDefF.groupby('name')['defender_size'].sum()
totalForce = attForce.add(defForce,fill_value = 0)

# Answer for Q4:
print(' %s has the most people involed' % totalForce.idxmax())
# Visualization for Q4:
totalForce.plot(kind = 'bar')
plt.title('Size of battle')
plt.xlabel('battle name')
plt.ylabel('size of battle')
plt.figure()
totalForce.plot(kind = 'pie')
plt.title('Size of battle')
plt.axis("equal")


# **问题4分析**：
# 
# 两种可视化方法都能有效得出结论，饼状图的标签似乎会过于密集，因此柱状图是更好的选择。
# 
# **问题5**：战争的胜利与进攻方人数比例有什么关系？
# 
# 求出进攻人数占比，用散点图进行探究

# In[10]:


# Question4: Which is the most fierce battle
# Data: df_attOrDefF
# Plot: pie chart or bar chart
attForce = df_attOrDefF['attacker_size']
defForce = df_attOrDefF['defender_size']
totalForce = attForce + defForce
percentForce = attForce/totalForce
# Visualization
#plt.figure()
#plt.scatter(percentForce, df_attOrDefF['attacker_outcome'], marker = 'o')
#ax = plt.gca()
#ax.spines['right'].set_color('none')
#ax.spines['top'].set_color('none')
#ax.xaxis.set_ticks_position('bottom')
#ax.spines['bottom'].set_position(('data', 0))
#plt.xlabel('Percent of attack force')
#plt.ylabel('Attacker outcome')
#plt.yticks([-1, 1], ['$loss$', '$win$'])

# When you have a discrete variable and a continuous variable, use box chart.
import seaborn as sns
import numpy as np

sns.boxplot(x = df_attOrDefF['attacker_outcome'],y = percentForce)

# Option of scatter
sns.set(style="darkgrid")
sns.lmplot(x='attacker_size', y='defender_size', hue = 'attacker_outcome',data = df,
       fit_reg=False)
plt.show()


# **问题5分析**：
# 
# 当一个变量是二元变量时，用散点图分析两个变量的相关性似乎不是最好的方法？
# 
# 但是从上面的散点图中仍然可以看出，战争胜利与进攻方的人数没有很大关系。

# 在数据的探索性分析中，请确保你对数据分析中的关键步骤和推理过程进行了记录。你可以自己插入code cell和markdown cell来组织你的报告。

# ## 得出结论

# **问题**：上面的分析能够回答你提出的问题？通过这些分析你能够得出哪些结论？
# 
# **答案**：
# 
# 1.The Riverlands 区域发生的战争最多
# 
# 2.Joffrey/Tommen Baratheon 获得了最多的胜利
# 
# 3.Joffrey/Tommen Baratheon 发起的进攻次数最多
# 
# 4.Battle of Castle Black 是规模最大的战役（此处对缺失的attacker_force与defender_force采取了设为0的处理）
# 
# 5.战争的胜利与进攻方人数比例关系不大

# ## 反思

# **问题**：在你的分析和总结过程中是否存在逻辑严谨。是否有改进的空间? 你可以从下面的一些角度进行思考：
# 1. 数据集是否完整，包含所有想要分析的数据？
# 2. 在对数据进行处理的时候，你的操作（例如删除/填充缺失值）是否可能影响结论？
# 3. 是否还有其他变量（本数据中没有）能够对你的分析有帮助？
# 4. 在得出结论时，你是否混淆了相关性和因果性？
# 
# **答案**：
# 
# 问题1-3：根据现有数据对问题1的回答没有问题
# 
# 问题4：对attacker_size与defender_size中缺失值直接设为0的处理可能有失偏颇
# 
# 问题5：采取了散点图对进攻方人数比例与战争结果两个变量进行了可视化，但是感觉结果不是那么直观，可能会有更好的可视化方法

# 恭喜你完成了此项目！这只是数据分析过程的一个样本：从生成问题、整理数据、探索数据到得出结论。在数据分析(进阶)纳米学位中，你将会学到更多高级的数据分析方法和技术，如果你感兴趣的话，我们鼓励你继续学习后续的课程，掌握更多的数据分析的高级技能！

# > 若想与他人分享我们的分析结果，除了向他们提供 jupyter Notebook (.ipynb) 文件的副本外，我们还可以将 Notebook 输出导出为一种甚至那些未安装 Python 的人都能打开的形式。从左上方的“文件”菜单，前往“下载为”子菜单。然后你可以选择一个可以更普遍查看的格式，例如 HTML (.html) 。你可能需要额外软件包或软件来执行这些导出。

# In[ ]:




