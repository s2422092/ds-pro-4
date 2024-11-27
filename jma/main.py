import flet as ft



def main(page: ft.Page):
    # 上半分を青色にするためのContainer
    top_half = ft.Container(
        content=ft.Text("天気予報", size=40, color=ft.colors.WHITE),  
        bgcolor=ft.colors.BLUE_500,  # 背景色を青に設定
        height=page.height // 10,  # ページの高さの半分
        alignment=ft.alignment.top_left,  # テキストを中央に配置
    )

    # SafeAreaの中に青色の上半分を配置
    page.add(ft.SafeArea(top_half))
    
    page.add(
        ft.ExpansionTile(
            title=ft.Text("ExpansionTile 1"),
            subtitle=ft.Text("Trailing expansion arrow icon"),
            affinity=ft.TileAffinity.PLATFORM,
            maintain_state=True,
            collapsed_text_color=ft.colors.RED,
            text_color=ft.colors.RED,
            controls=[ft.ListTile(title=ft.Text("This is sub-tile number 1"))],
        ),
    )

    

ft.app(main)
