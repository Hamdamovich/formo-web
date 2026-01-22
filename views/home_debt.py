import flet as ft
import requests
from .settings_config import ThemeManager

def format_money(amount):
    """24836000 -> 24.836.000 formatiga o'tkazish"""
    try:
        if amount is None: return "0"
        return f"{int(float(amount)):,}".replace(",", ".")
    except (ValueError, TypeError):
        return "0"

def get_home_debt(page: ft.Page):
    # ThemeManager modulini ishga tushiramiz
    tm = ThemeManager(page)
    
    # Dinamik ranglar
    text_color = tm.get_text_color()
    secondary_text = tm.get_secondary_text_color()
    
    # Umumiy miqdor raqami uchun rang (Mavzuga qarab)
    sub_amount_color = "#E0E0E0" if page.theme_mode == ft.ThemeMode.DARK else "#424242"
    divider_color = "#3D4043" if page.theme_mode == ft.ThemeMode.DARK else "#EEEEEE"

    # 1. Sessiyadan mijoz ID sini olamiz
    client_id = page.session.get("client_id")
    
    # 2. API manzili
    PAYMENTS_API = f"https://formo-api.onrender.com/payments?client_id={client_id}"

    total_debt = 0.0      
    total_paid = 0.0      
    error_message = None

    try:
        response = requests.get(PAYMENTS_API, timeout=15)
        if response.status_code == 200:
            payments_data = response.json()
            if isinstance(payments_data, list):
                for p in payments_data:
                    p_type = str(p.get('payment_type', '')).strip().lower()
                    # API dan kelayotgan turlarni tekshirish (uz/ru farq qilishi mumkin bo'lsa shunga moslang)
                    if "qarz" in p_type:
                        total_debt += float(p.get('debt', 0))
                    elif "lov" in p_type:
                        total_paid += float(p.get('amount', 0))
            else:
                error_message = tm.get_word("no_data") # "Ma'lumot topilmadi"
        else:
            error_message = f"API Error: {response.status_code}"
    except Exception as e:
        error_message = tm.get_word("no_internet") # Lug'atdan: "Internet bilan aloqa yo'q!"
        print(f"DEBUG ERROR: {e}")

    remaining = total_debt - total_paid

    return ft.Container(
        content=ft.Column(
            controls=[
                # 1. Asosiy Qolgan qarzdorlik
                ft.Text(tm.get_word("debt_title"), size=14, color=secondary_text, weight="w500"),
                ft.Text(
                    f"{format_money(remaining)} {tm.get_word('currency')}" if not error_message else tm.get_word("error"), 
                    size=28, 
                    weight="bold", 
                    color=text_color 
                ),
                
                ft.Container(height=10),
                
                # 2. Umumiy va To'langan summa
                ft.Container(
                    content=ft.Row(
                        controls=[
                            # Jami Qarz
                            ft.Column(
                                controls=[
                                    ft.Text(tm.get_word("total_amount"), size=11, color=secondary_text),
                                    ft.Text(
                                        format_money(total_debt), 
                                        size=14, 
                                        weight="bold", 
                                        color=sub_amount_color
                                    ),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=2
                            ),
                            
                            ft.VerticalDivider(width=1, color=divider_color),
                            
                            # Jami To'lov
                            ft.Column(
                                controls=[
                                    ft.Text(tm.get_word("paid_amount"), size=11, color=secondary_text),
                                    ft.Text(
                                        format_money(total_paid), 
                                        size=14, 
                                        weight="bold", 
                                        color="#4CAF50" # Yashil (Muvaffaqiyatli to'lov rangi)
                                    ),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=2
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    ),
                    padding=ft.padding.symmetric(vertical=10),
                ),
                # Xatolik xabari
                ft.Text(error_message if error_message else "", size=10, color="red")
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0
        ),
        padding=ft.padding.only(top=10, bottom=10),
        alignment=ft.alignment.center
    )