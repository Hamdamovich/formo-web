import flet as ft
from .settings_config import ThemeManager
from .home_down import get_home_down

class CallCenterView(ft.Container):
    """
    Aloqa va ijtimoiy tarmoqlar sahifasi.
    """
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.tm = ThemeManager(page)
        self.expand = True
        self.bgcolor = self.tm.get_bg_color()
        self.content = self.build_ui()

    def build_ui(self):
        main_color = self.tm.get_main_color()
        text_color = self.tm.get_text_color()
        card_bg = self.tm.get_card_color()
        sec_text = "grey"

        # 1. HEADER
        header = ft.Container(
            content=ft.Row([
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                    icon_color=text_color,
                    icon_size=20,
                    on_click=lambda _: self.page.go("/home"),
                ),
                ft.Text("Aloqa", size=20, weight="bold", color=text_color),
                ft.Container(width=40)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.only(left=10, right=10, top=10)
        )

        # 2. ALOQA KARTASI FUNKSIYASI
        def contact_item(title, subtitle, icon, link, is_phone=False):
            return ft.Container(
                content=ft.ListTile(
                    leading=ft.Icon(icon, color=main_color, size=28),
                    title=ft.Text(title, size=14, weight="w600", color=text_color),
                    subtitle=ft.Text(subtitle, size=12, color=sec_text),
                    trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT_ROUNDED, color=sec_text),
                    on_click=lambda _: self.page.launch_url(f"tel:{link}" if is_phone else link),
                ),
                bgcolor=card_bg,
                border_radius=15,
                margin=ft.margin.only(bottom=10),
                shadow=self.tm.get_box_shadow()
            )

        # Sarlavhalar uchun xatoliksiz funksiya (Container orqali margin berilgan)
        def section_label(text):
            return ft.Container(
                content=ft.Text(text, size=16, weight="bold", color=main_color),
                margin=ft.margin.only(top=15, bottom=8)
            )

        # 3. ASOSIY RO'YXAT (SCROLLABLE)
        content_list = ft.Column([
            # Instagram bo'limi
            section_label("Instagram"),
            contact_item(
                "Hamdam Binokor (Yorqin kelajak)", 
                "@hamdambinokor", 
                ft.Icons.CAMERA_ALT_OUTLINED, 
                "https://www.instagram.com/hamdambinokor/"
            ),
            contact_item(
                "Hamdam Binokor (Vatan)", 
                "@hamdam_binokor", 
                ft.Icons.CAMERA_ALT_OUTLINED, 
                "https://www.instagram.com/hamdam_binokor/"
            ),

            # Telegram bo'limi
            section_label("Telegram"),
            contact_item(
                "Hamdam Binokor kanali", 
                "Rasmiy kanalimiz", 
                ft.Icons.SEND_ROUNDED, 
                "https://t.me/hamdam_binokor"
            ),

            # Call Center bo'limi
            section_label("Call Center"),
            contact_item(
                "+998 (78) 555-85-00", 
                "Ish vaqti: 09:00 - 18:00", 
                ft.Icons.CALL_ROUNDED, 
                "+998785558500", 
                is_phone=True
            ),
            contact_item(
                "+998 (94) 380-85-00", 
                "Qo'shimcha bog'lanish", 
                ft.Icons.PHONE_ANDROID_ROUNDED, 
                "+998943808500", 
                is_phone=True
            ),
            
            ft.Container(height=30),
            
            # 4. BRENDING (Ikonka matnning boshida)
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.COPYRIGHT_ROUNDED, size=14, color=sec_text),
                    ft.Text("FormoMobile 2026 | HamdamovichSoft", size=11, color=sec_text),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
                alignment=ft.alignment.center
            ),
            ft.Container(height=40),
        ], scroll=ft.ScrollMode.ADAPTIVE, expand=True)

        # 5. NAVIGATSIYA PANELI (HomeDown moduli)
        bottom_nav = get_home_down(
            page=self.page, 
            tm=self.tm, 
            MAIN_COLOR=main_color, 
            CARD_BG=card_bg, 
            active_route="/call_center"
        )

        return ft.Column([
            header,
            ft.Container(
                content=content_list,
                padding=ft.padding.symmetric(horizontal=20),
                expand=True
            ),
            bottom_nav
        ], spacing=0)