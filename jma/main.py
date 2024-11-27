import flet as ft
import requests

# APIから地域データを取得
data_json = requests.get("http://www.jma.go.jp/bosai/common/const/area.json").json()

def main(page: ft.Page):
    # 地域名リストを作成
    regions = []
    
    # centers の中から地域名を抽出
    for region_id, region_info in data_json["centers"].items():
        regions.append(region_info["name"])  # 地域名をリストに追加

    # Containerで複数のExpansionTileを作成
    controls = []
    for region in regions:
        controls.append(
            ft.Container(
                content=ft.ExpansionTile(
                    title=ft.Text(region),  # 地域名をタイトルとして表示
                    subtitle=ft.Text("Trailing expansion arrow icon"),
                    affinity=ft.TileAffinity.PLATFORM,
                    maintain_state=True,
                    collapsed_text_color=ft.colors.RED,
                    text_color=ft.colors.RED,
                    controls=[ft.ListTile(title=ft.Text(f"This is sub-tile for {region}"))],
                ),
                width=300,  # 幅を設定
                alignment=ft.alignment.center,  # 中央に配置
            )
        )

    # すべてのExpansionTileをページに追加
    page.add(ft.Column(controls=controls))

# Fletアプリケーションを実行
ft.app(main)

