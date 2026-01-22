import flet as ft
import requests
import threading
import time
from .settings_config import ThemeManager
from .home_down import get_home_down  # Navigatsiya modulini import qilamiz

def get_google_doc_url(url):
    """Google Docs ssilkasini eksport formatiga (txt) o'tkazish"""
    try:
        if "docs.google.com/document/d/" in url:
            doc_id = url.split("/d/")[1].split("/")[0]
            return f"https://docs.google.com/document/d/{doc_id}/export?format=txt"
    except Exception as e:
        print(f"URL formatlashda xato: {e}")
        return None
    return url

def contracts_view(page: ft.Page):
    # ThemeManager modulini ishga tushiramiz
    tm = ThemeManager(page)
    
    # Dinamik ranglar
    bg_color = tm.get_bg_color()
    paper_color = tm.get_card_color() # Qog'oz rangi
    text_color = tm.get_text_color()
    main_color = tm.get_main_color()
    
    # Shartnoma varog'i atrofidagi fon
    outer_bg = "#121416" if page.theme_mode == ft.ThemeMode.DARK else "#E2E8F0"
    header_bg = "#1A1C1E" if page.theme_mode == ft.ThemeMode.DARK else "#F8FAFC"

    # 1. Sessiondan ssilkani olish
    contract_url = page.session.get("contracts_link")
    if not contract_url:
        contract_url = "https://docs.google.com/document/d/1LLTKpAL839HOwxojbcsMilkOviXTzjym/edit"

    # UI Elementlari
    contract_content = ft.Column(spacing=10, scroll=ft.ScrollMode.ADAPTIVE, expand=True)
    
    loading_indicator = ft.ProgressBar(visible=True, color=main_color)
    error_message = ft.Text(color="red", visible=False, size=13, weight="bold")
    
    # Word "Varoq" konteyneri
    paper_document = ft.Container(
        content=contract_content,
        padding=40,
        bgcolor=paper_color,
        border_radius=2,
        expand=True,
        shadow=tm.get_box_shadow(),
        visible=False 
    )

    def fetch_contract_data():
        time.sleep(0.2)
        try:
            download_url = get_google_doc_url(contract_url)
            response = requests.get(download_url, timeout=20)
            
            if response.status_code == 200:
                text_data = response.content.decode("utf-8")
                lines = text_data.split("\n")
                
                contract_content.controls.clear()
                
                for line in lines:
                    clean_line = line.strip()
                    if clean_line:
                        is_header = clean_line.isupper() and len(clean_line) > 3
                        
                        contract_content.controls.append(
                            ft.Text(
                                clean_line,
                                size=16 if is_header else 14,
                                weight="bold" if is_header else "normal",
                                text_align=ft.TextAlign.CENTER if is_header else ft.TextAlign.JUSTIFY,
                                width=float("inf"),
                                color=text_color
                            )
                        )
                
                paper_document.visible = True
                error_message.visible = False
            else:
                error_message.value = f"Xatolik: Server javob bermadi ({response.status_code})"
                error_message.visible = True
                
        except Exception as e:
            error_message.value = f"Internet bilan ulanishda xatolik yuz berdi"
            error_message.visible = True
            
        loading_indicator.visible = False
        page.update()

    # Navigatsiya panelini chaqirish (Shartnoma sahifasi Home tarkibida bo'lgani uchun uychani yoqamiz)
    bottom_nav = get_home_down(page, tm, main_color, paper_color, active_route="/home")

    # Layout tuzilishi
    main_layout = ft.Container(
        expand=True,
        bgcolor=bg_color,
        content=ft.Column(
            expand=True,
            spacing=0,
            controls=[
                # Header
                ft.Container(
                    content=ft.Row([
                        ft.IconButton(
                            ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED, 
                            on_click=lambda _: page.go("/home"),
                            icon_color=text_color
                        ),
                        ft.Text("Shartnomani ko'rish", size=18, weight="bold", color=text_color),
                    ]),
                    padding=10,
                    bgcolor=header_bg
                ),
                
                loading_indicator,
                ft.Container(error_message, padding=ft.padding.symmetric(horizontal=20)),
                
                # Asosiy Varoq maydoni (O'rtadagi skroll bo'ladigan qism)
                ft.Container(
                    expand=True,
                    padding=ft.padding.only(left=20, right=20, bottom=10, top=10),
                    bgcolor=outer_bg,
                    content=paper_document
                ),
                
                # Navigatsiya paneli (Doim pastda)
                bottom_nav
            ]
        )
    )

    # Ma'lumotni yuklashni boshlash
    threading.Thread(target=fetch_contract_data, daemon=True).start()

    return main_layout