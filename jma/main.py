import flet as ft
import requests

# APIから地域データを取得
area_json = requests.get("http://www.jma.go.jp/bosai/common/const/area.json").json()

def get_weather_data(region_code: str):
    """指定された地域コードに対して天気予報を取得する"""
    weather_url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{region_code}.json"
    response = requests.get(weather_url)
    
    # APIレスポンスの確認
    if response.status_code != 200:
        print(f"Weather data for {region_code} not found!")
        return {}
    
    return response.json()

def main(page: ft.Page):
    # メニューバーを追加
    page.add(
        ft.AppBar(
            title=ft.Text("天気予報", color=ft.colors.WHITE),
            actions=[
                ft.IconButton(ft.icons.SETTINGS, on_click=lambda e: print("Settings clicked"))
            ],
            bgcolor=ft.colors.BLUE_700
        )
    )

    # 地域名リストを作成
    controls = []
import flet as ft
import requests

# APIから地域データを取得
area_json = requests.get("http://www.jma.go.jp/bosai/common/const/area.json").json()

def get_weather_data(region_code: str):
    """指定された地域コードに対して天気予報を取得する"""
    weather_url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{region_code}.json"
    response = requests.get(weather_url)
    
    # APIレスポンスの確認
    if response.status_code != 200:
        print(f"Weather data for {region_code} not found!")
        return {}
    
    # レスポンスデータの確認
    print(f"Weather data for {region_code}: {response.json()}")
    
    return response.json()

def main(page: ft.Page):
    # メニューバーを追加
    page.add(
        ft.AppBar(
            title=ft.Text("天気予報", color=ft.colors.WHITE),
            actions=[
                ft.IconButton(ft.icons.SETTINGS, on_click=lambda e: print("Settings clicked"))
            ],
            bgcolor=ft.colors.BLUE_700
        )
    )

    # 地域名リストを作成
    controls = []

    # centers の中から親地域名を抽出し、その下の子地域を表示
    for region_id, region_info in area_json["centers"].items():
        parent_region_name = region_info["name"]
        
        print(f"Processing parent region: {parent_region_name}")  # 親地域のデバッグ

        # 子地域のリストを作成
        child_controls = []

        # 各子地域に対応する天気予報データを取得
        for child_id in region_info["children"]:
            child_region_name = area_json["offices"].get(child_id, {}).get("name", f"Unknown Region {child_id}")

            print(f"  Processing child region: {child_region_name}")  # 子地域のデバッグ

            # 天気予報データを取得
            weather_data = get_weather_data(child_id)
            
            # 天気情報を確認
            if weather_data:
                weather_info = "情報がありません"
                # 天気データがある場合、最初の予報を表示
                forecast = weather_data[0].get('timeSeries', [{}])[0].get('areas', [{}])[0].get('weatherCodes', [])
                if forecast:
                    weather_info = forecast[0]  # 予報コードを表示
            else:
                weather_info = "情報がありません"

            # 子地域のリストアイテムを作成
            child_controls.append(
                ft.ListTile(
                    title=ft.Text(child_region_name),
                    subtitle=ft.Text(f"天気予報: {weather_info}")
                )
            )

        # 親地域をExpansionTileとして表示
        controls.append(
            ft.Container(
                content=ft.ExpansionTile(
                    title=ft.Text(parent_region_name),  # 親地域名をタイトルとして表示
                    subtitle=ft.Text("子地域を表示"),
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

    # `Row` レイアウトで左半分にコンテンツを表示、右半分を白紙にする
    page.add(
        ft.Row(
            controls=[
                ft.Column(
                    controls=controls,  # 左側にExpansionTileを追加したリスト
                    expand=True,  # 左側を拡張してスペースを取る
                ),
                ft.Container(
                    width=600,  # 右側に空白スペースを作る
                    bgcolor=ft.colors.WHITE  # 白い背景を設定
                )
            ],
            expand=True  # 全体的に広げる
        )
    )

# Fletアプリケーションを実行
ft.app(main)
