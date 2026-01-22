import flet as ft
from views.login import login_view
from views.home import home_view
from views.payments_history import payments_history_view
from views.schedules import schedules_view
from views.contracts import contracts_view
from views.chessboard import ChessboardView  # Shaxmatka moduli
from views.settings import SettingsView      # Sozlamalar moduli
from views.notifications import NotificationsView # Bildirishnomalar moduli
from views.client_card import client_card_view # Profil (Mijoz kartasi) moduli
from views.client_qr import ClientQRView     # QR kod moduli
from views.call_center import CallCenterView  # Yangi Aloqa moduli

async def main(page: ft.Page):
    # --- 1. SAHIFA ASOSIY SOZLAMALARI ---
    page.title = "Formo Mobile"
    page.window_icon = "assets/icon.png" 
    
    # Webda qora ekranni oldini olish uchun yuklanishni kutamiz
    page.padding = 0
    
    # Mavzuni xavfsiz yuklash
    try:
        saved_theme = await page.client_storage.get_async("theme_mode")
        page.theme_mode = ft.ThemeMode.DARK if saved_theme == "dark" else ft.ThemeMode.LIGHT
    except:
        page.theme_mode = ft.ThemeMode.LIGHT
    
    # Shriftlar
    page.fonts = {
        "Poppins": "https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-Regular.ttf",
        "Poppins-Bold": "https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-Bold.ttf",
        "Poppins-Medium": "https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-Medium.ttf",
    }
    page.theme = ft.Theme(font_family="Poppins")

    # --- 2. YO'NALISHLAR (ROUTING) MANTIQI ---
    def route_change(route_event):
        try:
            # Joriy mavzuga qarab ranglarni belgilash
            current_bg = "#F8F9FE" if page.theme_mode == ft.ThemeMode.LIGHT else "#1A1C1E"
            card_bg = "white" if page.theme_mode == ft.ThemeMode.LIGHT else "#2D3033"
            
            page.views.clear()
            
            # --- ROUTE TEKSHIRUVI ---
            # Webda route "/" yoki bo'sh bo'lishi mumkin
            if page.route == "/" or page.route == "" or page.route is None:
                page.views.append(
                    ft.View("/", controls=[ft.SafeArea(login_view(page), expand=True)], padding=0, bgcolor=current_bg)
                )
            
            # --- ASOSIY SAHIFA ---
            elif page.route == "/home":
                page.views.append(
                    ft.View("/home", controls=[ft.SafeArea(home_view(page), expand=True)], padding=0, bgcolor=current_bg)
                )

            # --- MIJOZ PROFILI ---
            elif page.route in ["/client_card", "/profile"]:
                user_data = {
                    "full_name": page.session.get("user_full_name"),
                    "article_code": page.session.get("article_code"),
                    "phone_number": page.session.get("phone_number"),
                    "birth_date": page.session.get("birth_date"),
                    "passport_info": page.session.get("passport_info"),
                    "address": page.session.get("address"),
                    "floor": page.session.get("floor"),
                    "apartment_number": page.session.get("apartment_number"),
                    "contract_number": page.session.get("contract_number"),
                    "month_payments": page.session.get("month_payments"),
                    "contracts_link": page.session.get("contracts_link"),
                    "schedules_link": page.session.get("schedules_link"),
                }
                page.views.append(
                    ft.View(page.route, controls=[ft.SafeArea(client_card_view(page, user_data), expand=True)], padding=0, bgcolor=current_bg)
                )

            # --- BILDIRISHNOMALAR ---
            elif page.route == "/notifications":
                page.views.append(NotificationsView(page))

            # --- TO'LOVLAR TARIXI ---
            elif page.route in ["/payments_history", "/history"]:
                page.views.append(
                    ft.View(page.route, controls=[ft.SafeArea(payments_history_view(page), expand=True)], padding=0, bgcolor=card_bg)
                )

            # --- TO'LOV GRAFIGI ---
            elif page.route == "/schedule":
                page.views.append(
                    ft.View("/schedule", controls=[ft.SafeArea(schedules_view(page), expand=True)], padding=0, bgcolor=card_bg)
                )

            # --- SHARTNOMALAR ---
            elif page.route == "/contracts":
                page.views.append(
                    ft.View("/contracts", controls=[ft.SafeArea(contracts_view(page), expand=True)], padding=0, bgcolor="#E2E8F0" if page.theme_mode == ft.ThemeMode.LIGHT else "#1A1C1E")
                )

            # --- CHESSBOARD ---
            elif page.route == "/chessboard":
                real_client_data = {
                    "name": page.session.get("user_full_name") or "Mijoz",
                    "apartment_number": page.session.get("apartment_number") or "0/0"
                }
                page.views.append(
                    ft.View("/chessboard", controls=[ft.SafeArea(ChessboardView(page=page, client_data=real_client_data), expand=True)], padding=0, bgcolor="#F5F7F9" if page.theme_mode == ft.ThemeMode.LIGHT else "#1A1C1E")
                )

            # --- SOZLAMALAR ---
            elif page.route == "/settings":
                page.views.append(
                    ft.View("/settings", controls=[ft.SafeArea(SettingsView(page), expand=True)], padding=0, bgcolor=current_bg)
                )

            # --- MIJOZ QR KODI ---
            elif page.route == "/client_qr":
                qr_user_data = {
                    "full_name": page.session.get("user_full_name") or "Mijoz",
                    "article_code": page.session.get("article_code") or "-",
                    "phone_number": page.session.get("phone_number") or "-",
                    "contract_number": page.session.get("contract_number") or "-",
                    "apartment_number": page.session.get("apartment_number") or "-"
                }
                page.views.append(
                    ft.View("/client_qr", controls=[ft.SafeArea(ClientQRView(page, qr_user_data), expand=True)], padding=0, bgcolor=current_bg)
                )

            # --- ALOQA ---
            elif page.route == "/call_center":
                page.views.append(
                    ft.View("/call_center", controls=[ft.SafeArea(CallCenterView(page), expand=True)], padding=0, bgcolor=current_bg)
                )
            
            page.update()
            
        except Exception as e:
            print(f"Routing Error: {e}")
            # Xato bo'lsa login sahifasiga qaytarish
            page.go("/") 

    # --- 3. NAVIGATION MANTIQI ---
    def view_pop(view):
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    # Web uchun boshlang'ich yo'nalishni aniqlash
    # GitHub Pagesda /formo-web/ dan keyingi qismni o'qiydi
    initial_route = page.route if page.route else "/"
    page.go(initial_route)

if __name__ == "__main__":
    # Webda assets papkasini to'g'ri ko'rsatish
    ft.app(target=main, assets_dir="assets", view=ft.AppView.WEB_BROWSER)
