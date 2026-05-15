import sys
sys.stdout.reconfigure(encoding='utf-8')

# ── 文字列（テキスト）の変数 ──
name = "うかむせ"
message = "さん、こんにちは！"

print(name + message)   # + で文字列をつなげられる

# ── 数字の変数 ──
price = 500    # 値段
tax = 0.1       # 消費税10%
total = price + price * tax

print("税抜き価格:", price, "円")
print("税込み価格:", total, "円")

# ── f文字列（変数をきれいに埋め込む方法） ──
print(f"{name}さんの合計金額は {total} 円です。")
