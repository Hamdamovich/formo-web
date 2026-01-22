import flet as ft

def get_home_down(page, tm, MAIN_COLOR, CARD_BG, active_route="/home"):
    """
    Pastki navigatsiya paneli moduli.
    active_route: Qaysi sahifa faolligini aniqlash va ranglarni boshqarish uchun.
    """
    
    # 1. QR kod tugmasi bosilganda ochiladigan funksiya
    def open_qr_modal(e):
        # Navigatsiya orqali QR sahifasiga o'tish
        page.go("/client_qr") 

    # 2. Ikonka rangini aniqlash uchun yordamchi funksiya
    def get_icon_color(route):
        # Agar hozirgi yo'nalish (route) aktiv bo'lsa, asosiy rangda bo'ladi
        return MAIN_COLOR if active_route == route else "grey"

    # 3. QR tugmasining fon rangini aniqlash
    # Agar foydalanuvchi QR sahifasida bo'lsa, markaziy tugma ajralib turishi uchun
    qr_bg = MAIN_COLOR if active_route != "/client_qr" else ft.Colors.with_opacity(0.8, MAIN_COLOR)

    return ft.Container(
        content=ft.Row(
            controls=[
                # 1. Uycha ikonkasi - Home sahifasi
                ft.IconButton(
                    icon=ft.Icons.HOME_ROUNDED, 
                    icon_color=get_icon_color("/home"), 
                    icon_size=28,
                    tooltip=tm.get_word("home_tab"),
                    on_click=lambda _: page.go("/home")
                ),
                
                # 2. Odamcha ikonkasi - Client Card (Profil) sahifasi
                ft.IconButton(
                    icon=ft.Icons.PERSON_OUTLINE_ROUNDED, 
                    icon_color=get_icon_color("/client_card"), 
                    icon_size=28,
                    tooltip=tm.get_word("profile_tab"),
                    on_click=lambda _: page.go("/client_card")
                ),
                
                # 3. QR Skaner markaziy tugma - Mijoz uchun QR sahifasini ochadi
                ft.Container(
                    content=ft.Icon(
                        ft.Icons.QR_CODE_SCANNER_ROUNDED, 
                        color="white",
                        size=24
                    ),
                    bgcolor=qr_bg,
                    padding=12,
                    border_radius=15,
                    on_click=open_qr_modal,
                    ink=True, # Bosilganda animatsiya (ripple effect) uchun
                    tooltip="Mijoz QR kodi",
                    # QR sahifasida turganda biroz ko'tarilgan effekt berish uchun
                    shadow=ft.BoxShadow(blur_radius=10, color=MAIN_COLOR) if active_route == "/client_qr" else None
                ),
                
                # 4. Diagramma (Tarix) ikonkasi - Payments History sahifasi
                ft.IconButton(
                    icon=ft.Icons.INSERT_CHART_OUTLINED_ROUNDED, 
                    icon_color=get_icon_color("/payments_history"), 
                    icon_size=28,
                    tooltip=tm.get_word("history_tab"),
                    on_click=lambda _: page.go("/payments_history")
                ),
                
                # 5. Chiqish (Logout) ikonkasi
                ft.IconButton(
                    icon=ft.Icons.LOGOUT_ROUNDED, 
                    icon_color="grey", 
                    icon_size=28, 
                    on_click=lambda _: page.go("/"), 
                    tooltip=tm.get_word("back")
                ),
            ], 
            alignment=ft.MainAxisAlignment.SPACE_AROUND
        ),
        padding=ft.padding.only(bottom=20, top=10, left=10, right=10),
        bgcolor=CARD_BG, 
        border_radius=ft.border_radius.only(top_left=25, top_right=25),
        # ThemeManager-dan kelayotgan soya effekti
        shadow=tm.get_box_shadow()
    )