# プロジェクト概要

Claude Code と Python の基礎を習得するための学習フォルダ。
Week1でPython基礎（変数・if・for・関数）を完了済み。

# 私のスキルレベル

- Python歴: 2週間（完全初心者からスタート）
- 理解済み: 変数、f文字列、if/elif/else、for文、関数、git基本操作
- 未学習: クラス、ファイル入出力、外部ライブラリ、Web系
- 使用環境: Windows 11 / VS Code / Python 3.x

# コミュニケーションのルール

- 説明は必ず日本語で
- 専門用語を使うときは括弧内に簡単な説明を添える（例: 引数（関数に渡す値））
- コードを書いたら「このコードが何をしているか」を1〜2行で説明する
- 一度に教えることは1トピックまで。詰め込まない
- エラーが出たら「原因」と「修正方法」をセットで教える

# コードのルール

- コメントは日本語で書く（英語コメント禁止）
- ファイル名はスネークケース（単語をアンダースコアでつなぐ: my_file.py）
- 初心者向けにシンプルさを最優先。凝った書き方は避ける
- 文字化け対策として先頭に必ず以下を入れる:
  import sys
  sys.stdout.reconfigure(encoding='utf-8')

# このフォルダのファイル構成

- hello_world.py   : 最初の練習（print文）
- variables.py     : 変数とf文字列
- if_practice.py   : 条件分岐
- for_practice.py  : for文とリスト
- functions.py     : 関数の定義と呼び出し

# よく使うコマンド

- python ファイル名.py   : Pythonファイルを実行
- git status             : Gitの現在の状態を確認
- git add ファイル名     : コミット対象に追加
- git log --oneline      : コミット履歴を確認
