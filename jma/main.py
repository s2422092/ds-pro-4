import flet as ft
import requests

# APIから地域データを取得
data_json = requests.get("http://www.jma.go.jp/bosai/common/const/area.json").json()

def main(page: ft.Page):
    # メニューバーを追加
    page.add(
        ft.AppBar(
            title=ft.Text("天気予報",color=ft.colors.WHITE),  # メニューバーのタイトル
            actions=[  # メニューのアイコンを追加
                ft.IconButton(ft.icons.SETTINGS, on_click=lambda e: print("Settings clicked"))  # 設定ボタン
            ],
            
            bgcolor=ft.colors.BLUE_700  # メニューバーの背景色
        )
    )

    # 地域名リストを作成
    controls = []
    
    # centers の中から親地域名を抽出し、その下の子地域を表示
    for region_id, region_info in data_json["centers"].items():
        # 親地域（名前）を取得
        parent_region_name = region_info["name"]
        
        # 子地域のリストを作成
        child_controls = []
        for child_id in region_info["children"]:
            # 子地域の名前を取得
            child_region_name = data_json["offices"].get(child_id, {}).get("name", f"Unknown Region {child_id}")
            child_controls.append(ft.ListTile(title=ft.Text(child_region_name)))
        
        # 親地域をExpansionTileとして表示
        controls.append(
            ft.Container(
                content=ft.ExpansionTile(
                    title=ft.Text(parent_region_name),  # 親地域名をタイトルとして表示
                    subtitle=ft.Text("Trailing expansion arrow icon"),
                    affinity=ft.TileAffinity.PLATFORM,
                    maintain_state=True,
                    collapsed_text_color=ft.colors.RED,
                    text_color=ft.colors.RED,
                    controls=child_controls,  # 子地域のリストを追加
                ),
                width=200,  # 幅を200pxに設定（短く）
                alignment=ft.alignment.top_left,  # 左寄せに配置
            )
        )

    # ft.ListViewを使ってスクロール可能にする
    page.add(
        ft.ListView(
            controls=controls,  # ExpansionTileを追加したリスト
            expand=True,  # スクロール可能領域を確保
        )
    )

# Fletアプリケーションを実行
ft.app(main)
