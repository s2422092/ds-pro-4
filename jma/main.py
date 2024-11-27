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

    # 右側の空白部分に天気予報情報を表示するためのコンテナ
    weather_details = ft.Text("詳細な天気情報がここに表示されます。")

    # 地域名リストを作成
    controls = []

    # centers の中から親地域名を抽出し、その下の県と地域を表示
    for region_id, region_info in area_json["centers"].items():
        parent_region_name = region_info["name"]
        
        print(f"Processing parent region: {parent_region_name}")  # 親地域のデバッグ

        # 県ごとのリストを作成
        prefecture_controls = []

        # 各県に対応する地域データを取得
        for child_id in region_info["children"]:
            child_region_name = area_json["offices"].get(child_id, {}).get("name", f"Unknown Region {child_id}")
            
            # さらに県の下に細分化された地域のリストを作成
            subregion_controls = []

            # 子地域のリストアイテムを作成
            # 子地域コード（例えば '011000', '012000' など）に対応する天気情報を取得
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
            subregion_controls.append(
                ft.ListTile(
                    title=ft.Text(child_region_name),
                    subtitle=ft.Text(f"天気予報: {weather_info}"),
                    on_click=lambda e, region_id=child_id, region_name=child_region_name: show_weather_details(region_id, region_name, weather_details)
                )
            )

            # 県ごとのExpansionTileに子地域を追加
            prefecture_controls.append(
                ft.ExpansionTile(
                    title=ft.Text(child_region_name),  # 県名をタイトルとして表示
                    subtitle=ft.Text("地域を表示"),
                    affinity=ft.TileAffinity.PLATFORM,
                    maintain_state=True,
                    collapsed_text_color=ft.colors.RED,
                    text_color=ft.colors.RED,
                    controls=subregion_controls,  # 子地域（細分化された地域）のリストを追加
                )
            )

        # 親地域をさらにExpansionTileとして表示し、その中に県ごとのExpansionTileを追加
        controls.append(
            ft.Container(
                content=ft.ExpansionTile(
                    title=ft.Text(parent_region_name),  # 親地域名をタイトルとして表示
                    subtitle=ft.Text("県と地域を表示"),
                    affinity=ft.TileAffinity.PLATFORM,
                    maintain_state=True,
                    collapsed_text_color=ft.colors.RED,
                    text_color=ft.colors.RED,
                    controls=prefecture_controls,  # 県ごとのリストを追加
                ),
                width=200,  # 幅を200pxに設定（短く）
                alignment=ft.alignment.top_left,  # 左寄せに配置
            )
        )

    # `Row` レイアウトで左半分にコンテンツを表示、右半分に詳細情報を表示する
    page.add(
        ft.Row(
            controls=[
                ft.Column(
                    controls=controls,  # 左側にExpansionTileを追加したリスト
                    expand=True,  # 左側を拡張してスペースを取る
                    scroll=True  # 左側にスクロールを有効化
                ),
                ft.Container(
                    width=600,  # 右側に空白スペースを作る
                    bgcolor=ft.colors.WHITE,  # 白い背景を設定
                    content=weather_details  # 右側に天気予報の詳細を表示
                )
            ],
            expand=True  # 全体的に広げる
        )
    )

def show_weather_details(region_id, region_name, weather_details):
    """クリックされた子地域の天気予報を右側に表示"""
    # 天気予報データを取得
    weather_data = get_weather_data(region_id)

    # 天気情報を確認
    if weather_data:
        # ここに表示する情報を整理
        time_series = weather_data[0].get('timeSeries', [])
        
        # 1番目のtimeSeriesを取り出し、詳細を整理
        time_defines = time_series[0].get("timeDefines", [])
        areas = time_series[0].get("areas", [])
        
        detailed_info = []
        for i, area in enumerate(areas):
            area_name = area["area"]["name"]
            weather_code = area.get("weatherCodes", ["情報なし"])[i]  # 天気コード
            weather = area.get("weathers", ["情報なし"])[i]  # 天気
            wind = area.get("winds", ["情報なし"])[i]  # 風
            waves = area.get("waves", ["情報なし"])[i]  # 波
            
            # 日付ごとの天気情報を追加
            detailed_info.append(f"日時: {time_defines[i]}")
            detailed_info.append(f"地域: {area_name}")
            detailed_info.append(f"天気: {weather}")
            detailed_info.append(f"風: {wind}")
            detailed_info.append(f"波: {waves}")
            detailed_info.append("-" * 30)

        # 詳細な天気情報を右側のテキストに表示
        weather_details.value = "\n".join(detailed_info)
    else:
        weather_details.value = "天気情報が取得できませんでした。"
    
    weather_details.update()

# Fletアプリケーションを実行
ft.app(main)
