import flet as ft
import qrcode
import base64
from io import BytesIO
from .settings_config import ThemeManager

class ClientQRView(ft.Container):
    def __init__(self, page: ft.Page, client_data: dict):
        super().__init__()
        self.page = page
        self.client_data = client_data
        self.tm = ThemeManager(page)
        self.expand = True
        self.bgcolor = self.tm.get_bg_color()
        self.content = self.build_ui()

    def generate_qr_base64(self, data):
        # QR kod generatori - barcha ma'lumotlar bilan
        qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=2)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()

    def build_ui(self):
        main_color = self.tm.get_main_color()
        text_color = self.tm.get_text_color()
        card_bg = self.tm.get_card_color()
        sec_text = "grey"

        # 1. QR kod ichiga barcha ma'lumotlarni yig'ish (Skaner qilganda hammasi ko'rinadi)
        qr_raw_data = (
            f"Mijoz: {self.client_data.get('full_name', '-')}\n"
            f"ID: {self.client_data.get('article_code', '-')}\n"
            f"Tel: {self.client_data.get('phone_number', '-')}\n"
            f"Shartnoma: {self.client_data.get('contract_number', '-')}\n"
            f"Xonadon: {self.client_data.get('apartment_number', '-')}"
        )
        qr_base64 = self.generate_qr_base64(qr_raw_data)

        # 2. HEADER
        header = ft.Container(
            content=ft.Row([
                ft.IconButton(
                    icon=ft.Icons.CLOSE_ROUNDED, 
                    icon_color=text_color, 
                    on_click=lambda _: self.page.go("/home")
                ),
                ft.Text("Mijoz QR kodi", size=18, weight="bold", color=text_color),
                ft.Container(width=40)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=10
        )

        # 3. QR CARD (Asosiy vizual qism)
        qr_card = ft.Container(
            content=ft.Column([
                # QR Rasm oq fonda
                ft.Container(
                    content=ft.Image(
                        src_base64=qr_base64,
                        width=200,
                        height=200,
                    ),
                    bgcolor="white",
                    padding=10,
                    border_radius=15,
                ),
                ft.Container(height=10),
                # Mijozning asosiy ma'lumotlari matn ko'rinishida
                ft.Text(self.client_data.get('full_name', '-'), size=18, weight="bold", color=text_color, text_align="center"),
                ft.Text(f"ID: {self.client_data.get('article_code', '-')}", size=14, color=sec_text),
                
                ft.Divider(height=20, color=ft.Colors.with_opacity(0.1, sec_text)),
                
                # Qo'shimcha ma'lumotlar (Kichikroq va scannable bo'lmagan qismi)
                ft.Row([
                    ft.Icon(ft.Icons.PHONE_ANDROID_ROUNDED, size=14, color=main_color),
                    ft.Text(self.client_data.get('phone_number', '-'), size=12, color=text_color),
                ], alignment=ft.MainAxisAlignment.CENTER),
                
                ft.Row([
                    ft.Icon(ft.Icons.ASSIGNMENT_IND_ROUNDED, size=14, color=main_color),
                    ft.Text(f"Shartnoma: {self.client_data.get('contract_number', '-')}", size=12, color=text_color),
                ], alignment=ft.MainAxisAlignment.CENTER),

            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=card_bg,
            padding=25,
            border_radius=30,
            margin=ft.margin.symmetric(horizontal=30),
            shadow=self.tm.get_box_shadow()
        )

        # 4. BRENDING (Pastki qism - Copyright)
        branding = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.COPYRIGHT_ROUNDED, size=14, color=sec_text),
                ft.Text("FormoMobile 2026 | HamdamovichSoft", size=12, color=sec_text, weight="w500"),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
            margin=ft.margin.only(bottom=40)
        )

        return ft.Column([
            header,
            ft.Container(expand=True), # Moslashuvchan bo'shliq
            qr_card,
            ft.Container(expand=True), # Moslashuvchan bo'shliq
            branding
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)