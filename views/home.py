import flet as ft
from .settings_config import ThemeManager
from .home_up import get_home_up 
from .home_debt import get_home_debt
from .home_menu import get_home_menu
from .home_down import get_home_down  # Navbatdagi yangilangan modul

def home_view(page: ft.Page):
    # 1. ThemeManager orqali sozlamalarni yuklaymiz
    tm = ThemeManager(page)
    
    # 2. Dinamik ranglarni lug'atdan yoki sozlamalardan olamiz
    MAIN_COLOR = tm.get_main_color()
    BG_COLOR = tm.get_bg_color()
    TEXT_COLOR = tm.get_text_color()
    CARD_BG = tm.get_card_color()

    # --- UI KOMPONENTLARINI CHAQIRISH ---

    # Header qismi (Profil rasmi, ism, bildirishnomalar)
    header = get_home_up(page, MAIN_COLOR)

    # Balans/Qarz kartochkasi (Summa ko'rsatilgan qism)
    balance_card = get_home_debt(page)

    # Xizmatlar menyusi (Grid ko'rinishidagi ikonkalik tugmalar)
    services_grid = get_home_menu(page, MAIN_COLOR)
    
    # Pastki navigatsiya bari (Alohida modulga chiqarilgan qism)
    bottom_nav = get_home_down(page, tm, MAIN_COLOR, CARD_BG, active_route="/home")

    # --- ASOSIY SAHIFA MONTAJI ---
    return ft.Container(
        expand=True,
        bgcolor=BG_COLOR, # Sahifa foni (Light/Dark mode)
        content=ft.Column(
            controls=[
                # Yuqori qism: Header va Balans kartochkasi guruhi
                ft.Container(
                    content=ft.Column(
                        controls=[
                            header, 
                            ft.Container(height=10), # Elementlar orasidagi masofa
                            balance_card 
                        ]
                    ), 
                    padding=ft.padding.only(left=20, right=20, top=10, bottom=10)
                ),
                
                # O'rtadagi Dinamik xizmatlar paneli
                ft.Container(
                    expand=True,
                    content=ft.Column(
                        controls=[
                            # "Xizmatlar" va "Hammasi" yozuvlari qatori
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        tm.get_word("services_title"), # Lug'atdan: "Xizmatlar"
                                        size=18, 
                                        weight="bold", 
                                        color=TEXT_COLOR
                                    ),
                                    ft.TextButton(
                                        content=ft.Text(
                                            tm.get_word("all_btn"), # Lug'atdan: "Hammasi"
                                            color=MAIN_COLOR, 
                                            size=13
                                        ),
                                        on_click=lambda _: print("Barcha xizmatlar sahifasiga o'tish")
                                    )
                                ], 
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                            ft.Container(height=5),
                            
                            # Xizmatlar Grid paneli
                            services_grid, 
                        ]
                    ),
                    # Dizayn: Panelning chetlaridan masofa va burchaklarni qayirish
                    padding=ft.padding.only(left=25, right=25, top=25, bottom=0),
                    bgcolor=CARD_BG, # Paneldagi karta foni
                    border_radius=ft.border_radius.only(top_left=35, top_right=35)
                ),
                
                # Eng pastki qism: Navigatsiya tugmalari
                bottom_nav
            ], 
            spacing=0 # Elementlar orasida ortiqcha masofa qolmasligi uchun
        )
    )