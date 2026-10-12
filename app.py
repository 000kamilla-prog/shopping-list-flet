from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

import flet as ft

from components import (
    TitleText, HintText, LoginField, ItemField, LoginButton,
    AddButton, DeleteButton, ItemCheckbox, ItemRow, MainColumn,
)
from models import Item
from storage import PairStorage


class BaseApp(ABC):
    @abstractmethod
    def show_login(self):
        pass


class ShoppingApp(BaseApp):
    def __init__(self, page):
        self.page = page
        self.page.title = "Список покупок"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.window.width = 650
        self.page.window.height = 730
        self.page.padding = 25

        self.items = [
            Item("Молоко"), Item("Хлеб"), Item("Яйца"),
            Item("Сыр"), Item("Масло"), Item("Рис"),
            Item("Макароны"), Item("Яблоки"), Item("Чай"),
            Item("Сахар"),
        ]
        self.session = PairStorage()
        self.session.set("login", "guest")
        self.session.set("time_in", datetime.now())

        self.login_field = LoginField()
        self.item_field = ItemField()
        self.message = HintText(value="")

        self.page.window.prevent_close = True
        self.page.window.on_event = self.on_window_event
        self.show_login()

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, value):
        self._items = list(value)

    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, value):
        self._session = value

    @property
    def page(self):
        return self._page

    @page.setter
    def page(self, value):
        self._page = value

    @property
    def login_field(self):
        return self._login_field

    @login_field.setter
    def login_field(self, value):
        self._login_field = value

    @property
    def item_field(self):
        return self._item_field

    @item_field.setter
    def item_field(self, value):
        self._item_field = value

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value

    def __str__(self):
        return f"Список покупок: {len(self.items)} товаров"

    def __repr__(self):
        return f"ShoppingApp(items={self.items!r})"

    def __eq__(self, other):
        if not isinstance(other, ShoppingApp):
            return NotImplemented
        left = [(item.name, item.bought) for item in self.items]
        right = [(item.name, item.bought) for item in other.items]
        return left == right

    def __len__(self):
        return len(self.items)

    def __contains__(self, item):
        return item in self.items

    def __iter__(self):
        return iter(self.items)

    def show_login(self):
        self.page.clean()
        self.page.add(
            MainColumn(controls=[
                TitleText(value="Список покупок"),
                HintText(value="Войдите, чтобы открыть список"),
                self.login_field,
                LoginButton(content="Войти", on_click=self.login),
                self.message,
            ])
        )

    def login(self, e):
        name = (self.login_field.value or "").strip()
        if not name:
            self.message.value = "Сначала введите логин"
            self.page.update()
            return

        self.session.set("login", name)
        self.session.set("time_in", datetime.now())
        self.message.value = ""
        self.show_items()

    def show_items(self):
        rows = []
        for item in sorted(self.items):
            rows.append(
                ItemRow(controls=[
                    ItemCheckbox(
                        value=item.bought,
                        on_change=lambda e, current=item: self.toggle(
                            current, e.control.value
                        ),
                    ),
                    ft.Text(
                        item.get_name(),
                        expand=True,
                        color=ft.Colors.GREY_500 if item.bought else ft.Colors.BLACK,
                    ),
                    DeleteButton(on_click=lambda e, current=item: self.remove(current)),
                ])
            )

        bought_count = sum(item.bought for item in self.items)
        self.page.clean()
        self.page.add(
            MainColumn(expand=True, controls=[
                TitleText(value="Мой список покупок"),
                HintText(value="Пользователь: " + self.session.get("login")),
                ft.Row(controls=[
                    self.item_field,
                    AddButton(content="Добавить", on_click=self.add),
                ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                HintText(value=f"Всего: {len(self.items)}   Куплено: {bought_count}"),
                self.message,
                ft.Divider(),
                MainColumn(controls=rows, expand=True, scroll=ft.ScrollMode.AUTO),
            ])
        )

    def add(self, e):
        name = (self.item_field.value or "").strip()
        if not name:
            self.message.value = "Введите название товара"
            self.page.update()
            return

        item = Item(name)
        if item in self.items:
            self.message.value = "Такой товар уже есть"
            self.page.update()
            return

        self.items.append(item)
        self.item_field.value = ""
        self.message.value = "Товар добавлен"
        self.show_items()

    def toggle(self, item, value):
        item.bought = value
        self.show_items()

    def remove(self, item):
        self.items.remove(item)
        self.message.value = "Товар удалён"
        self.show_items()

    def save_report(self):
        login = self.session.get("login")
        login = login.replace("|", "/").replace("\n", " ")[:16]
        time_in = self.session.get("time_in").strftime("%d.%m.%Y %H:%M:%S")
        time_out = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        border = "+" + "-" * 18 + "+" + "-" * 21 + "+" + "-" * 21 + "+\n"
        report = (
            border
            + f"| {'login':<16} | {'time_in':<19} | {'time_out':<19} |\n"
            + border
            + f"| {login:<16} | {time_in:<19} | {time_out:<19} |\n"
            + border
        )

        report_dir = Path(__file__).parent / "reports"
        report_dir.mkdir(exist_ok=True)
        with (report_dir / "report.txt").open("a", encoding="utf-8") as file:
            file.write(report)

    async def on_window_event(self, e):
        if e.type == ft.WindowEventType.CLOSE:
            try:
                self.save_report()
            except OSError as error:
                self.message.value = "Ошибка сохранения отчёта: " + str(error)
                self.page.update()
                return
            await self.page.window.destroy()

    @staticmethod
    def start(page):
        ShoppingApp(page)
