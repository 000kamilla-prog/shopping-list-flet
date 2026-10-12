import flet as ft


@ft.control
class TitleText(ft.Text):
    def init(self):
        self.size = 26
        self.weight = ft.FontWeight.BOLD


@ft.control
class HintText(ft.Text):
    def init(self):
        self.size = 14
        self.color = ft.Colors.BLUE_GREY_600


@ft.control
class LoginField(ft.TextField):
    def init(self):
        self.label = "Введите логин"
        self.width = 280


@ft.control
class ItemField(ft.TextField):
    def init(self):
        self.label = "Название товара"
        self.expand = True


@ft.control
class LoginButton(ft.Button):
    def init(self):
        self.bgcolor = ft.Colors.BLUE_500
        self.color = ft.Colors.WHITE


@ft.control
class AddButton(ft.Button):
    def init(self):
        self.bgcolor = ft.Colors.GREEN_600
        self.color = ft.Colors.WHITE


@ft.control
class DeleteButton(ft.IconButton):
    def init(self):
        self.icon = ft.Icons.DELETE_OUTLINE
        self.icon_color = ft.Colors.RED_400


@ft.control
class ItemCheckbox(ft.Checkbox):
    def init(self):
        self.active_color = ft.Colors.GREEN_600


@ft.control
class ItemRow(ft.Row):
    def init(self):
        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER


@ft.control
class MainColumn(ft.Column):
    def init(self):
        self.spacing = 12
        self.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
