import sqlite3
import requests
import flet as ft

# SQLiteのDBファイル
db_filename = 'weather_forecast.db'

# APIから地域データを取得
area_json = requests.get("http://www.jma.go.jp/bosai/common/const/area.json").json()

def get_weather_data(region_code: str):
    """指定された地域コードに対して天気予報を取得する"""
    weather_url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{region_code}.json"
    response = requests.get(weather_url)
    
    if response.status_code != 200:
        print(f"Weather data for {region_code} not found!")
        return {}
    
    return response.json()

def save_weather_to_db(region_id, weather_data):
    """天気データをSQLiteデータベースに保存する"""
    con = sqlite3.connect(db_filename)
    cur = con.cursor()
    
    # テーブル作成（なければ作成）
    cur.execute("""
    CREATE TABLE IF NOT EXISTS weather_forecast (
        region_id TEXT,
        area_name TEXT,
        date TEXT,
        weather TEXT,
        wind TEXT,
        wave TEXT,
        UNIQUE(region_id, area_name, date)  -- 重複防止のためユニーク制約を追加
    )
    """)
    
    # 時間軸のデータを取り出して保存
    time_series = weather_data[0].get('timeSeries', [])
    if time_series:
        time_defines = time_series[0].get("timeDefines", [])
        areas = time_series[0].get("areas", [])
        
        for area in areas:
            area_name = area["area"]["name"]
            weather_codes = area.get("weatherCodes", ["情報なし"])
            weathers = area.get("weathers", ["情報なし"])
            winds = area.get("winds", ["情報なし"])
            waves = area.get("waves", ["情報なし"])
            
            for i in range(len(time_defines)):
                weather = weathers[i] if i < len(weathers) else "情報なし"
                wind = winds[i] if i < len(winds) else "情報なし"
                wave = waves[i] if i < len(waves) else "情報なし"
                date = time_defines[i] if i < len(time_defines) else "情報なし"
                
                # 重複がないか確認
                cur.execute("""
                SELECT COUNT(*) FROM weather_forecast WHERE region_id = ? AND area_name = ? AND date = ?
                """, (region_id, area_name, date))
                if cur.fetchone()[0] == 0:  # まだデータがなければ
                    # DBに挿入
                    cur.execute("""
                    INSERT INTO weather_forecast (region_id, area_name, date, weather, wind, wave)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """, (region_id, area_name, date, weather, wind, wave))
    
    con.commit()
    con.close()

def drop_weather_table():
    """アプリケーション終了時にテーブルを削除"""
    con = sqlite3.connect(db_filename)
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS weather_forecast")
    con.commit()
    con.close()

def search_weather(region_name: str, weather_details):
    """検索された地域名に基づいて天気予報を表示"""
    con = sqlite3.connect(db_filename)
    cur = con.cursor()

    cur.execute("""
    SELECT DISTINCT * FROM weather_forecast WHERE area_name LIKE ?
    """, ('%' + region_name + '%',))  # 入力された地域名を前後に%を付けて部分一致検索
    rows = cur.fetchall()

    detailed_info = []
    if rows:
        for row in rows:
            detailed_info.append(f"地域: {row[1]}")
            detailed_info.append(f"日時: {row[2]}")
            detailed_info.append(f"天気: {row[3]}")
            detailed_info.append(f"風: {row[4]}")
            detailed_info.append(f"波: {row[5]}")
            detailed_info.append("-" * 30)
    else:
        detailed_info.append("天気情報が見つかりません。")

    weather_details.controls = [ft.Container(
        content=ft.Column([ft.Text(info) for info in detailed_info]),
        bgcolor=ft.colors.BLACK, 
        padding=10  
    )]
    weather_details.update()

