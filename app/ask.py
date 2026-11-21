"""第1回: 会話履歴を保って素のLLMに質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする
    # 回答後に質問を続け、空行で終了

ツールは使わず、同じ実行中の会話履歴を保って質問する。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse

from google import genai
from google.genai import chats
from google.genai import errors
from google.genai import types

from app.config import MODEL, TEMPERATURE, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def create_chat(client: genai.Client) -> chats.Chat:
    config = (
        types.GenerateContentConfig(temperature=TEMPERATURE)
        if TEMPERATURE is not None
        else None
    )
    return client.chats.create(model=MODEL, config=config)


def ask(question: str, chat: chats.Chat) -> str:
    response = chat.send_message(question)

    usage = getattr(response, "usage_metadata", None)
    if usage is not None:
        prompt_tokens = getattr(usage, "prompt_token_count", None) or 0
        output_tokens = getattr(usage, "candidates_token_count", None) or 0
        print(f"[usage] 入力トークン数: {prompt_tokens}, 出力トークン数: {output_tokens}")
    else:
        print("[usage] トークン数の情報は取得できませんでした")

    return response.text


def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMに質問する")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    print("質問を続けられます。空行で終了します。\n")
    question = args.question
    try:
        client = genai.Client(api_key=get_api_key())
        chat = create_chat(client)
        while question:
            print(f"[質問] {question}\n")
            print(ask(question, chat))
            try:
                question = input("\n続けて質問してください（終了するには空行）: ").strip()
            except EOFError:
                print()
                break
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
