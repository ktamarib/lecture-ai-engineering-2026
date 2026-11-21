# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：
  - 第1回では一般論を回答していたが、今回は用語集を確認し、用語集に基づいた回答をしている。
  ```
  講座の用語集によると、LoRAとQLoRAの主な違いは以下の通りです：

  * **LoRA**: 事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法です。学習するパラメータが少なく、アダプタのファイルサイズも小さくなります。
  * **QLoRA**: ベースモデルの重みを4ビットなどに**量子化**してメモリを節約したうえで、LoRAによる学習を行う手法です。これにより、より大きなモデルを小さなGPUでも扱えるようになります。

  関係する回：第2回
  ```
- `--trace` で見えたツール呼び出し（ツール名と引数）：
  ```
  [tool call]   search_glossary({'query': 'LoRA'})
  [tool call]   search_glossary({'query': 'QLoRA'})
  [tool return] search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…
  [tool return] search_glossary -> [{"term": "QLoRA", "lecture": 2, "definition": "ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法。より大きなモデルを小さなGPUで扱える。本講座の第2…
  [usage] RunUsage(cost=Decimal('0.0008119'), details={'text_prompt_tokens': 1198}, input_text_tokens=1198, input_tokens=1198, output_tokens=181, requests=2, tool_calls=2)
  ```
- 1つの質問での LLM 呼び出し回数（`requests`）：2
- 追加したツールと、docstring に書いた説明：
  - make_quiz
  """指定した回の用語から 1つを選び、
  確認問題と答えを返す。
  「第2回の確認問題を出して」のように、
  復習用の問題を求められたときに使う。
  """

## 宿題

- 取り組んだレベル：基礎
- やったこと：
　- docstringの「用語を1つだけ入れる」を「まとめて入れる」に変更した。
- 結果：tool_calls=2 -> 1に減った。
```
「用語を1つだけ入れる」場合
[tool call]   search_glossary({'query': 'LoRA'})
[tool call]   search_glossary({'query': 'QLoRA'})
[tool return] search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…
[tool return] search_glossary -> [{"term": "QLoRA", "lecture": 2, "definition": "ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法。より大きなモデルを小さなGPUで扱える。本講座の第2…
[usage] RunUsage(cost=Decimal('0.0008768'), details={'text_prompt_tokens': 1356}, input_text_tokens=1356, input_tokens=1356, output_tokens=188, requests=2, tool_calls=2)

「まとめて入れる」場合
[tool call]   search_glossary({'query': 'LoRA QLoRA'})
[tool return] search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…
[usage] RunUsage(cost=Decimal('0.0008204'), details={'text_prompt_tokens': 1043}, input_text_tokens=1043, input_tokens=1043, output_tokens=203, requests=2, tool_calls=1)
```
- 気づき・疑問：
  - tool_calls=1に減って確かにまとめてqueryに2単語を入れていることが分かる。
  - requests=2のまま。tool_callsはLLMがツール呼び出し依頼をした回数。requestsはLLMとの通信回数。
  - search_glossaryの挙動を見ると、tool returnの結果はLoLAだけ戻っているように見えたが、先頭120文字だけ出力するようにされていたので、全文出力するように変更すると、確かに2単語の結果がまとめて返ってきていた。
