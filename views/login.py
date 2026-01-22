import flet as ft
import requests
import time
from .settings_config import ThemeManager

def login_view(page: ft.Page):
    # ThemeManager modulini ishga tushiramiz
    tm = ThemeManager(page)
    
    # API manzili (TAVSIYA: Har doim oxirgi ishlaydigan URL'ni tekshiring)
    API_URL = "https://formo-api.onrender.com/clients"
    
    # Dinamik Ranglar
    MAIN_COLOR = tm.get_main_color()
    BG_COLOR = tm.get_bg_color()
    TEXT_COLOR = tm.get_text_color()
    SEC_TEXT = tm.get_secondary_text_color()
    CANCEL_COLOR = "#757575"

    # --- DINAMIK LOGO TANLASH ---
    logo_src = "logo_white.png" if page.theme_mode == ft.ThemeMode.DARK else "logo_black.png"

    # Status UI elementlari
    status_icon = ft.ProgressRing(
        width=25, 
        height=25, 
        stroke_width=3, 
        visible=False,
        color=MAIN_COLOR
    )
    status_text = ft.Text("", size=11, text_align=ft.TextAlign.CENTER)

    # Checkbox (Eslab qolish)
    remember_me = ft.Checkbox(
        label=tm.get_word("remember_me"),
        value=False, 
        fill_color=MAIN_COLOR,
        label_style=ft.TextStyle(size=12, color=SEC_TEXT)
    )

    saved_contract = page.client_storage.get("contract_no")
    if saved_contract:
        remember_me.value = True
    
    def login_click(contract_no, phone):
        input_contract = str(contract_no).strip()
        input_phone = str(phone).strip()

        if not input_contract or not input_phone:
            status_text.value = tm.get_word("fill_fields")
            status_text.color = "orange"
            page.update()
            return

        # Animatsiyani boshlash
        status_container.content = status_icon
        status_icon.visible = True
        status_icon.value = None 
        status_text.value = tm.get_word("checking")
        status_text.color = SEC_TEXT
        login_button.disabled = True
        page.update()

        try:
            # API so'rovi
            response = requests.get(API_URL, timeout=15)
            
            if response.status_code == 200:
                clients = response.json()
                user_found = None
                
                for client in clients:
                    db_contract = str(client.get('contract_number', '')).strip()
                    db_phone = str(client.get('phone_number', '')).strip()
                    
                    if db_contract == input_contract and db_phone == input_phone:
                        user_found = client
                        break
                
                if user_found:
                    # --- MA'LUMOTLARNI SAQLASH (TO'LIQ YANGILANGAN QISM) ---
                    # 1. Shaxsiy ma'lumotlar
                    page.session.set("client_id", user_found.get('id'))
                    page.session.set("article_code", user_found.get('article_code'))
                    page.session.set("user_full_name", user_found.get('full_name', 'Mijoz'))
                    page.session.set("phone_number", user_found.get('phone_number'))
                    page.session.set("passport_info", user_found.get('passport_info'))
                    page.session.set("birth_date", user_found.get('birth_date'))
                    
                    # 2. Yashash manzili ma'lumotlari
                    page.session.set("address", user_found.get('address'))
                    page.session.set("floor", user_found.get('floor'))
                    page.session.set("apartment_number", user_found.get('apartment_number', '0/0'))
                    
                    # 3. Moliyaviy va hujjat ma'lumotlari
                    page.session.set("contract_number", user_found.get('contract_number'))
                    page.session.set("month_payments", user_found.get('month_payments'))
                    page.session.set("schedules_link", user_found.get('schedules_link'))
                    page.session.set("contracts_link", user_found.get('contracts_link'))
                    
                    # Doimiy xotiraga (client_storage) saqlash
                    if remember_me.value:
                        page.client_storage.set("contract_no", input_contract)
                        page.client_storage.set("article_code", user_found.get('article_code'))
                    else:
                        page.client_storage.remove("contract_no")
                        page.client_storage.remove("article_code")

                    # Muvaffaqiyatli animatsiya
                    status_container.content = ft.Icon(ft.Icons.CHECK_CIRCLE, color="green", size=30)
                    
                    full_name = user_found.get('full_name', '').strip()
                    name_parts = full_name.split()
                    display_name = name_parts[1] if len(name_parts) >= 2 else (name_parts[0] if name_parts else "Mijoz")
                    
                    welcome_msg = tm.get_word("welcome")
                    status_text.value = f"{welcome_msg}, {display_name}!"
                    status_text.color = "green"
                    page.update()
                    
                    time.sleep(1.2) 
                    page.go("/home")
                else:
                    status_container.content = ft.Icon(ft.Icons.CANCEL, color="red", size=30)
                    status_text.value = tm.get_word("login_error")
                    status_text.color = "red"
                    login_button.disabled = False
                    page.update()
            else:
                status_icon.visible = False
                status_text.value = f"Server xatosi: {response.status_code}"
                login_button.disabled = False
                page.update()

        except Exception as e:
            status_container.content = ft.Icon(ft.Icons.SIGNAL_WIFI_OFF, color="orange", size=30)
            status_text.value = tm.get_word("no_internet")
            status_text.color = "orange"
            login_button.disabled = False
            page.update()

    def cancel_click(e):
        contract_field.value = ""
        phone_field.value = ""
        status_text.value = ""
        status_icon.visible = False
        status_container.content = ft.Container()
        login_button.disabled = False
        page.update()

    # --- UI ELEMENTLARI ---
    contract_field = ft.TextField(
        label=tm.get_word("contract_label"), 
        value=saved_contract if saved_contract else "", 
        prefix_icon=ft.Icons.DESCRIPTION_OUTLINED,
        border_radius=25,
        width=280,
        height=50,
        text_size=14,
        color=TEXT_COLOR,
        label_style=ft.TextStyle(color=SEC_TEXT),
        focused_border_color=MAIN_COLOR,
        hint_text="Masalan: 12/22",
    )
    
    phone_field = ft.TextField(
        label=tm.get_word("phone_label"), 
        prefix_icon=ft.Icons.PHONE_ANDROID,
        hint_text="+998...",
        border_radius=25,
        width=280,
        height=50,
        text_size=14,
        color=TEXT_COLOR,
        label_style=ft.TextStyle(color=SEC_TEXT),
        focused_border_color=MAIN_COLOR,
        keyboard_type=ft.KeyboardType.PHONE
    )

    status_container = ft.Container(
        content=ft.Container(), 
        height=40, 
        alignment=ft.alignment.center
    )

    login_button = ft.ElevatedButton(
        content=ft.Text(tm.get_word("login_btn"), weight="bold", size=12),
        color="white",
        bgcolor=MAIN_COLOR,
        width=135,
        height=45,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
        on_click=lambda _: login_click(contract_field.value, phone_field.value)
    )

    cancel_button = ft.OutlinedButton(
        content=ft.Text(tm.get_word("cancel_btn"), weight="bold", size=12),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=20),
            side={ft.ControlState.DEFAULT: ft.BorderSide(1, CANCEL_COLOR)},
            color=CANCEL_COLOR
        ),
        width=135,
        height=45,
        on_click=cancel_click
    )

    return ft.Container(
        expand=True,
        bgcolor=BG_COLOR,
        content=ft.Column(
            spacing=0, 
            controls=[
                ft.Container(height=20),
                ft.Container(
                    content=ft.Image(
                        src=logo_src,
                        width=240,
                        height=240,
                        fit=ft.ImageFit.CONTAIN,
                    ),
                    margin=ft.margin.only(bottom=-80)
                ),
                ft.Text(
                    tm.get_word("login_hint"),
                    color=SEC_TEXT, 
                    size=12,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(height=25),
                contract_field,
                ft.Container(height=10),
                phone_field,
                ft.Container(
                    content=remember_me,
                    width=280,
                    padding=ft.padding.only(left=10)
                ),
                status_container,
                status_text,
                ft.Container(height=10),
                ft.Row(
                    controls=[login_button, cancel_button],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10
                ),
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.ADAPTIVE
        ),
        padding=20,
        alignment=ft.alignment.center
    )