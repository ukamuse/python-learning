import sys
import random
import os

sys.stdout.reconfigure(encoding='utf-8')

# ========================================
# 定数
# ========================================
TOTAL_FLOORS = 5
EVENTS_PER_FLOOR = 4

RESOURCE_NAMES = {
    "energy_cell": "エネルギーセル",
    "titanium":    "チタン",
    "nano_parts":  "ナノパーツ",
}

RECIPES = {
    "エネルギーシールド強化": {
        "cost":   {"energy_cell": 3},
        "effect": "max_shield",
        "value":  30,
        "desc":   "最大シールド +30",
    },
    "チタン装甲": {
        "cost":   {"titanium": 2},
        "effect": "defense",
        "value":  5,
        "desc":   "防御力 +5",
    },
    "量子ブレード": {
        "cost":   {"titanium": 1, "nano_parts": 2},
        "effect": "attack",
        "value":  10,
        "desc":   "攻撃力 +10",
    },
    "自動採掘ドローン": {
        "cost":   {"nano_parts": 2},
        "effect": "auto_mine",
        "value":  0,
        "desc":   "フロア開始時に自動で資源採掘",
    },
    "ナノ修復キット": {
        "cost":   {"energy_cell": 2},
        "effect": "heal",
        "value":  30,
        "desc":   "シールド即時 +30（消耗品）",
    },
}

ENEMIES = {
    1: [
        {"name": "ロスト・ドローン",   "hp": 22,  "attack": 7,  "defense": 0},
        {"name": "廃棄ユニット",       "hp": 28,  "attack": 6,  "defense": 2},
    ],
    2: [
        {"name": "機械兵 MK-I",        "hp": 42,  "attack": 12, "defense": 3},
        {"name": "警備ドローン",       "hp": 36,  "attack": 14, "defense": 2},
    ],
    3: [
        {"name": "機械兵 MK-II",       "hp": 58,  "attack": 16, "defense": 5},
        {"name": "重装甲ユニット",     "hp": 72,  "attack": 12, "defense": 8},
    ],
    4: [
        {"name": "エリート・ガード",   "hp": 78,  "attack": 20, "defense": 8},
        {"name": "量子キャノン砲台",   "hp": 62,  "attack": 25, "defense": 5},
    ],
    5: [
        {"name": "コアAI 《NEXUS》",   "hp": 200, "attack": 28, "defense": 12},
    ],
}


# ========================================
# ユーティリティ
# ========================================
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def hp_bar(current, maximum, length=20):
    filled = int(length * current / max(maximum, 1))
    return '█' * filled + '░' * (length - filled)

def cost_text(cost_dict):
    return "  ".join(f"{RESOURCE_NAMES[r]}x{v}" for r, v in cost_dict.items())

def print_header(floor):
    print("╔══════════════════════════════════════════╗")
    print(f"║   ◈ DEEP CORE SYSTEM  //  SECTOR {floor:02d}/{TOTAL_FLOORS:02d}   ║")
    print("╚══════════════════════════════════════════╝")

def print_status(player):
    bar = hp_bar(player['shield'], player['max_shield'])
    print(f"\n  [ SHIELD ]  {bar}  {player['shield']:3d} / {player['max_shield']:3d}")
    print(f"  [ ATK ] {player['attack']:3d}   [ DEF ] {player['defense']:3d}")
    print(f"\n  [ RESOURCES ]")
    for key, name in RESOURCE_NAMES.items():
        print(f"    {name:<16}: {player['resources'][key]}")

def wait(msg="  [ ENTER ] >> 続行"):
    input(f"\n{msg}")


# ========================================
# プレイヤー
# ========================================
def new_player():
    return {
        "shield":     100,
        "max_shield": 100,
        "attack":     10,
        "defense":    0,
        "resources":  {"energy_cell": 0, "titanium": 0, "nano_parts": 0},
        "upgrades":   [],
        "auto_mine":  False,
    }


