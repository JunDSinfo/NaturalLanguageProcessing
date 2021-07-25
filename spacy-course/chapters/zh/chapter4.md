---
title: '第四章：训练神经网络模型'
description: '本章中，我们要学习更新spaCy的统计模型使其能够为特定的使用场景做出定制化。一个例子是我们想要在网络上的评论中抽取一种新的实体。我们将会学到如何从头编码自己的模型训练流程，了解模型训练的基本工作原理，以及一些技巧使得我们自己的定制化自然语言处理项目能够更加成功。'
prev: /chapter3
next: null
type: chapter
id: 4
---

<exercise id="1" title="训练和更新模型" type="slides">

<slides source="chapter4_01_training-updating-models">
</slides>

</exercise>

<exercise id="2" title="模型训练的目的">

spaCy已经预装了一系列预训练好的模型来抽取各种语言学标签，然后我们几乎 _总是_
想要用更多的新例子来优化模型。我们可以用更多的标注数据来训练模型达到这个目的。

模型训练不能达到哪个目标？

<choice>

<opt text="改进特定数据上面的准确度。">

如果预训练模型在特定数据上面效果不好，用特定的例子再去训练模型会是个好方法。

</opt>

<opt text="学习新的分类目标。">

我们可以通过训练来教会模型新的标签、实体类别或是其它分类目标。

</opt>

<opt text="在未标注数据中做模式发现。" correct="true">

spaCy的组件都是用来做文本标注的监督学习模型，这意味着这些模型只能学习标注过的例子，
而不能从原始文本中估计出新的标签。

</opt>

</choice>

</exercise>

<exercise id="3" title="创建训练数据(1)">

spaCy的基于规则的`Matcher`可以很好地被用来快速创建一些命名实体模型的训练数据。变量
`TEXTS`中存储着句子的列表，我们可以将其打印出来做检查。我们想要找到所有对应不同iPhone
型号的文本，所以我们可以创建一些训练数据来教会模型把它们识别为电子产品`"GADGET"`。

- 编写一个模板，含有两个词符且它们的小写形式可以匹配到`"iphone"`和`"x"`。
- 编写一个模板，含有两个词符，第一个词符的小写形式匹配到`"iphone"`，第二个词符用`"?"`
  运算符匹配到一个数字。

<codeblock id="04_03">

- 要匹配一个小写形式的词符，我们可以用`"LOWER"`属性，比如`{"LOWER": "apple"}`。
- 要寻找一个数字词符，我们可以用`"IS_DIGIT"`标签，比如`{"IS_DIGIT": True}`。

</codeblock>

</exercise>

<exercise id="4" title="创建训练数据(2)">

我们现在用上一个练习中创建的匹配模板来引出一系列的训练例子。`TEXTS`变量中存有句子的
列表。

- 使用`nlp.pipe`对每一个文本创建一个doc。
- 在`doc`上做匹配创建出一个匹配结果的span列表。
- 获取匹配结果span的`(start character, end character, label)`元组。
- 把每个例子的格式写为一个文本和一个词典的元组，把`"entities"`映射到实体元组上。
- 把例子附加到`TRAINING_DATA`中，检查打印的数据。

<codeblock id="04_04">

- 要得到匹配结果，在`doc`上面调用`matcher`。
- 返回的匹配结果在`(match_id, start, end)`元组里。
- 我们可以用`TRAINING_DATA.append()`把一个例子添加到训练示例列表中。

</codeblock>

</exercise>

<exercise id="5" title="模型训练过程" type="slides">

<slides source="chapter4_02_training-loop">
</slides>

</exercise>

<exercise id="6" title="设置流程">

这个练习中，我们来搭建一个spaCy的流程，训练实体识别器识别文本中的`"GADGET"`实体，
比如"iPhone X"。

- 创建一个空的`"en"`模型，我们可以用`spacy.blank`方法。
- 用`nlp.create_pipe`创建一个新的实体识别器，加入到流程中。
- 我们可以在流程组件上调用`add_label`方法， 把新的标签`"GADGET"`加入到实体识别器中。

<codeblock id="04_06">

- 要创建一个空的实体识别器，我们可以调用`nlp.create_pipe`，返回给名字是`"ner"`的变量。
- 要把组件加入到流程中，我们可以用`nlp.add_pipe`方法。
- `add_label`方法是实体识别器流程组件的一个方法，这个组件我们已经存储在了变量`ner`里面。
  要给它增加一个标签，我们可以调用`ner.add_label`加上标签的字符串名，
  比如`ner.add_label("SOME_LABEL")`。

