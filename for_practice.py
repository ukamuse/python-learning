import sys
sys.stdout.reconfigure(encoding='utf-8')

# ── 基本のfor文 ──
print("=== 買い物リスト ===")

items = ["りんご", "バナナ", "みかん", "ぶどう"]

for item in items:
    print(f"・{item}")

# ── 番号付きで表示する（enumerate） ──
print("\n=== 番号付きリスト ===")

for i, item in enumerate(items, start=1):
    print(f"{i}番目: {item}")

# ── 数字のリストで計算する ──
print("\n=== 合計金額 ===")

prices = [150, 200, 100, 300]  # 各商品の値段
total = 0

for price in prices:
    total = total + price  # 合計に足していく

print(f"合計: {total} 円")

# ── range()で回数を指定する ──
print("\n=== 3回繰り返す ===")

for i in range(3):
    print(f"{i + 1}回目の処理")

# ── if文と組み合わせる ──
print("\n=== 500円以上の商品だけ表示 ===")

products = [
    ("りんご", 150),
    ("高級メロン", 3000),
    ("バナナ", 200),
    ("松阪牛", 8000),
    ("松阪牛2", 1200),
]

for name, price in products:
    if price >= 500:
        print(f"{name}: {price}円 ← 高級品！")
    else:
        print(f"{name}: {price}円")