# ========================================
# 戦闘
# ========================================
def combat(player, floor):
    template = random.choice(ENEMIES.get(floor, ENEMIES[4]))
    enemy = template.copy()

    print(f"\n  ⚠  警告 ── {enemy['name']} が接近中...")
    wait("  [ ENTER ] >> 戦闘開始")

    while enemy['hp'] > 0 and player['shield'] > 0:
        clear_screen()
        print_header(floor)
        print(f"\n  ╔ COMBAT ══════════════════════════════╗")
        print(f"  ║  {enemy['name']:<20}                ║")
        enemy_bar = hp_bar(enemy['hp'], template['hp'], 15)
        print(f"  ║  HP: {enemy_bar} {enemy['hp']:<5}          ║")
        print(f"  ╚══════════════════════════════════════╝")
        print_status(player)
        print("\n  ──────────────────────────────────────")
        print("\n  [1] >> 攻撃する")
        print("  [2] >> 撤退する（シールド -10）")

        choice = input("\n  COMMAND > ").strip()

        if choice == "1":
            dmg = max(1, player['attack'] - enemy['defense'])
            enemy['hp'] -= dmg
            print(f"\n  >> {dmg} ダメージを与えた！")

            if enemy['hp'] <= 0:
                print(f"  >> {enemy['name']} を撃破！")
                drop = random.choice(list(RESOURCE_NAMES.keys()))
                amount = random.randint(1, 2)
                player['resources'][drop] += amount
                print(f"  >> {RESOURCE_NAMES[drop]} x{amount} を入手！")
                wait()
                break

            enemy_dmg = max(1, enemy['attack'] - player['defense'])
            player['shield'] -= enemy_dmg
            player['shield'] = max(0, player['shield'])
            print(f"  >> {enemy['name']} の攻撃！  シールド -{enemy_dmg}")
            wait()

        elif choice == "2":
            player['shield'] = max(0, player['shield'] - 10)
            print("  >> 撤退した。  シールド -10")
            wait()
            break

    return player['shield'] > 0


