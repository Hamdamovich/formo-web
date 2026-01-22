import flet as ft
from .settings_config import ThemeManager
from .home_down import get_home_down  # Navigatsiya paneli

class ChessboardView(ft.Container):
    """
    Xonadonlar shaxmati moduli.
    Kataklar balandligi dinamik moslashadi va ekran bo'ylab optimal taqsimlanadi.
    """
    def __init__(self, page: ft.Page, client_data):
        super().__init__()
        self.page = page
        self.tm = ThemeManager(page)
        self.expand = True
        self.client_data = client_data
        
        # Dinamik ranglar
        self.bg_color = self.tm.get_bg_color()
        self.card_bg = self.tm.get_card_color()
        self.text_color = self.tm.get_text_color()
        self.sec_text = self.tm.get_secondary_text_color()
        self.main_color = self.tm.get_main_color()
        self.border_color = "#3D4043" if page.theme_mode == ft.ThemeMode.DARK else "#E2E8F0"
        self.header_bg = "#1A1C1E" if page.theme_mode == ft.ThemeMode.DARK else "#F8FAFC"
        
        # Logika: apartment_number ajratish
        try:
            parts = str(self.client_data["apartment_number"]).strip().split("/")
            self.lot_id = parts[0]
            self.target_apartment = int(parts[1]) if len(parts) > 1 else None
        except Exception:
            self.lot_id = "Noma'lum"
            self.target_apartment = None

        self.current_lot_title = self.tm.get_word(f"lot_{self.lot_id}") 
        if self.current_lot_title == f"lot_{self.lot_id}":
            self.current_lot_title = f"{self.lot_id}-lot"

        # Static Data
        f_suffix = self.tm.get_word("floor_suffix")
        noturar_label = self.tm.get_word("non_residential")
        yertola_label = self.tm.get_word("basement")

        self.floors_data = [
            {"floor": f"12{f_suffix}", "units": [{"id": 53}, {"id": 54}, {"id": 55}, {"id": 56}, {"id": 57}]},
            {"floor": f"11{f_suffix}", "units": [{"id": 48}, {"id": 49}, {"id": 50}, {"id": 51}, {"id": 52}]},
            {"floor": f"10{f_suffix}", "units": [{"id": 43}, {"id": 44}, {"id": 45}, {"id": 46}, {"id": 47}]},
            {"floor": f"9{f_suffix}", "units": [{"id": 38}, {"id": 39}, {"id": 40}, {"id": 41}, {"id": 42}]},
            {"floor": f"8{f_suffix}", "units": [{"id": 33}, {"id": 34}, {"id": 35}, {"id": 36}, {"id": 37}]},
            {"floor": f"7{f_suffix}", "units": [{"id": 28}, {"id": 29}, {"id": 30}, {"id": 31}, {"id": 32}]},
            {"floor": f"6{f_suffix}", "units": [{"id": 23}, {"id": 24}, {"id": 25}, {"id": 26}, {"id": 27}]},
            {"floor": f"5{f_suffix}", "units": [{"id": 18}, {"id": 19}, {"id": 20}, {"id": 21}, {"id": 22}]},
            {"floor": f"4{f_suffix}", "units": [{"id": 13}, {"id": 14}, {"id": 15}, {"id": 16}, {"id": 17}]},
            {"floor": f"3{f_suffix}", "units": [{"id": 8}, {"id": 9}, {"id": 10}, {"id": 11}, {"id": 12}]},
            {"floor": f"2{f_suffix}", "units": [{"id": 3}, {"id": 4}, {"id": 5}, {"id": 6}, {"id": 7}]},
            {"floor": f"1{f_suffix}", "units": [{"id": 1}, {"label": noturar_label, "span": 3}, {"id": 2}]},
            {"floor": yertola_label, "units": [{"id": -1}, {"id": -2}, {"id": -3}, {"id": -4}, {"id": -5}]},
        ]

        self.bgcolor = self.bg_color 
        self.content = self.build_ui()

    def get_unit_color(self, unit):
        unit_id = unit.get("id")
        unit_label = unit.get("label")
        target_label = self.tm.get_word("non_residential")
        if (unit_id is not None and unit_id == self.target_apartment) or \
           (unit_label == target_label and self.target_apartment == 0):
            return ft.Colors.RED_ACCENT_700
        return "#37474F" if self.page.theme_mode == ft.ThemeMode.DARK else ft.Colors.BLUE_GREY_100

    def create_unit(self, unit):
        unit_id = unit.get("id")
        unit_label = unit.get("label")
        return ft.Container(
            content=ft.Text(
                str(unit_id) if unit_id is not None else unit_label,
                color="white" if self.page.theme_mode == ft.ThemeMode.DARK or self.get_unit_color(unit) == ft.Colors.RED_ACCENT_700 else "black", 
                weight="bold", size=11
            ),
            alignment=ft.alignment.center,
            bgcolor=self.get_unit_color(unit),
            expand=unit.get("span", 1), # Eniga cho'zilish
            border_radius=4,
            ink=True,
            on_click=lambda _: self.on_unit_click(unit_id, unit_label)
        )

    def on_unit_click(self, unit_id, label):
        msg = self.tm.get_word("selected_msg")
        text = f"{self.tm.get_word('apartment_label')} {unit_id} {msg}" if unit_id is not None else f"{label} {msg}"
        self.page.snack_bar = ft.SnackBar(ft.Text(text), duration=1500)
        self.page.snack_bar.open = True
        self.page.update()

    def build_ui(self):
        # Kvadraturalar (Sarlavha)
        sq_values = ["61.64", "54.1", "44.51", "54.1", "61.64"]
        header_row_content = [ft.Container(width=60)]
        for val in sq_values:
            header_row_content.append(
                ft.Container(
                    content=ft.Text(val, size=10, weight="bold", color=self.sec_text),
                    expand=1,
                    alignment=ft.alignment.center
                )
            )
        
        grid_rows = [ft.Row(controls=header_row_content, spacing=5)]

        # Qavatlar
        for data in self.floors_data:
            row_content = [
                ft.Container(
                    content=ft.Text(data['floor'], size=11, weight="w500", color=self.text_color),
                    width=60,
                    alignment=ft.alignment.center_left
                )
            ]
            for u in data["units"]:
                row_content.append(self.create_unit(u))
            
            # Har bir qavat Row-ga expand=True berildi, shunda balandlik teng taqsimlanadi
            grid_rows.append(
                ft.Row(
                    controls=row_content, 
                    spacing=5, 
                    expand=True  # Qavatlar vertikal bo'shliqni to'ldiradi
                )
            )

        # HEADER PANEL
        header_panel = ft.Container(
            content=ft.Row([
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED, 
                    icon_size=20,
                    icon_color=self.text_color,
                    on_click=lambda _: self.page.go("/home") 
                ),
                ft.Column([
                    ft.Text(self.current_lot_title, size=16, weight="bold", color=self.text_color),
                    ft.Row([
                        ft.Icon(ft.Icons.PERSON, size=13, color=self.sec_text),
                        ft.Text(f"{self.tm.get_word('client_label')}: {self.client_data['name']}", size=12, color=self.sec_text)
                    ], spacing=5),
                    ft.Row([
                        ft.Icon(ft.Icons.HOME_ROUNDED, size=13, color=self.sec_text),
                        ft.Text(f"{self.tm.get_word('apartment_label')}: {self.client_data['apartment_number']}", size=12, color=self.sec_text)
                    ], spacing=5)
                ], spacing=1, expand=True)
            ], alignment=ft.MainAxisAlignment.START, spacing=5, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.only(left=10, right=15, top=10, bottom=10),
            bgcolor=self.header_bg,
            border=ft.border.only(bottom=ft.BorderSide(1, self.border_color))
        )

        # Bottom Nav
        bottom_nav = get_home_down(self.page, self.tm, self.main_color, self.card_bg, active_route="/chessboard")

        # ASOSIY COLUMN
        return ft.Column(
            expand=True,
            spacing=0,
            controls=[
                header_panel,
                ft.Container(
                    content=ft.Column(
                        controls=grid_rows,
                        spacing=5,
                        expand=True, # Ichki grid to'liq bo'shliqni oladi
                    ),
                    padding=ft.padding.only(left=10, right=10, top=10, bottom=5),
                    expand=True # Grid va Home_down orasidagi bo'shliqni yo'qotadi
                ),
                bottom_nav
            ]
        )

def chessboard_view(page: ft.Page):
    client_data = {
        "name": page.session.get("client_name") or "Mijoz ma'lumoti yo'q",
        "apartment_number": page.session.get("apartment_number") or "Noma'lum"
    }
    return ChessboardView(page, client_data)