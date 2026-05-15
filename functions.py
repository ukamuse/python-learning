import sys
sys.stdout.reconfigure(encoding='utf-8')

# ── 基本の関数（引数あり・戻り値あり） ──
def calc_tax(price):
    """税込み価格を計算して返す"""
    return price + price * 0.1

print("=== 税込み計算 ===")
print(f"500円 → {calc_tax(500)} 円")
print(f"3000円 → {calc_tax(3000)} 円")


# ── 複数の引数を受け取る関数 ──
def greet(name, rank="通常会員"):
    """挨拶メッセージを返す（rankはデフォルト値あり）"""
    return f"{name}さん（{rank}）、いらっしゃいませ！"

print("\n=== 挨拶 ===")
print(greet("うかむせ"))                    # rankを省略
print(greet("うかむせ", "ゴールド会員"))    # rankを指定


# ── 複数の値を返す関数 ──
def calc_summary(prices):
    """合計・平均・最高値を一度に返す"""
    total = sum(prices)
    average = total / len(prices)
    highest = max(prices)
    return total, average, highest

print("\n=== 購入履歴の集計 ===")
history = [500, 1200, 300, 8000, 150]
total, average, highest = calc_summary(history)
print(f"合計:   {total} 円")
print(f"平均:   {average} 円")
print(f"最高値: {highest} 円")


# ── 関数 + for文 + if文を組み合わせる ──
def judge_rank(total):
    """合計金額からランクを判定する"""
    if total >= 5000:
        return "ゴールド"
    elif total >= 2000:
        return "シルバー"
    else:
        return "通常"

print("\n=== 会員ランク判定 ===")
customers = [
    ("うかむせ", 6800),
    ("田中", 2500),
    ("山田", 800),
]

for name, spent in customers:
    rank = judge_rank(spent)
    print(f"{name}さん: {spent}円 → {rank}会員")
