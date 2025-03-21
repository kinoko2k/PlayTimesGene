import requests
import time

def get_mcid(uuid):
    url = f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid.replace('-', '')}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json().get("name")
        elif response.status_code == 204:
            print(f"エラー: {uuid}に該当のMCIDが見つかりません。")
            return "Unknown"
        else:
            print(f"エラー: {uuid}の取得に失敗しました。({response.status_code})")
            return "Unknown"
    except requests.RequestException as e:
        print(f"エラー: {e}")
        return "Unknown"
try:
    with open("playtimes.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
except FileNotFoundError:
    print("playtimes.txtが見つかりません。")
    exit()

output_lines = []
for line in lines:
    try:
        uuid, ticks = line.strip().split(": ")
        ticks = int(ticks)
    except ValueError:
        print(f"フォーマットが正しくありません。{line.strip()}")
        continue
    total_seconds = ticks // 20
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    time_str = f"{hours}時間 {minutes}分" if hours else f"{minutes}分"
    mcid = get_mcid(uuid)
    output_lines.append(f"{mcid}: {time_str}")
    time.sleep(5)

with open("mcid.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))

print("変換が完了しました。")
