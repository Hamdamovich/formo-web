import flet as ft
import requests
import threading
from .settings_config import ThemeManager
from .home_down import get_home_down  # Navigatsiya moduli

def format_money(amount):
    """24836000 -> 24 836 000 formatiga o'tkazish"""
    try:
        if amount is None or amount == "" or amount == 0: return "0"
        return f"{int(float(amount)):,}".replace(",", " ")
    except (ValueError, TypeError):
        return "0"

def payments_history_view(page: ft.Page):
    tm = ThemeManager(page)
    
    # 1. Dinamik ranglar va sozlamalar
    MAIN_COLOR = tm.get_main_color()
    BG_COLOR = tm.get_bg_color()
    CARD_BG = tm.get_card_color()
    TEXT_COLOR = tm.get_text_color()
    SEC_TEXT_COLOR = tm.get_secondary_text_color()
    BORDER_COLOR = "#3D4043" if page.theme_mode == ft.ThemeMode.DARK else "#EEEEEE"
    HEADER_BG = "#1A1C1E" if page.theme_mode == ft.ThemeMode.DARK else "#F8FAFC"

    def get_col_widths():
        w = page.width - 40 
        if page.width < 600:
            return [w*0.1, w*0.25, w*0.2, w*0.2, w*0.25]
        return [w*0.05, w*0.2, w*0.25, w*0.25, w*0.25]

    is_mobile = page.width < 600
    font_size_header = 12 if is_mobile else 14
    font_size_cell = 11 if is_mobile else 13

    client_id = page.session.get("client_id") or 1 
    PAYMENTS_API = f"https://formo-api.onrender.com/payments?client_id={client_id}"

    # UI Elementlari
    loading_indicator = ft.ProgressBar(visible=True, color=MAIN_COLOR)
    error_message = ft.Text(color="red", visible=False, size=12, weight="bold")
    
    # Summary elementlari
    total_contract_text = ft.Text("0", weight="bold", color=MAIN_COLOR, size=13)
    total_paid_text = ft.Text("0", weight="bold", color="green", size=13)
    remaining_debt_text = ft.Text("0", weight="bold", color="red", size=13)

    def create_cell_container(content, align, width_idx):
        return ft.Container(
            content=content,
            alignment=align,
            width=get_col_widths()[width_idx],
            padding=ft.padding.only(left=2, right=2)
        )

    # 2. JADVAL TUZILISHI
    history_table = ft.DataTable(
        border=ft.border.all(1, BORDER_COLOR),
        border_radius=10,
        heading_row_color=tm.get_bg_color() if page.theme_mode == ft.ThemeMode.DARK else "#F3F4F6",
        column_spacing=0,
        horizontal_margin=5,
        heading_row_height=35,
        data_row_min_height=35,
        columns=[
            ft.DataColumn(create_cell_container(ft.Text(tm.get_word("col_no"), weight="bold", size=font_size_header, color=TEXT_COLOR), ft.alignment.center, 0)),
            ft.DataColumn(create_cell_container(ft.Text(tm.get_word("col_date"), weight="bold", size=font_size_header, color=TEXT_COLOR), ft.alignment.center, 1)),
            ft.DataColumn(create_cell_container(ft.Text(tm.get_word("col_type"), weight="bold", size=font_size_header, color=TEXT_COLOR), ft.alignment.center, 2)),
            ft.DataColumn(create_cell_container(ft.Text(tm.get_word("col_pay"), weight="bold", size=font_size_header, color=TEXT_COLOR), ft.alignment.center, 3)),
            ft.DataColumn(create_cell_container(ft.Text(tm.get_word("col_debt"), weight="bold", size=font_size_header, color=TEXT_COLOR), ft.alignment.center, 4)),
        ],
        rows=[],
    )

    # Asosiy kontent konteyneri
    main_content_area = ft.Column(visible=False, scroll=ft.ScrollMode.ADAPTIVE, spacing=5, expand=True)

    # 3. MA'LUMOTNI YUKLASH FUNKSIYASI
    def load_data():
        try:
            response = requests.get(PAYMENTS_API, timeout=30)
            if response.status_code == 200:
                data = response.json()
                data.sort(key=lambda x: x.get('date', ''))
                
                new_rows = []
                sum_paid = 0
                sum_debt = 0

                for index, p in enumerate(data, start=1):
                    raw_amount = p.get('amount', 0) or 0
                    raw_debt = p.get('debt', 0) or 0
                    sum_paid += raw_amount
                    sum_debt += raw_debt
                    
                    raw_date = str(p.get('date', ''))[:10]
                    try:
                        y, m, d = raw_date.split('-')
                        formatted_date = f"{d}.{m}.{y[2:]}" if is_mobile else f"{d}.{m}.{y}"
                    except:
                        formatted_date = raw_date

                    new_rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(create_cell_container(ft.Text(str(index), size=font_size_cell, color=TEXT_COLOR), ft.alignment.center, 0)),
                                ft.DataCell(create_cell_container(ft.Text(formatted_date, size=font_size_cell, color=TEXT_COLOR), ft.alignment.center_left, 1)),
                                ft.DataCell(create_cell_container(ft.Text(str(p.get('payment_type', '')), size=font_size_cell, color=TEXT_COLOR), ft.alignment.center_left, 2)),
                                ft.DataCell(create_cell_container(ft.Text(format_money(raw_amount), color="green", weight="w500", size=font_size_cell), ft.alignment.center_right, 3)),
                                ft.DataCell(create_cell_container(ft.Text(format_money(raw_debt), color="red", weight="w500", size=font_size_cell), ft.alignment.center_right, 4)),
                            ]
                        )
                    )
                
                total_contract_text.value = format_money(sum_debt)
                total_paid_text.value = format_money(sum_paid)
                remaining_debt_text.value = format_money(sum_debt - sum_paid)
                
                history_table.rows = new_rows
                main_content_area.visible = True
                error_message.visible = False
            else:
                error_message.value = f"Server xatosi: {response.status_code}"
                error_message.visible = True
        except Exception as e:
            error_message.value = "Internet ulanish xatosi"
            error_message.visible = True
        finally:
            loading_indicator.visible = False
            page.update()

    # 4. RESPONSIVE
    def on_resize(e):
        try:
            new_widths = get_col_widths()
            for i, col in enumerate(history_table.columns):
                if hasattr(col.label, "width"): col.label.width = new_widths[i]
            for row in history_table.rows:
                for i, cell in enumerate(row.cells):
                    if hasattr(cell.content, "width"): cell.content.width = new_widths[i]
            page.update()
        except: pass

    page.on_resize = on_resize

    # ASOSIY UI ELEMENTLARINI YIG'ISH
    main_content_area.controls = [
        ft.Container(
            content=ft.Column([
                ft.Row([ft.Text(tm.get_word("total_sum"), size=12, color=SEC_TEXT_COLOR), total_contract_text], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([ft.Text(tm.get_word("paid_sum"), size=12, color=SEC_TEXT_COLOR), total_paid_text], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([ft.Text(tm.get_word("remain_sum"), size=12, color=SEC_TEXT_COLOR), remaining_debt_text], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ], spacing=2),
            padding=15, bgcolor=CARD_BG, border_radius=10, border=ft.border.all(1, BORDER_COLOR), shadow=tm.get_box_shadow()
        ),
        ft.Container(height=10),
        ft.Text(tm.get_word("list_title"), size=15, weight="bold", color=TEXT_COLOR),
        ft.Divider(height=1, color=BORDER_COLOR),
        ft.Row([history_table], scroll=ft.ScrollMode.ADAPTIVE, alignment=ft.MainAxisAlignment.START),
        ft.Container(height=10),
        ft.Text(tm.get_word("note"), size=10, italic=True, color=SEC_TEXT_COLOR)
    ]

    # Navigatsiya panelini chaqirish (Tarix/Chart ikonkasi yonadi)
    bottom_nav = get_home_down(page, tm, MAIN_COLOR, CARD_BG, active_route="/payments_history")

    # SAHIFA TUZILISHI (Layout)
    layout = ft.Container(
        expand=True,
        bgcolor=BG_COLOR,
        content=ft.Column(
            expand=True,
            spacing=0,
            controls=[
                # HEADER
                ft.Container(
                    content=ft.Row([
                        ft.IconButton(ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED, on_click=lambda _: page.go("/home"), icon_size=18, icon_color=TEXT_COLOR),
                        ft.Text(tm.get_word("history_title"), size=18, weight="bold", color=TEXT_COLOR),
                    ]),
                    padding=ft.padding.only(left=10, right=10, top=10, bottom=5),
                    bgcolor=HEADER_BG
                ),
                loading_indicator,
                ft.Divider(height=1, color=BORDER_COLOR),
                
                # ERROR MESSAGE
                ft.Container(error_message, padding=ft.padding.symmetric(horizontal=20, vertical=10)),

                # ASOSIY KONTENT (O'rtada skroll bo'ladi)
                ft.Container(
                    expand=True, 
                    padding=ft.padding.only(left=15, right=15, bottom=0, top=10), 
                    content=main_content_area
                ),
                
                # BOTTOM NAVIGATION (Doim pastda qat'iy turadi)
                bottom_nav
            ]
        )
    )

    # Ma'lumotlarni yuklashni boshlash
    threading.Thread(target=load_data, daemon=True).start()

    return layout