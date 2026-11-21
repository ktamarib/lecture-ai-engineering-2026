from unittest.mock import Mock

import app.ask as ask_module


def test_ask_uses_model_default_temperature_when_unset(monkeypatch):
    client = Mock()
    chat = client.chats.create.return_value
    chat.send_message.return_value.text = "answer"
    monkeypatch.setattr(ask_module.genai, "Client", Mock(return_value=client))
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")
    monkeypatch.setattr(ask_module, "TEMPERATURE", None)

    created_chat = ask_module.create_chat(client)
    assert ask_module.ask("question", created_chat) == "answer"
    client.chats.create.assert_called_once_with(
        model=ask_module.MODEL,
        config=None,
    )
    chat.send_message.assert_called_once_with("question")


def test_ask_passes_configured_temperature(monkeypatch):
    client = Mock()
    chat = client.chats.create.return_value
    chat.send_message.return_value.text = "answer"
    monkeypatch.setattr(ask_module.genai, "Client", Mock(return_value=client))
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")
    monkeypatch.setattr(ask_module, "TEMPERATURE", 0.8)

    created_chat = ask_module.create_chat(client)
    assert ask_module.ask("question", created_chat) == "answer"
    config = client.chats.create.call_args.kwargs["config"]
    assert config.temperature == 0.8
    chat.send_message.assert_called_once_with("question")


def test_main_reuses_chat_for_follow_up_questions(monkeypatch, capsys):
    client = Mock()
    chat = client.chats.create.return_value
    chat.send_message.return_value.text = "answer"
    monkeypatch.setattr(ask_module.genai, "Client", Mock(return_value=client))
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")
    monkeypatch.setattr(ask_module, "TEMPERATURE", None)
    monkeypatch.setattr("sys.argv", ["app.ask"])
    monkeypatch.setattr("builtins.input", Mock(side_effect=["follow-up", ""]))

    ask_module.main()

    ask_module.genai.Client.assert_called_once_with(api_key="test-key")
    client.chats.create.assert_called_once()
    assert [call.args[0] for call in chat.send_message.call_args_list] == [
        ask_module.DEFAULT_QUESTION,
        "follow-up",
    ]
    assert capsys.readouterr().out.count("answer") == 2