# ========================================
# 採掘
# ========================================
def mine(player, floor):
    base = random.randint(1, 2 + floor // 2)
    gained = {
        "energy_cell": random.randint(0, base),
        "titanium":    random.randint(0, base),
        "nano_parts":  random.randint(0, max(0, base - 1)),
    }
    for key, val in gained.items():
        player['resources'][key] += val

    print("\n  ◈ 採掘完了！")
    for key, val in gained.items():
        if val > 0:
            print(f"     {RESOURCE_NAMES[key]} +{val}")


# ========================================
# 製造ターミナル
# ========================================
def craft_menu(player):
    while True:
        clear_screen()
        print("╔══════════════════════════════════════════╗")
        print("║      ◈ 製造ターミナル // FABRICATOR      ║")
        print("╚══════════════════════════════════════════╝")
        print_status(player)
        print("\n  ──────────────────────────────────────")

        items = list(RECIPES.items())
        for i, (name, recipe) in enumerate(items, 1):
            already = name in player['upgrades'] and recipe['effect'] != "heal"
            can = all(player['resources'][r] >= v for r, v in recipe['cost'].items())

            if already:
                tag = "[ 製造済 ]"
            elif can:
                tag = "[ 製造可 ]"
            else:
                tag = "[ 素材不足 ]"

            print(f"\n  [{i}] {name}  {tag}")
            print(f"       {recipe['desc']}")
            print(f"       コスト: {cost_text(recipe['cost'])}")

        print("\n  [0] >> 戻る")
        choice = input("\n  COMMAND > ").strip()

        if choice == "0":
            break
        if not choice.isdigit() or not (1 <= int(choice) <= len(items)):
            continue

        name, recipe = items[int(choice) - 1]

        if name in player['upgrades'] and recipe['effect'] != "heal":
            print("  >> すでに製造済みです")
            wait()
            continue

        if not all(player['resources'][r] >= v for r, v in recipe['cost'].items()):
            print("  >> 素材が不足しています")
            wait()
            continue

        for r, v in recipe['cost'].items():
            player['resources'][r] -= v

        effect = recipe['effect']
        if effect == "max_shield":
            player['max_shield'] += recipe['value']
            player['shield'] = min(player['shield'] + recipe['value'], player['max_shield'])
        elif effect == "defense":
            player['defense'] += recipe['value']
        elif effect == "attack":
            player['attack'] += recipe['value']
        elif effect == "auto_mine":
            player['auto_mine'] = True
        elif effect == "heal":
            player['shield'] = min(player['shield'] + recipe['value'], player['max_shield'])

        player['upgrades'].append(name)
        print(f"\n  >> {name} の製造完了！")
        wait()


# ========================================
# フロア探索
# ========================================
def run_floor(player, floor):
    clear_screen()
    print_header(floor)

    if player['auto_mine']:
        e = random.randint(1, 2)
        t = random.randint(0, 1)
        n = random.randint(0, 1)
        player['resources']['energy_cell'] += e
        player['resources']['titanium'] += t
        player['resources']['nano_parts'] += n
        print(f"\n  >> 自動採掘ドローン稼働：資源を回収しました")

    wait("  [ ENTER ] >> セクター探索開始")

    if floor == TOTAL_FLOORS:
        clear_screen()
        print_header(floor)
        print("\n  !! コアAIの反応を検知 ── FINAL BOSS !!")
        wait()
        return combat(player, floor)

    pool = ["enemy", "enemy", "mine", "mine", "trap", "rest", "craft"]
    events = random.sample(pool, EVENTS_PER_FLOOR)

    for step, event in enumerate(events, 1):
        if player['shield'] <= 0:
            return False

        clear_screen()
        print_header(floor)
        print_status(player)
        print("\n  ──────────────────────────────────────")
        print(f"\n  探索進捗: {step} / {EVENTS_PER_FLOOR}")
        print("\n  [1] >> 前進する")
        print("  [2] >> 製造ターミナルを開く")

        action = input("\n  COMMAND > ").strip()
        if action == "2":
            craft_menu(player)
            if player['shield'] <= 0:
                return False

        clear_screen()
        print_header(floor)

        if event == "enemy":
            alive = combat(player, floor)
            if not alive:
                return False

        elif event == "mine":
            print("\n  ◈ 資源デポジットを発見！")
            mine(player, floor)
            wait()

        elif event == "trap":
            dmg = random.randint(5, 15)
            player['shield'] = max(0, player['shield'] - dmg)
            print(f"\n  ⚠  トラップ発動！  シールド -{dmg}")
            wait()

        elif event == "rest":
            heal = random.randint(15, 30)
            player['shield'] = min(player['shield'] + heal, player['max_shield'])
            print(f"\n  ◈ 修復ステーション発見！  シールド +{heal}")
            wait()

        elif event == "craft":
            print("\n  ◈ 製造ターミナルを発見！")
            wait("  [ ENTER ] >> 開く")
            craft_menu(player)

    return player['shield'] > 0


# ========================================
# メインループ
# ========================================
def main():
    clear_screen()
    print("╔══════════════════════════════════════════╗")
    print("║                                          ║")
    print("║    D E E P   C O R E   S Y S T E M      ║")
    print("║                                          ║")
    print("║    地下工場ダンジョン  //  Ver. 1.0      ║")
    print("║                                          ║")
    print("╚══════════════════════════════════════════╝")
    print()
    print("  深層コアに潜入し、コアAI《NEXUS》を撃破せよ。")
    print("  資源を集め、装備を製造し、5セクターを突破しろ。")
    print()
    print("  [ ゲームの基本 ]")
    print("  　各セクターでイベントに遭遇しながら前進する。")
    print("  　敵を倒して資源を集め、製造ターミナルで強化しよう。")
    print("  　シールドが0になるとゲームオーバー。")
    wait("  [ ENTER ] >> ゲーム開始")

    player = new_player()

    for floor in range(1, TOTAL_FLOORS + 1):
        survived = run_floor(player, floor)

        if not survived or player['shield'] <= 0:
            clear_screen()
            print("╔══════════════════════════════════════════╗")
            print("║   ✖   SYSTEM FAILURE  //  GAME OVER      ║")
            print("╚══════════════════════════════════════════╝")
            print(f"\n  セクター {floor:02d} にて活動停止。")
            print("  コアAIは深層で今も稼働し続けている...")
            wait("  [ ENTER ] >> 終了")
            return

        if floor < TOTAL_FLOORS:
            clear_screen()
            print_header(floor)
            print(f"\n  ✓  セクター {floor:02d} クリア！  次の階層へ降下する...")
            print_status(player)
            wait("  [ ENTER ] >> 次のセクターへ")

    clear_screen()
    print("╔══════════════════════════════════════════╗")
    print("║   ★   MISSION COMPLETE  //  CLEARED     ║")
    print("╚══════════════════════════════════════════╝")
    print()
    print("  コアAI《NEXUS》を撃破！")
    print("  深層工場システムの制圧に成功した。")
    print_status(player)
    wait("  [ ENTER ] >> 終了")


if __name__ == "__main__":
    main()
