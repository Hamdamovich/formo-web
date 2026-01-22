import flet as ft
import time
from .settings_config import ThemeManager

def get_home_menu(page: ft.Page, main_color: str):
    # Mavzu boshqaruvchisini yuklaymiz
    tm = ThemeManager(page)
    
    # Dinamik ranglarni aniqlaymiz
    card_bg = tm.get_card_color()
    text_color = tm.get_text_color()
    border_color = "#3D4043" if page.theme_mode == ft.ThemeMode.DARK else "#EEEEEE"
    hover_color = "#343739" if page.theme_mode == ft.ThemeMode.DARK else "#F5F5F5"

    def service_card(icon, label_key, on_click_action=None):
        """Xatosiz ishlaydigan Hover va Press effectli universal kartochka"""
        
        # Lug'atdan so'zni olish
        display_label = tm.get_word(label_key)

        # Hover effekti
        def on_hover(e):
            if e.data == "true":
                e.control.bgcolor = hover_color
                e.control.scale = 1.05
                e.control.border = ft.border.all(1, main_color)
            else:
                e.control.bgcolor = card_bg
                e.control.scale = 1.0
                e.control.border = ft.border.all(1, border_color)
            e.control.update()

        # Press effect simulyatsiyasi
        def handle_click(e):
            e.control.scale = 0.95
            e.control.update()
            
            if on_click_action:
                # Kichik kechikish effektni vizual ko'rish uchun
                time.sleep(0.1) 
                on_click_action(e)

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Icon(icon, color=main_color, size=26),
                        alignment=ft.alignment.center,
                    ),
                    ft.Text(
                        display_label, 
                        size=10, 
                        weight="w500", 
                        text_align=ft.TextAlign.CENTER, 
                        color=text_color, # Dinamik matn rangi
                        max_lines=2,
                        overflow=ft.TextOverflow.ELLIPSIS
                    ),
                ], 
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5
            ),
            bgcolor=card_bg, # Dinamik kartochka foni
            border_radius=15,
            padding=10,
            border=ft.border.all(1, border_color), # Dinamik chegara
            alignment=ft.alignment.center,
            
            # Hodisalar
            on_click=handle_click,
            on_hover=on_hover,
            
            # Animatsiyalar
            # animate=ft.Animation(200, "decelerate"), # Container animatsiyasi
            animate_scale=ft.Animation(200, "decelerate"),
            
            # Dinamik soya
            shadow=tm.get_box_shadow(),
        )

    # Xizmatlar Grid-i
    return ft.GridView(
        expand=True,
        runs_count=3,
        max_extent=130, 
        child_aspect_ratio=1.0,
        spacing=12, 
        run_spacing=12,
        padding=ft.padding.all(10), 
        controls=[
            # 1. To'lovlar tarixi
            service_card(ft.Icons.HISTORY, "menu_history", lambda _: page.go("/payments_history")),
            
            # 2. To'lov grafigi
            service_card(ft.Icons.CALENDAR_MONTH, "menu_schedule", lambda _: page.go("/schedule")),
            
            # 3. Shartnomalar
            service_card(ft.Icons.DESCRIPTION_OUTLINED, "menu_contract", lambda _: page.go("/contracts")),
            
            # 4. Shaxmatka (Joylashuv)
            service_card(
                ft.Icons.LOCATION_ON_OUTLINED, 
                "menu_location", 
                lambda _: page.go("/chessboard")
            ),
            
            # 5. Aloqa (Call Center) - Yangilangan qism
            service_card(
                ft.Icons.CONTACT_SUPPORT_OUTLINED, 
                "menu_contact", 
                lambda _: page.go("/call_center")
            ),
            
            # 6. Sozlamalar
            service_card(
                ft.Icons.SETTINGS_OUTLINED, 
                "menu_settings", 
                lambda _: page.go("/settings")
            ),
        ]
    )