from nicegui import ui
import urllib.request, json
import logic

#   ui.image('https://picsum.photos/id/377/640/360').props('fit=scale-down')

# Global variables =-=-=-=-=-=-=-=-=-=
logged : bool = False
login_error : bool = False
selected : str = ''
relacao_codigo_nome : dict[str: str] = {}
codigos : list[str] = []
bibliografia_page : str = ""
# =-=-=-=-=-=-=-=-=

try:
    file = open("generos_literarios_para_catalogacao.txt", encoding='utf-8')
    codigos = file.readlines()
    file.close()

    relacao_codigo_nome = {}
    for i in range(len(codigos)):
        relacao_codigo_nome[codigos[i].split(":")[0]] = codigos[i].split(":")[1].replace("\n","")
        codigos[i] = codigos[i].split(":")[0]

except:
    pass

def change_selected_classificacao(label, value):

    global relacao_codigo_nome
    global codigos

    try:
        label.set_text(relacao_codigo_nome[value])
    except:
        label.set_text("Classificação não registrada")


def show_background():
    image = 'https://www.bing.com/'
    with urllib.request.urlopen("http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US") as url:
        data = json.load(url)
        image = image + data['images'][0]['url']

    ui.image(image).classes("absolute-center").props(f"width=100vh, height=100vh")


def login(label, user, senha):

    global logged
    global login_error
    global biblivre
    global bibliografia_page

    if logged:
        home()

    #print(v.sender)
    user_v = user.value
    senha_v = senha.value

    bibliografia = logic.login(user_v, senha_v, biblivre)

    if (bibliografia != ''):
        logged = True
        login_error = False
        label.set_text("")
        home()
    else:
        logged = False
        login_error = True
        label.set_text("Erro ao tentar entrar, verifique as credenciais.")
        user.set_value('')
        senha.set_value('')

def login_page():

    global login_error

    main.clear()
    with main:

        show_background()

        with ui.card(align_items='end').classes('no-shadow border-[1px]').classes('fixed-center'):

            with ui.column(align_items='center'):
                ui.label('Atalho para catalogação de livros').style('color: #6E93D6; font-size: 200%; font-weight: 500')
                
                autocomplete_options = ['admin', 'biblioteca']
                user = ui.input(label="Usuário", autocomplete=autocomplete_options)
                senha = ui.input(label="Senha", password=True)

                """if(login_error):
                    color = 'color:rgb(255, 0, 0)'
                else:
                    color = 'color:rgb(81, 84, 90)'"""

                login_error_label = ui.label('').style(f'color:rgb(255, 0, 0); font-size: 90%; font-weight: 500')
                ui.button('Entrar', on_click=lambda v, user=user, senha=senha, label=login_error_label: login(label, user, senha))

                ui.label('Utilize as mesmas credencias da plataforma Biblivre').style(f'color:rgb(81, 84, 90); font-size: 80%; font-weight: 500')

def home():

    global relacao_codigo_nome
    global codigos

    main.clear()
     
     
    with main:
        #show_background()   

        with ui.row():  
            #ui.button('Sair', on_click=lambda: login())

            with ui.card().classes('no-shadow border-[1px] justify-center') \
                .style('width: 100%; heigh: 100%').tight():

                with ui.row(): 

                    with ui.card(align_items='end').classes('no-shadow no-borde'):
                        with ui.row():
                            ui.input(label="Autor").props('clearable').style("width: 25vh")
                            ui.input(label="Título").props('clearable').style("width: 25vh")
                            ui.number(label="Exemplares", min=0,validation={"Insira um número": lambda v: (type(v) == float) or (type(v) == float)}).style("width: 25vh")
                    
                        with ui.row():       
                            with ui.card().classes('no-shadow').tight():
                                selected = ui.label().style('color:rgb(81, 84, 90); font-size: 70%; font-weight: 500')
                                ui.input(label="Classificação do livro",placeholder="028.5, 869.0(81), etc",autocomplete=codigos, on_change=lambda v, \
                                        label=selected: change_selected_classificacao(label, v.value)).props('clearable').style("width: 25vh") \
                                        .move(target_index=0)
                                
                            with ui.card().classes('no-shadow').tight():
                                ui.input(label="Código Cutter").props('clearable').style("width: 25vh")
                                ui.button('Procurar cutter on-line').tooltip('Utilizando o site www.tabelacutter.com').style("width: 25vh") \
                                .style('color:rgb(81, 84, 90); font-size: 60%; font-weight: 500') \
                                .classes('no-shadow')
                            ui.number(label="Volume", min=1, validation={"Insira um número": lambda v: (type(v) == float) or (type(v) == float)}).style("width: 25vh")
                                

                    with ui.card(align_items='end').classes('no-shadow no-border'):
                        with ui.column():
                            ui.button('Registrar').style("width: 25vh")
                            ui.button('Procurar').style("width: 25vh")
                            ui.button('Revisar').style("width: 25vh")
                            ui.button('Limpar').style("width: 25vh")

main = ui.column()

if not logged:
    login_page()
else:
    home()

biblivre = logic.inicia_driver()


ui.run(port=5555, title="Catalogação", reload=False) #, native=True, reload=False)    

biblivre.quit()