</codeblock>

</exercise>

<exercise id="7" title="搭建训练过程">

我们现在来从头写一个简单的训练过程。

我们在上一个练习中创建的流程存储在`nlp`实例中，里面已经含有了实体识别器和我们
新增的标签`"GADGET"`。

我们之前创建的一小组标注例子存储在`TRAINING_DATA`中。想要看这些例子的话我们可以在
代码中把它们打印出来。

- 调用`nlp.begin_training`，创建一个有10个循环的训练过程并把训练数据的顺序随机化。
- 使用`spacy.util.minibatch`创建几批训练数据，然后在每一批数据上作遍历。
- 把每一批数据里的`(text, annotations)`元组转变为`texts`和`annotations`的列表。
- 对每一批数据，调用`nlp.update`方法用这些文本text和标注annotation去更新模型。

<codeblock id="04_07">

- 调用`nlp.begin_training()`方法来重置模型参数并开始训练。
- 在训练例子的列表上调用`spacy.util.minibatch`函数来将训练数据分为一系列批次。

</codeblock>

</exercise>

<exercise id="8" title="检测模型">

让我们来看看模型在未出现过的新数据上表现如何！为了节省时间，我们已经在一些文本上面
训练好了一个带有标签`"GADGET"`的模型。这里是一些结果：


| 文本                                                                                                              | 实体              |
| ----------------------------------------------------------------------------------------------------------------- | ---------------------- |
| 苹果已经开始让iPhone 8和iPhone X变得越来越慢了，怎么办                                                              | `(iPhone 8, iPhone X)` |
| 我终于明白iPhone X的“刘海”是干嘛的了                                                                               | `(iPhone X,)`          |
| 关于Samsung Galaxy S9你需要了解的一切                                                                              | `(Samsung Galaxy,)`    |
| 想要比较不同的iPad型号？这里是2020年所有的产品线对比。                                                              | `(iPad,)`              |
| iPhone 8和iPhone 8 Plus是苹果公司设计、研发和销售的智能手机                                                         | `(iPhone 8, iPhone 8)` |
| 那个型号ipad是最便宜的，尤其是ipad pro里面的？？                                                                    | `(ipad, ipad)`         |
| Samsung Galaxy是三星电子公司设计、生产并退出市场的一系列移动计算设备                                                 | `(Samsung Galaxy,)`    |

在模型从文本中抽取的所有实体中，**有多少实体模型的判断是正确的**？
注意如果实体的跨度span不完整的话也被认为是一个错误！
小技巧：数一数模型 _应该_ 抽取出的实体数目，然后数一数模型 _实际中_ 抽取正确的实体数目，
把后者除以前者也就是全部正确实体的数目就可以得到准确率。

<choice>

<opt text="45%">
试着数数模型正确抽取的实体数目，然后除以模型 _应该_ 抽取出的全部正确实体的数目。

</opt>

<opt text="60%">

试着数数模型正确抽取的实体数目，然后除以模型 _应该_ 抽取出的全部正确实体的数目。

</opt>

<opt text="70%" correct="true">

在我们的测试数据上模型的准确率是70%。

</opt>

<opt text="90%">

试着数数模型正确抽取的实体数目，然后除以模型 _应该_ 抽取出的全部正确实体的数目。

</opt>

</choice>

</exercise>

<exercise id="9" title="模型训练最佳实践" type="slides">

<slides source="chapter4_03_training-best-practices">
</slides>

</exercise>

<exercise id="10" title="好数据vs烂数据">

这是一段摘抄，来自于一个训练集试图在旅行者的评论中标注实体类型
`TOURIST_DESTINATION`（游客目的地）。

```python
TRAINING_DATA = [
    (
        "我去年去了西安，那里的城墙很壮观！",
        {"entities": [(4, 5, "TOURIST_DESTINATION")]},
    ),
    (
        "人一辈子一定要去一趟爸黎，但那里的埃菲尔铁塔有点无趣。",
        {"entities": [(5, 6, "TOURIST_DESTINATION")]},
    ),
    (
        "深圳也有个巴黎的埃菲尔铁塔，哈哈哈",
        {"entities": []}
    ),
    (
        "北京很适合暑假去：长城、故宫，还有各种好吃的小吃！",
        {"entities": [(0, 1, "TOURIST_DESTINATION")]},
    ),
]
```

