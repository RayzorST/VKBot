import flet

def main(page: flet.Page):
    page.title = "Flet counter example"
    page.vertical_alignment = flet.MainAxisAlignment.CENTER

    txt_number = flet.TextField(value="0", text_align=flet.TextAlign.RIGHT, width=100)

    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()

    page.add(
        flet.Row(
            [
                flet.IconButton(flet.icons.REMOVE, on_click=minus_click),
                txt_number,
                flet.IconButton(flet.icons.ADD, on_click=plus_click),
            ],
            alignment=flet.MainAxisAlignment.CENTER,
        )
    )

def web_start():
    flet.app(target=main)