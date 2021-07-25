---
type: slides
---

# ルールベースマッチ

Notes: この演習では、spaCyのmatcherについて学びます。
matcherを使えば、単語やフレーズを見つけるルールを書くことができます。

---

# 正規表現じゃだめなの？

- 単なる文字列ではなく、`Doc`や`Token`にマッチします
- トークンの文字列だけでなく、属性を条件にできます
- (トークンに対する)モデルの予測結果も条件にできます
  - 例："duck"（動詞） vs. "duck"（名詞）

Notes: 正規表現と異なり、単なる文字列ではなく`Doc`や`Token`にマッチします。

そして正規表現よりも柔軟です。文字列だけでなくトークンの属性も対象に検索することができます。

さらに、モデルの予測結果をもとにしたルールを書くこともできます。

例えば、「duck」という単語が名詞ではなく動詞の時のみマッチする、というルールを書けます。

---

# マッチのパターン

トークンに対する条件のリスト

1. トークンの文字列にマッチ　

```python
[{"TEXT": "iPhone"}, {"TEXT": "X"}]
```

2. トークンの属性にマッチ

```python
[{"LOWER": "iphone"}, {"LOWER": "x"}]
```

3. 様々な属性を使用したマッチ

```python
[{"POS": "NOUN"}, {"POS": "ADP"}, {"LEMMA": "買う"}]
```

Notes: 辞書のリストでマッチのパターンを作成します。
各辞書が各トークンに対する条件になります。
辞書のキーはトークンの属性を、辞書の値はマッチする値を表します。

1は、文字列がそれぞれ「iPhone」と「X」である二つのトークンからなるトークン列を検索します。

2は、小文字化した場合に「iphone」と「x」からなるトークン列を検索します。  
このように語彙属性に対しマッチさせることができます。

3は、名詞、接置詞のトークンの後に基本形が「買う」であるトークンが続くトークン列を検索します。  
つまり、「牛乳を買っている」や「花を買った」等にマッチします。  
このように、モデルの予測結果を条件にマッチさせることができます。

---

# Matcherをつかう（1）

```python
import spacy

# Matcherをインポート
from spacy.matcher import Matcher

# モデルをロードし、nlpオブジェクトを作成
nlp = spacy.load("ja_core_news_sm")

# matcherを共有語彙データを用いて初期化
matcher = Matcher(nlp.vocab)

# パターンをmatcherに追加
pattern = [{"TEXT": "iPhone"}, {"TEXT": "X"}]
matcher.add("IPHONE_PATTERN", None, pattern)

# テキストを処理
doc = nlp("これから発売されるiPhone Xの発売日がリークした")

# matcherをdocに対して呼び出し
matches = matcher(doc)
```

Notes: パターンを使うには、まず最初に`spacy.matcher`からMatcherをインポートします。

そしてモデルをロードし、`nlp`オブジェクトを作成します。

Matcherは共有語彙データ`nlp.vocab`を用いて初期化します。
これについては後ほど詳しくみていきます。とりあえず、このようにして初期化する必要があると覚えておいてください。

パターンは、`matcher.add`メソッドを用いて登録します。
第一引数は、それぞれのパターンを識別するためのユニークIDです。
第二引数は、任意のコールバック関数です。今は必要ないので、`None`を与えておきます。
第三引数はパターンです。

パターンをマッチさせるには、docオブジェクトに対してmatcherを呼び出します。

matcherを呼び出すと、マッチの結果が返ってきます。

---

# Matcherをつかう（2）

```python
# matcherをdocに対して呼びだす
doc = nlp("これから発売されるiPhone Xの発売日がリークした")
matches = matcher(doc)

# 結果をイテレートする
for match_id, start, end in matches:
    # マッチ結果を取得
    matched_span = doc[start:end]
    print(matched_span.text)
```

```out
iPhone X
```

- `match_id`: パターン名のハッシュ値
  - (整数のハッシュ値になっており`nlp.vocab.strings[match_id]`でUnicode文字列に戻せます)
- `start`: マッチしたスパンの開始インデックス
- `end`: マッチしたスパンの終了インデックス

Notes: matcherをdocオブジェクトに対して呼び出すと、タプルのリストがかえってきます。

それぞれのタプルは、マッチID、マッチしたスパンの開始インデックス、終了インデックスの3つの要素からなります。

この返り値をイテレートし、開始インデックスと終了インデックスで`doc`をスライスすることで、`Span`オブジェクトを作ることができます。

---

# 語彙属性のマッチ

```python
pattern = [
    {"IS_DIGIT": True},
    {"LOWER": "fifa"},
    {"LOWER": "world cup"},
    {"IS_PUNCT": True}
]
```

```python
doc = nlp("2018 FIFA World Cup: フランスが勝った!")
```

```out
2018 FIFA World Cup:
```

Notes: これは、語彙属性を用いたより複雑なマッチの例です。

次の4つからなるトークン列を探索しています：

- 数字からなるトークン
- 2つのトークン「fifa」、「world cup」（ただし大文字小文字を区別しない）
- 句読点記号

このパターンは、「2018 FIFA World Cup:」というトークン列にマッチします。

---

# その他のトークン属性のマッチ

```python
pattern = [
    {"POS": "NOUN"},
    {"POS": "ADP"},
    {"LEMMA": "飼う", "POS": "VERB"}
]
```

```python
doc = nlp("犬を飼っていたけど、今はたくさん猫を飼うようになった。")
doc.is_tagged = True
```

```out
犬を飼っ
猫を飼う
```

Note: この例では、次の3つのトークンからなる列を探索しています：

- 名詞
- 接置詞
- 「飼う」という動詞

このパターンは「犬を飼っ」と「猫を飼う」にマッチします。

(※ spaCy 2.3.2では、日本語モデルで品詞タグ付けが実行されていると認識されないバグがあります。そのため、`doc.is_tagged = True`でタグ付け済みであると明示的に指定しています。詳細は[spaCyのIssue](https://github.com/explosion/spaCy/pull/5803)を参照してください)

---

# 演算子と量指定子を使う(1)

```python
pattern = [
    {"POS": "NOUN"},
    {"POS": "ADP", "OP": "?"},  # Optional: 0個か1個にマッチ
    {"LEMMA": "買う"},
]
```

```python
doc = nlp("スマートフォン買ったので、アプリも買ってる")
```

```out
スマートフォン買っ
アプリも買っ
```

Notes: 演算子と量指定子を使うと、マッチするトークンの量を指定することができます。
これらは「OP」キーによって指定します。

ここで「?」演算子はトークンのマッチをオプショナルにしています。
つまりこのパターンは、
見出し語の名詞+接置詞0個か1個+「買う」
にマッチします。

---

# 演算子と量指定子を使う(2)

| 例 | 説明 |
| ------------- | ---------------------------- |
| `{"OP": "!"}` | 否定：0個にマッチ |
| `{"OP": "?"}` | Optional: 0個か1個にマッチ |
| `{"OP": "+"}` | 1個以上にマッチ |
| `{"OP": "*"}` | 0個以上にマッチ |

Notes: 「OP」には以下のいずれかを指定することができます：

「!」トークンの否定。0個にマッチします。

「?」Optional。0個か1個にマッチします。

「+」1個以上にマッチします。

「\*」0個以上にマッチします。

演算子を使えばより強力なパターンを作ることができますが、より複雑になってしまいます。上手に使いましょう。

---

# Let's practice!

Notes: トークンベースのマッチングは、情報抽出の可能性を大きく広げてくれます。
それでは、実際にいくつかのパターンを書いて試してみましょう。