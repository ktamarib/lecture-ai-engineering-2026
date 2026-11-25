# 第6回 解答

## 演習

<!-- [tool call] の行は、表示された行をそのまま貼り付けてください。終わらなかった STEP は、空欄のままでかまいません。 -->

- STEP 1 のツールの名前：glossary_search_glossary
- STEP 2 の [tool call]：glossary_search_glossary({'query': '3レベル'})
- STEP 3 の [tool call]：fetch_fetch({'url': 'https://modelcontextprotocol.io/'})
- STEP 4 の [tool call]：aws_aws___search_documentation({'topics': ['general'], 'search_phrase': 'Amazon S3 バージョニング 概要'}), aws_aws___search_documentation({'search_phrase': '"Versioning" "Amazon S3" what is', 'topics': ['general']})
- 気づき・疑問：STEP 4では2回ツールが呼び出されている。awsはサーバ側で検索フレーズを指定できる引数が存在する。

## 宿題

<!-- 基礎・実装・発展のどれか1つに取り組めば完了です。 -->

- 取り組んだレベル：実装
- やったこと：make_quizをmcpサーバから呼び出せるように実装した。
- 結果：範囲外の回答をした際には以下のように適切に範囲外となることを確認した。
  --- trace ---
  [tool call]   glossary_make_quiz({'lecture': 16})
  [tool return] glossary_make_quiz -> {"error": "第16回の用語は見つかりませんでした。"}…
  [usage] 入力 5,613 tokens / 出力 72 tokens / モデル応答 2 回
- 気づき・疑問：すでに関数はtools.pyに用意していたので、全く同様に追加するだけでMCPサーバとして利用できることを確認した。また先生がおっしゃっていたように、ローカルの場合は書き方の問題だけで、必ずしもMCPを介する必要がないことが理解できた。