### 第一部分

为什么这段数据和标注方法有问题？

<choice>

<opt text="一个地方是不是游客目的地是一个主观看法而不是客观绝对的，所以实体识别器很难学习到。" correct="true">

一个更好的方法应该是只标注`"GPE"`（地理政治实体）或者是`"LOCATION"`（位置实体），然后用基于规则的系统
来判断这个实体在语境中是不是游客目的地，比如我们可以在知识库中寻找该实体类别或者在旅行百科
中查询这些实体。

</opt>

<opt text="埃菲尔铁塔为了保持一致也应该被标注为游客目的地，不然扰乱模型的判断。">

虽然Paris确实有可能是一个游客目的地，但这恰恰表明了这种标注的方法有多么主观，
以及决定标签是否符合这个实体有多么困难。结果就是我们的实体识别器也很难学习到这种区别。

</opt>

<opt text="像拼写错误的'爸黎'这种非常罕见的词库以外的词就不应该被标注为实体。">

就算是不常见的或者拼写错误的词也是可以被标注为实体的。实际上基于语境来判断拼写错误的文本
的类别恰恰是统计实体识别模型的一大优势。

</opt>

</choice>

### 第二部分

- 重写`TRAINING_DATA`使其标签为`"GPE"`（城市、州省、国家）而非`"TOURIST_DESTINATION"`。
- 别忘了添加那些数据中本来未被标注为`"GPE"`的实体的元组。

<codeblock id="04_10">

- 对于那些已经标注过的span，我们只需要将其标签名从`"TOURIST_DESTINATION"`换为`"GPE"`。
- 有一段文本包含了城市和州省实体但还没有被标注。要加入实体的跨度span，我们需要数一数字符
  来找出实体的span是从哪里开始和从哪里结束。然后把`(start, end, label)`元组加到实体中。

</codeblock>

</exercise>

<exercise id="11" title="训练多个标签">

这里是某个数据集的一个样品，我们创建它来训练一个新的实体种类`"WEBSITE"`。
原始的数据集包含了几千个句子。这个练习中我们要手动做标注。实际工作中我们
很可能想要用一些标注工具来自动化这一步，比如[Brat](http://brat.nlplab.org/)，
一个很流行的开源方案，或者[Prodigy](https://prodi.gy)，我们自己开发的整合
了spaCy的标注工具。

### 第一部分

- 完成数据中所有`"WEBSITE"`实体的位置参数。如果不想手动数字符数目的话我们可以随时调
用`len()`。

<codeblock id="04_11_01">

- 实体span的起始和终止位置就是其对应字符在文本中的位置。比如一个从位置5开始的实体，
  其起始位置就是`5`。记住终止位置是 _不包含_ 实体的，所以`10`意味着一直到字符10
  _之前_。

</codeblock>

### 第二部分

我们已经用刚才标注好的数据和其它几千个类似的例子训练了一个模型。训练完成之后，这个模型
对`"WEBSITE"`的抽取表现很好，但却识别不了`"PERSON"`了。这是怎么回事？

<choice>

<opt text='对模型来说很难学习到如<code>"PERSON"</code>和<code>"WEBSITE"</code>这样不同的类别。'>

让模型学习到不同类别是完全可能的。比如spaCy的预训练英文模型就可以识别人名、组织名或者
百分数。

</opt>

<opt text='训练数据中没有任何<code>"PERSON"</code>的例子了，所以模型学习到这个标签本身是错误的。' correct="true">

如果`"PERSON"`实体在训练数据中出现但并未被标注，模型就会学到这些实体不应该被抽取出来。
类似的如果一个已有的实体类别没有出现在训练数据中，模型就会 \"忘记\" 它而停止抽取。

</opt>

<opt text="我们需要返回模型超参数来让两种实体类别都被识别出来。">

超参数确实对模型准确度有影响，但不是这里的问题所在。

</opt>

</choice>

### 第三部分

- 更新训练数据，加入对`"PERSON"`实体"李子柒"和"马云"的标注。

<codeblock id="04_11_02">

- 要添加更多的实体，给列表后面加入另一个`(start, end, label)`元组就行。

</codeblock>

</exercise>

<exercise id="12" title="总结" type="slides">

<slides source="chapter4_04_wrapping-up">
</slides>

</exercise>
