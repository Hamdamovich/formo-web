import flet as ft
from .settings_config import ThemeManager
from .home_down import get_home_down  # Navigatsiya modulini import qilamiz

def client_card_view(page: ft.Page, client_data: dict):
    tm = ThemeManager(page)
    
    # --- 1. RANG VA MAVZU SOZLAMALARI ---
    MAIN_COLOR = tm.get_main_color()
    BG_COLOR = tm.get_bg_color()
    TEXT_COLOR = tm.get_text_color()
    CARD_BG = tm.get_card_color()
    SEC_TEXT = tm.get_secondary_text_color()

    # --- 2. YORDAMCHI FUNKSIYALAR ---
    
    def g(key):
        val = client_data.get(key)
        return str(val) if val not in [None, "None", "", "null"] else "-"

    def format_money(amount):
        try:
            if amount in [None, "-", "None", ""]:
                return "0"
            clean_amount = float(str(amount).replace(",", "").replace(" ", ""))
            return "{:,.0f}".format(clean_amount).replace(",", " ")
        except Exception:
            return str(amount)

    def info_tile(label_text, value, icon):
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(icon, color=MAIN_COLOR, size=20),
                    bgcolor=ft.Colors.with_opacity(0.1, MAIN_COLOR),
                    padding=10,
                    border_radius=10
                ),
                ft.Column([
                    ft.Text(label_text, size=11, color=SEC_TEXT),
                    ft.Text(value, size=14, weight="w500", color=TEXT_COLOR, selectable=True),
                ], spacing=1, expand=True)
            ]),
            margin=ft.margin.only(bottom=15)
        )

    # --- 3. INTERFEYS ELEMENTLARI ---

    # Header
    header = ft.Row([
        ft.IconButton(
            icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
            icon_color=TEXT_COLOR,
            on_click=lambda _: page.go("/home")
        ),
        ft.Text(tm.get_word("profile_tab") or "Profil", size=18, weight="bold", color=TEXT_COLOR),
        ft.Container(width=40)
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    # Profil Asosiy qismi
    profile_header = ft.Container(
        content=ft.Column([
            ft.CircleAvatar(
                content=ft.Icon(ft.Icons.PERSON, size=40, color=MAIN_COLOR),
                bgcolor=ft.Colors.with_opacity(0.1, MAIN_COLOR),
                radius=45
            ),
            ft.Text(g("full_name"), size=20, weight="bold", color=TEXT_COLOR, text_align="center"),
            ft.Text(f"ID: {g('article_code')}", size=14, color=SEC_TEXT),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=20
    )

    # Ma'lumotlar ro'yxati (Scrollable qism)
    details_list_content = ft.Column([
        info_tile("Telefon raqami", g("phone_number"), ft.Icons.PHONE_ANDROID_ROUNDED),
        info_tile("Pasport ma'lumotlari", g("passport_info"), ft.Icons.FINGERPRINT_ROUNDED),
        info_tile("Tug'ilgan sana", g("birth_date"), ft.Icons.CAKE_ROUNDED),
        info_tile("Yashash manzili", g("address"), ft.Icons.HOME_ROUNDED),
        ft.Divider(height=20, color=ft.Colors.with_opacity(0.1, SEC_TEXT)),
        info_tile("Sotib olingan xonadon", f"{g('floor')}-qavat, {g('apartment_number')}-xonadon", ft.Icons.APARTMENT_ROUNDED),
        info_tile("Shartnoma raqami", g("contract_number"), ft.Icons.ASSIGNMENT_ROUNDED),
        info_tile("Oylik to'lov miqdori", f"{format_money(client_data.get('month_payments'))} so'm", ft.Icons.PAYMENTS_ROUNDED),
    ], scroll=ft.ScrollMode.ADAPTIVE)

    # Tugmalar (PDF/Grafik)
    links_row = ft.Row([
        ft.ElevatedButton(
            text="Shartnoma",
            icon=ft.Icons.PICTURE_AS_PDF_ROUNDED,
            on_click=lambda _: page.launch_url(client_data.get("contracts_link")) if client_data.get("contracts_link") else None,
            visible=bool(client_data.get("contracts_link")),
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
        ),
        ft.ElevatedButton(
            text="Grafik",
            icon=ft.Icons.CALENDAR_MONTH_ROUNDED,
            on_click=lambda _: page.launch_url(client_data.get("schedules_link")) if client_data.get("schedules_link") else None,
            visible=bool(client_data.get("schedules_link")),
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
        )
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)

    # --- 4. NAVIGATSIYA PANELINI CHAQIRISH ---
    # active_route ushbu sahifa yo'liga moslangan (Odamcha ikonkasi yonadi)
    bottom_nav = get_home_down(page, tm, MAIN_COLOR, CARD_BG, active_route="/client_card")

    # --- 5. YAKUNIY KONTEYNER ---
    return ft.Container(
        expand=True,
        bgcolor=BG_COLOR,
        content=ft.Column([
            # Yuqori Header va Profil qismi
            ft.Container(
                content=ft.Column([
                    ft.Container(content=header, padding=ft.padding.only(top=10, left=10, right=10)),
                    profile_header,
                ], spacing=0)
            ),
            
            # O'rtadagi asosiy ma'lumotlar qismi (Pastga qarab suriladi)
            ft.Container(
                expand=True,
                content=ft.Column([
                    ft.Text("Mijoz ma'lumotlari", size=16, weight="bold", color=TEXT_COLOR),
                    ft.Container(height=10),
                    ft.Container(content=details_list_content, expand=True),
                    ft.Container(content=links_row, padding=ft.padding.only(top=10, bottom=10))
                ]),
                padding=ft.padding.only(left=30, right=30, top=30, bottom=0),
                bgcolor=CARD_BG,
                border_radius=ft.border_radius.only(top_left=35, top_right=35),
            ),
            
            # Pastki Navigatsiya (Doim joyida turadi)
            bottom_nav
        ], spacing=0)
    )