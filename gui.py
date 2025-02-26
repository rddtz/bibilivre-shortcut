from nicegui import ui
import urllib.request, json

#   ui.image('https://picsum.photos/id/377/640/360').props('fit=scale-down')

image = 'https://www.bing.com/'
with urllib.request.urlopen("http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US") as url:
    data = json.load(url)
    image = image + data['images'][0]['url']

ui.image(image).classes("absolute-center").props(f"width=100vh, height=100vh")

with ui.card(align_items='end').classes('no-shadow border-[1px]').classes('fixed-center'):

    with ui.column(align_items='center'):
        ui.label('Atalho para catalogação de livros').style('color: #6E93D6; font-size: 200%; font-weight: 500')
        autocomplete_options = ['admin', 'biblioteca']
        ui.input(label="Usuário", autocomplete=autocomplete_options)
        ui.input(label="Senha").props("size=15")

        ui.button('BUTTON', on_click=lambda: ui.notify('button was pressed'))


ui.run(port=5555, title="Catalogação", native=True, reload=False)