import flet as ft
import httpx
from .settings_config import ThemeManager

# Qizil nuqtani global obyekt sifatida yaratamiz (bildirishnomalar uchun)
notification_dot = ft.Container(
    bgcolor="red",
    width=10,
    height=10,
    border_radius=5,
    right=8,
    top=8,
    visible=False, # API dan ma'lumot kelguncha yashirin
)

async def check_notifications(page: ft.Page):
    """API orqali yangi bildirishnomalarni tekshirish funksiyasi"""
    if not page:
        return
    try:
        client_id = page.session.get("client_id") or 2
        try:
            read_ids = page.client_storage.get("read_notifications") or []
        except:
            read_ids = []
            
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                "https://formo-api.onrender.com/payments", 
                params={"client_id": client_id}
            )
            if response.status_code == 200:
                payments = response.json()
                has_new = any(pay.get("id") not in read_ids for pay in payments)
                notification_dot.visible = has_new
                if page.adapter:
                    notification_dot.update()
    except Exception as e:
        print(f"Notification error: {e}")

def get_home_up(page: ft.Page, main_color: str):
    # ThemeManager modulini ishga tushiramiz
    tm = ThemeManager(page)
    
    # Dinamik ranglarni moduldan olamiz
    text_color = tm.get_text_color()
    secondary_text = tm.get_secondary_text_color()
    
    # Dark mode uchun avatar foni va ikonka rangi
    avatar_bg = "#263238" if page.theme_mode == ft.ThemeMode.DARK else "#E0F2F1"
    icon_button_color = ft.Colors.WHITE if page.theme_mode == ft.ThemeMode.DARK else ft.Colors.BLACK

    # Nuqta atrofidagi chegara
    notification_dot.border = ft.border.all(2, tm.get_card_color())

    # --- ISMNI FORMATLASH QISMI ---
    guest_word = tm.get_word("guest")
    raw_full_name = page.session.get("user_full_name") or guest_word
    formatted_name = raw_full_name.strip().title()
    
    name_parts = formatted_name.split()
    display_name = f"{name_parts[0]} {name_parts[1]}" if len(name_parts) > 2 else formatted_name

    return ft.Row(
        controls=[
            # Chap tomondagi qism: Avatar va Ism
            ft.Row(
                controls=[
                    # --- AVATAR (BOSILGANDA CLIENT_CARD OCHILADI) ---
                    ft.Container(
                        content=ft.CircleAvatar(
                            content=ft.Icon(ft.Icons.PERSON, color=main_color), 
                            bgcolor=avatar_bg,
                            radius=22
                        ),
                        on_click=lambda _: page.go("/profile"), # Client Card sahifasiga o'tish
                        tooltip=tm.get_word("profile_tab") # "Mening profilim"
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                tm.get_word("home_welcome"), 
                                size=11, 
                                color=secondary_text
                            ),
                            ft.Text(
                                display_name, 
                                size=13, 
                                weight="bold",
                                color=text_color,
                                max_lines=1,
                                overflow=ft.TextOverflow.ELLIPSIS,
                                width=150 
                            ),
                        ], 
                        spacing=0
                    )
                ],
                spacing=10
            ),
            
            # O'ng tomondagi qism: Bildirishnomalar
            ft.Stack(
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.NOTIFICATIONS_NONE_ROUNDED,
                        icon_color=icon_button_color,
                        icon_size=26,
                        on_click=lambda _: page.go("/notifications")
                    ),
                    notification_dot
                ]
            )
        ], 
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )