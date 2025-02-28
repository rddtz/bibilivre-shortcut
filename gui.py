from nicegui import ui
import urllib.request, json

#   ui.image('https://picsum.photos/id/377/640/360').props('fit=scale-down')

logged : bool = False

def show_background():
    image = 'https://www.bing.com/'
    with urllib.request.urlopen("http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US") as url:
        data = json.load(url)
        image = image + data['images'][0]['url']

    ui.image(image).classes("absolute-center").props(f"width=100vh, height=100vh")



def login():
    global logged
    logged = not logged

    if logged:
        home()
    else:
        login_page()

def login_page():

    main.clear()
    with main:

        show_background()

        with ui.card(align_items='end').classes('no-shadow border-[1px]').classes('fixed-center'):

            with ui.column(align_items='center'):
                ui.label('Atalho para catalogação de livros').style('color: #6E93D6; font-size: 200%; font-weight: 500')
                
                autocomplete_options = ['admin', 'biblioteca']
                ui.input(label="Usuário", autocomplete=autocomplete_options)
                ui.input(label="Senha", password=True)

                ui.button('Entrar', on_click=lambda: login())

                ui.label('Utilize as mesmas credencias da plataforma Biblivre').style('color:rgb(81, 84, 90); font-size: 80%; font-weight: 500')

def home():
    main.clear()
     
     
    with main:
        #show_background()   

        ui.button('Sair', on_click=lambda: login())


        with ui.card(align_items='end').classes('no-shadow').classes('fixed-center'):
            with ui.row():
                ui.input(label="Autor")
                ui.input(label="Título")
                ui.number(label="Exemplares", min=0, validation={"Insira um número": lambda v: (type(v) == float) or (type(v) == float)})
                ui.number(label="Volume", min=1, validation={"Insira um número": lambda v: (type(v) == float) or (type(v) == float)})



main = ui.column()

if not logged:
    login_page()
else:
    pass

ui.run(port=5555, title="Catalogação") #, native=True, reload=False)    