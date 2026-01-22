import flet as ft
import pandas as pd
import io
import requests
import re
import threading
from .settings_config import ThemeManager
from .home_down import get_home_down  # Navigatsiya modulini import qilamiz

def format_money(amount):
    """Raqamlarni chiroyli pul formatiga o'tkazish"""
    try:
        if pd.isna(amount) or amount == "": return "-"
        if isinstance(amount, (int, float)):
            return f"{int(amount):,}".replace(",", " ")
        return str(amount)
    except:
        return str(amount)

def get_google_download_url(url):
    """Google Sheets silkasini yuklab olish formatiga o'tkazish"""
    if url and "docs.google.com/spreadsheets" in url:
        match = re.search(r"/d/([a-zA-Z0-9-_]+)", url)
        if match:
            file_id = match.group(1)
            return f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=xlsx"
    return url

def schedules_view(page: ft.Page):
    tm = ThemeManager(page)
    
    # 1. Dinamik ranglar
    bg_color = tm.get_bg_color()
    card_bg = tm.get_card_color()
    text_color = tm.get_text_color()
    sec_text = tm.get_secondary_text_color()
    main_color = tm.get_main_color()
    
    border_color = "#3D4043" if page.theme_mode == ft.ThemeMode.DARK else "#E2E8F0"
    header_bg = "#1A1C1E" if page.theme_mode == ft.ThemeMode.DARK else "#F8FAFC"
    blue_accent = "#8AB4F8" if page.theme_mode == ft.ThemeMode.DARK else "blue900"

    excel_url = page.session.get("schedules_link")
    is_mobile = page.width < 600

    # Responsive kengliklar
    def get_col_widths():
        w = page.width - 40
        if page.width < 600:
            return [w*0.10, w*0.25, w*0.32, w*0.33]
        return [w*0.05, w*0.20, w*0.35, w*0.40]

    def create_cell_container(content, align, width_idx):
        return ft.Container(
            content=content,
            alignment=align,
            width=get_col_widths()[width_idx],
            padding=ft.padding.only(left=2, right=2)
        )

    # UI Elementlari
    loading_indicator = ft.ProgressBar(visible=True, color=main_color)
    error_text = ft.Text(color="red", visible=False, weight="bold", size=12)
    
    info_card_content = ft.Column(spacing=1) 
    info_container = ft.Container(
        content=info_card_content,
        padding=15,
        bgcolor=card_bg,
        border_radius=10,
        border=ft.border.all(1, border_color),
        visible=False,
        shadow=tm.get_box_shadow()
    )
    
    font_size_header = 12 if is_mobile else 14
    font_size_cell = 11 if is_mobile else 13

    # Jadval
    schedule_table = ft.DataTable(
        border=ft.border.all(1, border_color),
        border_radius=10,
        heading_row_color=tm.get_bg_color() if page.theme_mode == ft.ThemeMode.DARK else "#F3F4F6",
        column_spacing=0, 
        horizontal_margin=5,
        heading_row_height=35,
        data_row_min_height=35,
        columns=[
            ft.DataColumn(create_cell_container(ft.Text(tm.get_word("col_no"), weight="bold", size=font_size_header, color=text_color), ft.alignment.center, 0)),
            ft.DataColumn(create_cell_container(ft.Text(tm.get_word("col_date"), weight="bold", size=font_size_header, color=text_color), ft.alignment.center, 1)),
            ft.DataColumn(create_cell_container(ft.Text(tm.get_word("col_total_debt"), weight="bold", size=font_size_header, color=text_color), ft.alignment.center, 2)),
            ft.DataColumn(create_cell_container(ft.Text(tm.get_word("col_monthly_pay"), weight="bold", size=font_size_header, color=text_color), ft.alignment.center, 3)),
        ],
        rows=[]
    )

    # Asosiy kontent maydoni
    main_content_area = ft.Column(visible=False, scroll=ft.ScrollMode.ADAPTIVE, spacing=5, expand=True)

    def load_excel_data():
        if not excel_url:
            error_text.value = tm.get_word("error_link_not_found")
            error_text.visible = True
            loading_indicator.visible = False
            page.update()
            return
        
        try:
            download_url = get_google_download_url(excel_url)
            response = requests.get(download_url, timeout=30)
            
            if response.status_code == 200:
                excel_data = io.BytesIO(response.content)
                df = pd.read_excel(excel_data, engine="openpyxl", header=None)

                info_card_content.controls.clear()
                details_map = [
                    ("floor", 2), ("apartment", 3), ("status", 4),
                    ("area", 5), ("period", 6),
                    ("start_percent", 8), ("total_price", 9),
                    ("initial_payment", 10)
                ]

                for word_key, row_idx in details_map:
                    display_label = tm.get_word(word_key)
                    val = df.iloc[row_idx, 3] if not pd.isna(df.iloc[row_idx, 3]) else "-"
                    
                    info_card_content.controls.append(
                        ft.Container(
                            content=ft.Row([
                                ft.Text(f"{display_label}:", size=12, color=sec_text),
                                ft.Text(format_money(val), size=12, weight="bold", color=blue_accent)
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            padding=ft.padding.symmetric(vertical=1)
                        )
                    )

                table_header_row = 14
                new_rows = []
                for i in range(table_header_row + 2, len(df)):
                    row_data = df.iloc[i]
                    if pd.isna(row_data[0]): break
                    
                    sana = row_data[1]
                    sana_str = "-"
                    if not pd.isna(sana):
                        try:
                            if hasattr(sana, 'strftime'):
                                sana_str = sana.strftime('%d.%m.%Y')
                            else:
                                clean_sana = str(sana).split(" ")[0]
                                sana_str = pd.to_datetime(clean_sana).strftime('%d.%m.%Y')
                        except:
                            sana_str = str(sana).split(" ")[0]
                    
                    new_rows.append(ft.DataRow(cells=[
                        ft.DataCell(create_cell_container(ft.Text(str(int(row_data[0])), size=font_size_cell, color=text_color), ft.alignment.center, 0)),
                        ft.DataCell(create_cell_container(ft.Text(sana_str, size=font_size_cell, color=text_color), ft.alignment.center, 1)),
                        ft.DataCell(create_cell_container(ft.Text(format_money(row_data[2]), size=font_size_cell, color=text_color), ft.alignment.center_right, 2)),
                        ft.DataCell(create_cell_container(ft.Text(format_money(row_data[3]), size=font_size_cell, weight="bold", color=text_color), ft.alignment.center_right, 3)),
                    ]))
                
                schedule_table.rows = new_rows
                info_container.visible = True
                main_content_area.visible = True
                error_text.visible = False
            else:
                error_text.value = tm.get_word("error_download_failed")
                error_text.visible = True

        except Exception as e:
            print(f"Excel Error: {e}")
            error_text.value = tm.get_word("error_process_data")
            error_text.visible = True
        
        finally:
            loading_indicator.visible = False
            page.update()

    def on_resize(e):
        try:
            new_widths = get_col_widths()
            for i, col in enumerate(schedule_table.columns):
                col.label.width = new_widths[i]
            for row in schedule_table.rows:
                for i, cell in enumerate(row.cells):
                    cell.content.width = new_widths[i]
            page.update()
        except: pass

    page.on_resize = on_resize

    # Kontentni yig'ish
    main_content_area.controls = [
        info_container, 
        ft.Container(height=10),
        ft.Text(tm.get_word("schedule_list_title"), size=15, weight="bold", color=text_color),
        ft.Divider(height=1, color=border_color),
        ft.Row([schedule_table], scroll=ft.ScrollMode.ADAPTIVE, alignment=ft.MainAxisAlignment.START),
        ft.Container(height=10),
        ft.Text(tm.get_word("schedule_note"), size=10, italic=True, color=sec_text)
    ]

    # Navigatsiya panelini chaqirish (Taqvim ikonkasi yonadi)
    bottom_nav = get_home_down(page, tm, main_color, card_bg, active_route="/schedules")

    # ASOSIY LAYOUT
    layout = ft.Container(
        expand=True,
        bgcolor=bg_color,
        content=ft.Column(
            expand=True,
            spacing=0,
            controls=[
                # HEADER
                ft.Container(
                    content=ft.Row([
                        ft.IconButton(ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED, on_click=lambda _: page.go("/home"), icon_size=18, icon_color=text_color),
                        ft.Text(tm.get_word("schedule_title"), size=18, weight="bold", color=text_color),
                    ]),
                    padding=ft.padding.only(left=10, right=10, top=10, bottom=5),
                    bgcolor=header_bg
                ),
                
                # Progress Bar (Header ostida)
                loading_indicator,
                ft.Divider(height=1, color=border_color),
                
                # Error Message
                ft.Container(error_text, padding=ft.padding.symmetric(horizontal=15, vertical=5)),
                
                # Scrollable Content
                ft.Container(
                    expand=True,
                    padding=ft.padding.only(left=15, right=15, bottom=0, top=10),
                    content=main_content_area
                ),

                # BOTTOM NAVIGATION (Doim pastda)
                bottom_nav
            ]
        )
    )

    # Ma'lumotlarni yuklash
    threading.Thread(target=load_excel_data, daemon=True).start()

    return layout