def main(page: ft.Page):
    # メニューバーを追加
    page.add(
        ft.AppBar(
            title=ft.Text("天気予報", color=ft.colors.WHITE),
            actions=[
                ft.IconButton(ft.icons.SETTINGS, on_click=lambda e: print("Settings clicked"))
            ],
            bgcolor=ft.colors.BLUE,  
        )
    )

    weather_details = ft.ListView(  
        spacing=10,  
        width=600,  
        height=500,  
    )

    controls = []

    # 各地域の情報を展開して表示
    for region_id, region_info in area_json["centers"].items():
        parent_region_name = region_info["name"]
        
        prefecture_controls = []

        for child_id in region_info["children"]:
            child_region_name = area_json["offices"].get(child_id, {}).get("name", f"Unknown Region {child_id}")
            
            subregion_controls = []

            weather_data = get_weather_data(child_id)

            if weather_data:
                save_weather_to_db(child_id, weather_data)
                weather_info = "情報がありません"
                forecast = weather_data[0].get('timeSeries', [{}])[0].get('areas', [{}])[0].get('weatherCodes', [])
                if forecast:
                    weather_info = forecast[0]  
            else:
                weather_info = "情報がありません"

            subregion_controls.append(
                ft.ListTile(
                    title=ft.Text(child_region_name),
                    subtitle=ft.Text(f"天気予報: {weather_info}"),
                    on_click=lambda e, region_id=child_id, region_name=child_region_name: show_weather_details(region_id, region_name, weather_details)
                )
            )

            prefecture_controls.append(
                ft.Container(
                    bgcolor=ft.colors.GREY,  
                    content=ft.ExpansionTile(
                        title=ft.Text(child_region_name),  
                        subtitle=ft.Text("地域を表示", color=ft.colors.WHITE),  
                        affinity=ft.TileAffinity.PLATFORM,
                        maintain_state=True,
                        collapsed_text_color=ft.colors.WHITE,  
                        text_color=ft.colors.WHITE,  
                        controls=subregion_controls,  
                    )
                )
            )

        controls.append(
            ft.Container(
                bgcolor=ft.colors.GREY,  
                content=ft.ExpansionTile(
                    title=ft.Text(parent_region_name),  
                    subtitle=ft.Text("県と地域を表示",color=ft.colors.WHITE),
                    affinity=ft.TileAffinity.PLATFORM,
                    maintain_state=True,
                    collapsed_text_color=ft.colors.WHITE,  
                    text_color=ft.colors.WHITE,  
                    controls=prefecture_controls,  
                ),
                width=200,  
                alignment=ft.alignment.top_left,  
            )
        )

    page.add(
        ft.Row(
            controls=[
                ft.Column(
                    controls=controls,  
                    expand=True,  
                    scroll=True  
                ),
                ft.Container(
                    width=600,  
                    content=weather_details  
                )
            ],
            expand=True  
        )
    )

    search_field = ft.TextField(
        label="地域名で検索",
        autofocus=True,  
        on_change=lambda e: search_weather(e.control.value, weather_details)  
    )
    page.add(search_field)

    page.on_page_close = lambda _: drop_weather_table()

def show_weather_details(region_id, region_name, weather_details):
    """クリックされた子地域の天気予報を右側に表示"""
    con = sqlite3.connect('weather_forecast.db')
    cur = con.cursor()
    cur.execute("""
    SELECT DISTINCT * FROM weather_forecast WHERE region_id = ? LIMIT 10
    """, (region_id,))
    rows = cur.fetchall()

    detailed_info = []
    if rows:
        for row in rows:
            detailed_info.append(f"地域: {row[1]}")
            detailed_info.append(f"日時: {row[2]}")
            detailed_info.append(f"天気: {row[3]}")
            detailed_info.append(f"風: {row[4]}")
            detailed_info.append(f"波: {row[5]}")
            detailed_info.append("-" * 30)
    else:
        detailed_info.append("天気情報が見つかりません。")

    weather_details.controls = [ft.Container(
        content=ft.Column([ft.Text(info, color=ft.colors.WHITE) for info in detailed_info]),
        bgcolor=ft.colors.BLACK,  
        padding=10  
    )]
    weather_details.update()

# Fletアプリケーションを実行
ft.app(main)
