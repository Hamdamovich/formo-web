import flet as ft

class ThemeManager:
    def __init__(self, page: ft.Page):
        """
        ThemeManager ilovadagi barcha ranglarni va matnlarni (tillarni) 
        markazlashgan holda boshqaradi.
        """
        self.page = page

        # --- KO'P TILLI LUG'AT (TRANSLATIONS) ---
        self.TRANSLATIONS = {
            "O'zbekcha": {
                # Settings sahifasi
                "title": "Sozalamalar",
                "lang_label": "Ilova tili",
                "theme_label": "Tungi mavzu",
                "theme_sub": "Light / Dark rejim",
                "bright_label": "Yorug'lik balansi",
                "bright_sub": "Ekran yorqinligi",
                "current": "Joriy",
                "version": "Versiya",
                "toast": "Til o'zgartirildi",
                "back": "Orqaga qaytish",
                
                # Login sahifasi
                "login_btn": "KIRISH",
                "cancel_btn": "BEKOR QILISH",
                "contract_label": "Shartnoma raqami",
                "phone_label": "Telefon raqami",
                "login_hint": "Tizimga kirish uchun ma'lumotlarni kiriting",
                "remember_me": "Shartnoma raqamini eslab qolish",
                "fill_fields": "Maydonlarni to'ldiring!",
                "checking": "Tekshirilmoqda...",
                "welcome": "Xush kelibsiz",
                "login_error": "Shartnoma yoki telefon raqami noto'g'ri!",
                "no_internet": "Internet bilan aloqa yo'q!",
                "server_error": "Server bilan aloqa uzildi",

                # Home Header & Debt Card
                "home_welcome": "Xush kelibsiz 👋",
                "guest": "Mijoz",
                "notifications": "Bildirishnomalar",
                "debt_title": "Qolgan qarzdorlik",
                "total_amount": "Umumiy miqdor",
                "paid_amount": "To'langan summa",
                "currency": "so'm",
                "error": "Xatolik",
                "no_data": "Ma'lumot topilmadi",

                # Home Menu Grid
                "services_title": "Xizmatlar",
                "all_btn": "Hammasi",
                "menu_history": "To'lov tarixi",
                "menu_schedule": "To'lov grafigi",
                "menu_contract": "Shartnoma",
                "menu_location": "Xonadon joylashuvi",
                "menu_contact": "Aloqa",
                "menu_settings": "Sozlamalar",

                # History (To'lov tarixi) sahifasi
                "history_title": "To'lovlar tarixi",
                "col_no": "№",
                "col_date": "Sana",
                "col_type": "Turi",
                "col_pay": "To'lovlar",
                "col_debt": "Qarzdorlik",
                "total_sum": "Umumiy miqdor:",
                "paid_sum": "To'langan:",
                "remain_sum": "Qolgan qarz:",
                "list_title": "To'lovlar ro'yxati:",
                "note": "Izoh: To'lovlar bank tasdig'idan so'ng bazada aks etadi.",

                # Schedules (To'lov grafigi) sahifasi qo'shimchalari
                "schedule_title": "To'lov grafigi",
                "schedule_list_title": "To'lov jadvali:",
                "col_total_debt": "Umumiy qarz",
                "col_monthly_pay": "Oylik to'lov",
                "floor": "Qavat",
                "apartment": "Xonadon",
                "status": "Xolati",
                "area": "Xonadon kv.m",
                "period": "Muddati (oy)",
                "start_percent": "Boshlang'ich %",
                "total_price": "Jami narxi",
                "initial_payment": "Boshlang'ich to'lov",
                "schedule_note": "Izoh: Ushbu grafik shartnoma asosida tasdiqlangan.",
                "error_link_not_found": "Xatolik: Excel ssilka topilmadi",
                "error_download_failed": "Xatolik: Faylni yuklab bo'lmadi",
                "error_process_data": "Xatolik: Ma'lumotlarni ishlashda xato",

                # Chessboard (Shaxmatka) sahifasi qo'shimchalari
                "lot_13": "Yorqin kelajak (13-lot)",
                "lot_12": "Vatan (12-lot)",
                "lot_11": "Istiqlol (11-lot)",
                "floor_suffix": "-qavat",
                "basement": "Yerto'la",
                "non_residential": "NOTURAR",
                "client_label": "Mijoz",
                "apartment_label": "Xonadon",
                "selected_msg": "tanlandi",

                # Bottom Navigation
                "home_tab": "Asosiy",
                "history_tab": "Tarix",
                "profile_tab": "Profil"
            },
            "Русский язык": {
                # Settings sahifasi
                "title": "Настройки",
                "lang_label": "Язык приложения",
                "theme_label": "Ночной режим",
                "theme_sub": "Светлая / Темная тема",
                "bright_label": "Баланс яркости",
                "bright_sub": "Яркость экрана",
                "current": "Текущий",
                "version": "Версия",
                "toast": "Язык изменен",
                "back": "Назад",
                
                # Login sahifasi
                "login_btn": "ВХОД",
                "cancel_btn": "ОТМЕНА",
                "contract_label": "Номер контракта",
                "phone_label": "Номер телефона",
                "login_hint": "Введите данные для входа в систему",
                "remember_me": "Запомнить номер контракта",
                "fill_fields": "Заполните поля!",
                "checking": "Проверка...",
                "welcome": "Добро пожаловать",
                "login_error": "Номер контракта или телефона неверный!",
                "no_internet": "Нет интернет-соединения!",
                "server_error": "Ошибка сервера",

                # Home Header & Debt Card
                "home_welcome": "Добро пожаловать 👋",
                "guest": "Клиент",
                "notifications": "Уведомления",
                "debt_title": "Оставшаяся задолженность",
                "total_amount": "Общая сумма",
                "paid_amount": "Оплаченная сумма",
                "currency": "сум",
                "error": "Ошибка",
                "no_data": "Данные не найдены",

                # Home Menu Grid
                "services_title": "Услуги",
                "all_btn": "Все",
                "menu_history": "История платежей",
                "menu_schedule": "График платежей",
                "menu_contract": "Контракт",
                "menu_location": "Расположение",
                "menu_contact": "Связь",
                "menu_settings": "Настройки",

                # History (История платежей) sahifasi
                "history_title": "История платежей",
                "col_no": "№",
                "col_date": "Дата",
                "col_type": "Тип",
                "col_pay": "Оплаты",
                "col_debt": "Задолженность",
                "total_sum": "Общая сумма:",
                "paid_sum": "Оплачено:",
                "remain_sum": "Остаток:",
                "list_title": "Список оплат:",
                "note": "Примечание: Платежи отражаются в базе после подтверждения банком.",

                # Schedules (График платежей) sahifasi qo'shimchalari
                "schedule_title": "График платежей",
                "schedule_list_title": "График оплат:",
                "col_total_debt": "Общий долг",
                "col_monthly_pay": "Ежем. платеж",
                "floor": "Этаж",
                "apartment": "Квартира",
                "status": "Статус",
                "area": "Кв.м квартиры",
                "period": "Срок (мес)",
                "start_percent": "Первоначальный %",
                "total_price": "Общая стоимость",
                "initial_payment": "Первоначальный взнос",
                "schedule_note": "Примечание: Данный график утвержден на основании договора.",
                "error_link_not_found": "Ошибка: Ссылка на Excel не найдена",
                "error_download_failed": "Ошибка: Не удалось загрузить файл",
                "error_process_data": "Ошибка: Ошибка при обработке данных",

                # Chessboard (Шахматка) sahifasi qo'shimchalari
                "lot_13": "Ёркин келажак (13-лот)",
                "lot_12": "Ватан (12-лот)",
                "lot_11": "Истиклол (11-лот)",
                "floor_suffix": "-этаж",
                "basement": "Подвал",
                "non_residential": "НЕЖИЛОЕ",
                "client_label": "Клиент",
                "apartment_label": "Квартира",
                "selected_msg": "выбрано",

                # Bottom Navigation
                "home_tab": "Главная",
                "history_tab": "История",
                "profile_tab": "Профиль"
            }
        }

    # --- MATNLARNI OLISH FUNKSIYASI ---
    def get_word(self, key):
        """Storage-dagi tildan kelib chiqib so'zni qaytaradi"""
        lang = self.page.client_storage.get("lang") or "O'zbekcha"
        return self.TRANSLATIONS.get(lang, self.TRANSLATIONS["O'zbekcha"]).get(key, key)

    # --- RANG FUNKSIYALARI ---
    def get_bg_color(self):
        """Asosiy fon rangi"""
        if self.page.theme_mode == ft.ThemeMode.DARK:
            return "#1A1C1E"
        return "#F8F9FE"

    def get_card_color(self):
        """Kartochkalar fon rangi"""
        if self.page.theme_mode == ft.ThemeMode.DARK:
            return "#2D3033"
        return ft.Colors.WHITE

    def get_text_color(self):
        """Asosiy matn rangi"""
        if self.page.theme_mode == ft.ThemeMode.DARK:
            return ft.Colors.WHITE
        return ft.Colors.BLACK

    def get_main_color(self):
        """Ilovaning asosiy brend rangi"""
        return "#00838F"

    def get_secondary_text_color(self):
        """Yordamchi matnlar rangi"""
        return "grey"

    def get_box_shadow(self):
        """Kartochkalar uchun soya"""
        if self.page.theme_mode == ft.ThemeMode.DARK:
            return None
        return ft.BoxShadow(
            blur_radius=5,
            color=ft.Colors.with_opacity(0.1, "black")
        )

    # --- SOZLAMALAR ---
    def get_language(self):
        return self.page.client_storage.get("lang") or "O'zbekcha"

    def get_brightness(self):
        return self.page.client_storage.get("brightness_level") or 0.8