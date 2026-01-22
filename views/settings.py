import flet as ft
from .settings_config import ThemeManager
from .home_down import get_home_down  # Navigatsiya paneli modulini chaqiramiz

class SettingsView(ft.Container):
    """
    Ilova sozlamalari oynasi. 
    Mavzu, til va yorqinlikni boshqarish uchun.
    Pastki qismida home_down navigatsiya paneli bilan integratsiya qilingan.
    """
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.tm = ThemeManager(self.page)
        
        self.expand = True
        self.bgcolor = self.tm.get_bg_color()

        # Saqlangan tilni storage-dan olamiz
        self.current_lang = self.page.client_storage.get("lang") or "O'zbekcha"

        # UI interfeysini qurish
        self.content = self.build_ui()

    def change_theme(self, e):
        """Mavzuni almashtirish va saqlash"""
        is_dark = e.control.value
        self.page.theme_mode = ft.ThemeMode.DARK if is_dark else ft.ThemeMode.LIGHT
        self.page.client_storage.set("theme_mode", "dark" if is_dark else "light")
        
        # UI-ni yangilash
        self.bgcolor = self.tm.get_bg_color()
        self.content = self.build_ui()
        self.update()
        self.page.update()

    def change_language(self, e):
        """Tilni almashtirish va UI-ni qayta chizish"""
        new_lang = "O'zbekcha" if e.control.value else "Русский язык"
        self.page.client_storage.set("lang", new_lang)
        self.current_lang = new_lang
        
        # ThemeManager-dan yangi tildagi xabarnomani olish
        toast_text = self.tm.get_word("toast")
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(f"{toast_text}: {new_lang}"),
            action="OK"
        )
        self.page.snack_bar.open = True
        
        # UI-ni yangi til bilan qayta qurish
        self.content = self.build_ui()
        self.update()
        self.page.update()

    def change_brightness(self, e):
        """Yorqinlikni saqlash"""
        val = e.control.value
        self.page.client_storage.set("brightness_level", val)
        self.page.update()

    def build_ui(self):
        # Ranglarni va matnlarni olish
        text_color = self.tm.get_text_color()
        card_bg = self.tm.get_card_color()
        main_cyan = self.tm.get_main_color()

        # 1. SARLAVHA (Header)
        header = ft.Container(
            content=ft.Row([
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                    icon_color=text_color,
                    icon_size=20,
                    on_click=lambda _: self.page.go("/home"),
                ),
                ft.Text(
                    self.tm.get_word("title"), 
                    size=20, 
                    weight="bold", 
                    color=text_color
                ),
            ], alignment=ft.MainAxisAlignment.START),
            padding=ft.padding.only(left=10, top=10, bottom=10)
        )

        # Kartochka yaratish yordamchi funksiyasi
        def settings_card(title, subtitle, control, icon):
            return ft.Container(
                content=ft.ListTile(
                    leading=ft.Icon(icon, color=main_cyan),
                    title=ft.Text(title, weight="w500", color=text_color, size=14),
                    subtitle=ft.Text(subtitle, size=11, color="grey"),
                    trailing=control,
                    toggle_inputs=True,
                ),
                bgcolor=card_bg,
                border_radius=15,
                margin=ft.margin.only(bottom=10),
            )

        # Control elementlar
        lang_switch = ft.Switch(
            value=True if self.current_lang == "O'zbekcha" else False,
            active_color=main_cyan,
            on_change=self.change_language,
            scale=0.85 
        )

        theme_switch = ft.Switch(
            value=self.page.theme_mode == ft.ThemeMode.DARK,
            active_color=main_cyan,
            on_change=self.change_theme,
            scale=0.85
        )

        saved_bright = self.page.client_storage.get("brightness_level") or 0.8
        brightness_slider = ft.Slider(
            min=0, max=1, value=saved_bright,
            active_color=main_cyan,
            on_change=self.change_brightness,
            width=120
        )

        # 2. SOZLAMALAR RO'YXATI (Skroll bo'ladigan asosiy qism)
        settings_content = ft.Column([
            settings_card(
                self.tm.get_word("lang_label"), 
                f"{self.tm.get_word('current')}: {self.current_lang}", 
                lang_switch, 
                ft.Icons.LANGUAGE
            ),
            settings_card(
                self.tm.get_word("theme_label"), 
                self.tm.get_word("theme_sub"), 
                theme_switch, 
                ft.Icons.DARK_MODE
            ),
            settings_card(
                self.tm.get_word("bright_label"), 
                self.tm.get_word("bright_sub"), 
                brightness_slider, 
                ft.Icons.BRIGHTNESS_6
            ),
            ft.Container(height=30),
            # Brending / Versiya
            ft.Container(
                content=ft.Column([
                    ft.Text("Formo Mobile", size=13, weight="bold", color="grey"),
                    ft.Text(
                        f"{self.tm.get_word('version')}: 1.0.2", 
                        size=11, 
                        color="grey"
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.alignment.center
            ),
            ft.Container(height=20), # Pastki qismda bo'sh joy
        ], scroll=ft.ScrollMode.ADAPTIVE, expand=True)

        # 3. NAVIGATSIYA PANELI (Home_down)
        bottom_nav = get_home_down(
            self.page, 
            self.tm, 
            main_cyan, 
            card_bg, 
            active_route="/settings"
        )

        # ASOSIY TUZILMA
        return ft.Column(
            controls=[
                header,
                ft.Container(
                    content=settings_content,
                    padding=ft.padding.symmetric(horizontal=20),
                    expand=True # Skroll qismi o'rtadagi hamma joyni egallaydi
                ),
                bottom_nav # Bu doim eng pastda turadi
            ],
            spacing=0,
            expand=True
        )