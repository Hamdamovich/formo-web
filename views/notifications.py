import flet as ft
import httpx
import asyncio
from .settings_config import ThemeManager

class NotificationsView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/notifications", padding=0, spacing=0)
        self.page = page
        self.tm = ThemeManager(page)
        
        # Ranglarni yuklash
        self.main_color = self.tm.get_main_color()
        self.bgcolor = self.tm.get_bg_color()
        self.text_color = self.tm.get_text_color()
        self.card_color = self.tm.get_card_color()
        self.secondary_text = self.tm.get_secondary_text_color()

        self.read_notifications = []
        
        # UI elementlarini yaratish
        self.app_bar = ft.AppBar(
            leading=ft.IconButton(
                icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                icon_size=20, icon_color=self.text_color,
                on_click=lambda _: self.page.go("/home")
            ),
            title=ft.Text("Bildirishnomalar", size=18, weight=ft.FontWeight.BOLD, color=self.text_color),
            center_title=True, bgcolor=self.card_color, elevation=0.5,
            actions=[
                ft.IconButton(
                    icon=ft.Icons.DONE_ALL_ROUNDED, icon_color=self.main_color,
                    on_click=self.mark_all_as_read
                ),
                ft.VerticalDivider(width=10, color="transparent") 
            ]
        )

        self.notifications_list = ft.ListView(expand=True, spacing=12, padding=20)
        self.loader = ft.ProgressBar(visible=False, color=self.main_color)

        self.controls = [
            self.app_bar,
            self.loader,
            ft.Column(controls=[self.notifications_list], expand=True)
        ]

    def did_mount(self):
        # Sahifa yuklanganda birinchi storage'dan ma'lumotlarni xavfsiz olamiz
        self.page.run_task(self.initialize_page)

    async def initialize_page(self):
        """Storage bilan bog'liq ishlarni asinxron bajarish"""
        try:
            # Storage'dan o'qishda xatolik bo'lmasligi uchun try-except
            self.read_notifications = self.page.client_storage.get("read_notifications") or []
        except:
            self.read_notifications = []
        
        # Bildirishnomalarni yuklash
        await self.load_notifications()

    async def show_system_notification(self, title, body):
        """Push-notification simulyatsiyasi"""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Row([
                ft.Icon(ft.Icons.NOTIFICATIONS_ACTIVE, color="white"),
                ft.Text(f"{title}: {body}")
            ]),
            bgcolor=self.main_color
        )
        self.page.snack_bar.open = True
        self.page.update()

    async def mark_all_as_read(self, e):
        all_ids = []
        for control in self.notifications_list.controls:
            if hasattr(control, "data") and control.data:
                all_ids.append(control.data.get("id"))
                self.apply_read_style(control)
        
        if not all_ids: return

        self.read_notifications = list(set(self.read_notifications + all_ids))
        try:
            self.page.client_storage.set("read_notifications", self.read_notifications)
        except: pass

        self.page.snack_bar = ft.SnackBar(ft.Text("Barcha bildirishnomalar o'qildi"), bgcolor=self.main_color)
        self.page.snack_bar.open = True
        self.page.update()

    def apply_read_style(self, container: ft.Container):
        try:
            container.content.controls[0].bgcolor = ft.Colors.with_opacity(0.05, self.secondary_text)
            container.content.controls[0].content.color = self.secondary_text
            title_row = container.content.controls[1].controls[0]
            title_text = title_row.controls[0]
            title_text.weight = ft.FontWeight.NORMAL
            title_text.color = self.secondary_text
            container.content.controls[2].bgcolor = ft.Colors.TRANSPARENT
            container.update()
        except Exception as e:
            print(f"Style error: {e}")

    async def load_notifications(self):
        self.loader.visible = True
        self.page.update()

        try:
            client_id = self.page.session.get("client_id") or self.page.client_storage.get("client_id") or 2
            api_base_url = "https://formo-api.onrender.com" 
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{api_base_url}/payments", params={"client_id": client_id})
                
                if response.status_code == 200:
                    payments = response.json()
                    self.notifications_list.controls.clear()
                    
                    if not payments:
                        self.show_empty_state()
                    else:
                        new_found = False
                        for pay in payments:
                            p_id = pay.get("id")
                            amount = float(pay.get("amount", 0))
                            debt = float(pay.get("debt", 0))
                            is_new = p_id not in self.read_notifications
                            
                            if amount == 0 and debt > 0:
                                title = "Qarzdorlik qo'shildi"
                                desc = f"{debt:,.0f} so'm miqdorida yangi qarzdorlik yozildi."
                                icon = ft.Icons.ERROR_OUTLINE_ROUNDED
                                color = ft.Colors.RED_700
                            else:
                                title = "To'lov qabul qilindi"
                                desc = f"{amount:,.0f} so'm to'lov qabul qilindi."
                                icon = ft.Icons.PAYMENT_ROUNDED
                                color = ft.Colors.GREEN_700

                            if is_new: new_found = True
                            
                            self.notifications_list.controls.append(
                                self.build_notification_card({
                                    "id": p_id,
                                    "title": title,
                                    "desc": desc,
                                    "time": str(pay.get("date", "")),
                                    "icon": icon,
                                    "color": color,
                                    "is_new": is_new 
                                })
                            )
                        
                        if new_found:
                            await self.show_system_notification("Yangi xabar", "To'lovlar ro'yxati yangilandi")
                else:
                    self.show_empty_state()
        except Exception as e:
            print(f"Fetch error: {e}")
            self.show_empty_state()

        self.loader.visible = False
        self.page.update()

    def show_empty_state(self):
        self.notifications_list.controls.clear()
        self.notifications_list.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.NOTIFICATIONS_OFF_OUTLINED, size=80, color=ft.Colors.with_opacity(0.2, self.text_color)),
                    ft.Text("Hozircha bildirishnomalar yo'q", color=self.secondary_text, size=16, text_align=ft.TextAlign.CENTER)
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                margin=ft.margin.only(top=100)
            )
        )

    async def on_item_click(self, item_id, container: ft.Container):
        if item_id not in self.read_notifications:
            self.read_notifications.append(item_id)
            try:
                self.page.client_storage.set("read_notifications", self.read_notifications)
            except: pass
            self.apply_read_style(container)

    def build_notification_card(self, item):
        is_n = item["is_new"]
        c_title_color = self.text_color if is_n else self.secondary_text
        c_icon_color = item["color"] if is_n else self.secondary_text
        c_icon_bg = ft.Colors.with_opacity(0.1, item["color"]) if is_n else ft.Colors.with_opacity(0.05, self.secondary_text)
        c_weight = ft.FontWeight.W_600 if is_n else ft.FontWeight.NORMAL
        dot_color = self.main_color if is_n else ft.Colors.TRANSPARENT

        card = ft.Container(
            data={"id": item["id"]},
            padding=15, bgcolor=self.card_color, border_radius=15,
            shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.04, "black"), offset=ft.Offset(0, 4))
        )
        
        card.on_click = lambda _: self.page.run_task(self.on_item_click, item["id"], card)

        card.content = ft.Row([
            ft.Container(
                content=ft.Icon(item["icon"], color=c_icon_color, size=26),
                width=46, height=46, bgcolor=c_icon_bg,
                border_radius=12, alignment=ft.alignment.center
            ),
            ft.Column([
                ft.Row([
                    ft.Text(item["title"], size=14, weight=c_weight, color=c_title_color),
                    ft.Text(item["time"], size=10, color=self.secondary_text),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Text(item["desc"], size=12, color=self.secondary_text, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
            ], spacing=2, expand=True),
            ft.Container(width=8, height=8, bgcolor=dot_color, border_radius=4)
        ], vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        return card