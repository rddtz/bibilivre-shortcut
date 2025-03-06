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
        if not value:
            label.set_text("")
        else:
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

    bibliografia_page = logic.login(user_v, senha_v, biblivre)

    if (bibliografia_page != ''):
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

def novoExemplar(card, index, pesquisa):

    global biblivre
    global bibliografia_page

    biblivre.get(bibliografia_page)
    logic.NovoExemplar(biblivre, index, pesquisa)
    card.clear()
    procurar(card, pesquisa, '')

def procurar(card, autor, titulo):
    
    global biblivre
    global bibliografia_page

    card.clear()
    biblivre.get(bibliografia_page)   
    
    pesquisa = f'{autor.value if autor.value != None else ""} {titulo.value if titulo.value != None else ""}'
    resultados = logic.ResultsSearch(pesquisa, biblivre)
    print(resultados)

    if(pesquisa != ' ' and pesquisa != '' and resultados > 0):
        with card:
            ui.label(f"{resultados} Resultados")
            for i in range(1, resultados + 1):
                with ui.row():
                    ui.label(logic.GetTextIndex(biblivre, i)).style("width: 80vh; font-size: 200%; font-weight: 500'")
                    ui.button("Novo Exemplar", on_click=lambda v, card=card, index=i, pesquisa=pesquisa: novoExemplar(card, index, pesquisa))


def limpar(card, autor, titulo, exemp, classi, cutter, vol):
    autor.set_value(None)
    titulo.set_value(None)
    exemp.set_value(None)
    classi.set_value(None)
    cutter.set_value(None)
    vol.set_value(None)
    card.clear()


def registrar(card, autor, titulo, exemp, classi, cutter, vol):

    global bibliografia_page
    global biblivre

    biblivre.get(bibliografia_page)

    nome = logic.FormataNome(autor.value)
    titul = titulo.value
    codigo = cutter.value
    classif = classi.value
    exemp = exemp.value
    volume_n = vol.value
    if(not volume_n):
        volume_n = '0'
    if(not exemp):
        exemp = '1'

    exemp = int(exemp)

    logic.novo_registro_func(nome, titul, codigo, classif, exemp, volume_n, biblivre)
    #existentes(biblivre)

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


                login_error_label = ui.label('').style(f'color:rgb(255, 0, 0); font-size: 90%; font-weight: 500')
                ui.button('Entrar', on_click=lambda v, user=user, senha=senha, label=login_error_label: login(label, user, senha))

                ui.label('Utilize as mesmas credencias da plataforma Biblivre').style(f'color:rgb(81, 84, 90); font-size: 80%; font-weight: 500')

def home():

    global relacao_codigo_nome
    global codigos

    main.clear()
     
    #validation={"Por favor preencha esse campo." : lambda v : v != None}

    with main:
        #show_background()   

        with ui.row().classes('w-full items-center'):  
            #ui.button('Sair', on_click=lambda: login())

            with ui.card().classes('w-full items-center no-shadow border-[5px]') \
                .style('width: 100%; heigh: 100%; margin: 0; pagging: 0').tight():


                ui.label('Atalho para catalogação de livros')\
                    .style('color: #6E93D6; font-size: 200%; font-weight: 500; padding: 50px')

                rows = ui.row()
                results_card = ui.scroll_area().classes('no-shadow border-[1px]')

                with rows: 

                    with ui.card(align_items='center').classes('no-shadow no-borde'):
                        with ui.row():
                            autor = ui.input(label="Autor").props('clearable').style("width: 25vh")
                            titulo = ui.input(label="Título").props('clearable').style("width: 25vh")
                            exemplares = ui.number(label="Exemplares", min=1,validation={"Insira um número": lambda v: (type(v) == float) or (type(v) == float) or v == None}).style("width: 25vh")
                    
                        with ui.row():       
                            with ui.card().classes('no-shadow').tight():
                                selected = ui.label().style('color:rgb(81, 84, 90); font-size: 70%; font-weight: 500')
                                classi = ui.input(label="Classificação do livro",placeholder="028.5, 869.0(81), etc",
                                                        autocomplete=codigos, on_change=lambda v, 
                                                        label=selected: change_selected_classificacao(label, v.value)).props('clearable') \
                                                        .style("width: 25vh")
                                
                            with ui.card().classes('no-shadow').tight():
                                cutter = ui.input(label="Código Cutter").props('clearable').style("width: 25vh")
                                
                            volume = ui.number(label="Volume", min=1, validation={"Insira um número": lambda v: (type(v) == float) or (type(v) == float) or v == None}).style("width: 25vh")
                                

                    #with ui.card(align_items='end').classes('no-shadow no-border'):
                        with ui.row():
                            ui.button('Registrar', on_click=lambda b, autor=autor, titulo=titulo, exemp=exemplares, 
                                      classi=classi, cutter=cutter, vol=volume: registrar(autor, titulo, exemp, classi, cutter, vol))\
                                        .style("width: 25vh; height: 10vh;").bind_enabled_from(autor, 'error', lambda error: autor.value and 
                                                                                titulo.value and cutter.value and exemplares.value and classi.value) \
                                        .tooltip("Preehcha os campos obrigatórios.")
                            
                            ui.button('Procurar', on_click=lambda b, card=results_card, autor=autor, titulo=titulo, exemp=exemplares, 
                                      classi=classi, cutter=cutter, vol=volume: procurar(results_card, autor, titulo)).style("width: 25vh; height: 10vh;")\
                                      .bind_enabled_from(autor, 'error', lambda error: autor.value or titulo.value)\
                                      .tooltip("Preehcha autor ou título para pesquisar")
                            
                            ui.button('Limpar', on_click=lambda b, card=results_card, autor=autor, titulo=titulo, exemp=exemplares, 
                                      classi=classi, cutter=cutter, vol=volume: limpar(card, autor, titulo, exemp, classi, cutter, vol)).style("width: 25vh; height: 10vh;")
                            
                            ui.button('Procurar cutter on-line').tooltip('Utilizando o site www.tabelacutter.com').style("width: 25vh; height: 10vh; font-size: 80%")

main = ui.column().classes('w-full items-center no-border').style('margin: 0; padding: 0')


if not logged:
    login_page()
else:
    home()


first_run = True

if first_run:
#    biblivre = logic.inicia_driver()
    first_run = False

#bibliografia_page = logic.login("admin", "admin", biblivre)
home()

ui.run(port=5555, title="Catalogação")#, reload=False) #, native=True, reload=False)    

#biblivre.quit()