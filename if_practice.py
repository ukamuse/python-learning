import sys
sys.stdout.reconfigure(encoding='utf-8')

name = "うかむせ"
total = 3500  # 税込み金額（円）

# ── 基本の if / else ──
if total >= 1000:
    print(f"{name}さん、1000円以上のご購入で送料無料です！")
else:
    print(f"{name}さん、送料無料まであと {1000 - total} 円です。")

# ── 3つ以上の条件： if / elif / else ──
print("--- ポイント付与 ---")

if total >= 3000:
    point = total * 0.05  # 5%還元
    print(f"ゴールド会員：{point} ポイント付与")
elif total >= 1000:
    point = total * 0.03  # 3%還元
    print(f"シルバー会員：{point} ポイント付与")
else:
    point = total * 0.01  # 1%還元
    print(f"通常会員：{point} ポイント付与")

# ── 複数条件を組み合わせる（and / or） ──
print("--- クーポン確認 ---")

has_coupon = True   # クーポンを持っているか
is_member = True    # 会員か

if has_coupon and is_member:
    print("会員クーポン適用：100円引き！")
elif has_coupon or is_member:
    print("割引適用：50円引き！")
else:
    print("割引なし")
