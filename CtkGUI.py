from customtkinter import *
import tkinter.ttk as ttk
import logic
from PIL import ImageTk
from sys import exit
from time import sleep

def pegaCodigo(cutter):

    codigo = ''

    if(len(autor_input.get()) > 1):
        nome = logic.FormataNome(autor_input.get()).split(',')[0]
        codigo = logic.CodigoAutor(nome, cutter)

    return codigo

def evento_nome(cutter):
    pegaCodigo(cutter)

def livroCodigo(codigo):

    titulo = livro_input.get()

    if(len(titulo) > 1):
        codigo = logic.CodigoLivro(codigo, titulo)

    return codigo

def muda_input(atual):

    generos = {
    'Literatura Infantojuvenil' : '028.5',
    'Literatura Infantojuvenil (Poesia)' : '028.5-1',
    'Literatura Infantojuvenil (Teatro)'  : '028.5-2',
    'Literatura Infantojuvenil (Conto)' : '028.5-34',
    'Literatura Infantojuvenil (Crônicas)' : '028.5-94',

    'História em Quadrinhos' : '741.5',

    'Literatura Brasileira' :  '869.0(81)',
    'Literatura Brasileira (Poesia)' : '869.0(81)-1',
    'Literatura Brasileira (Teatro)' : '869.0(81)-2',
    'Literatura Brasileira (Sátira)' : '869.0(81)-7',
    'Literatura Brasileira (Novela)' : '869.0(81)-32',
    'Literatura Brasileira (Conto)' : '869.0(81)-34',
    'Literatura Brasileira (Crônicas)' : '869.0(81)-94',

    'Literatura Estrangeira' : '810/890',

    'Gramática' : '801.5',
    'Língua Inglesa' : '802.0',
    'Língua Espanhola' : '806.0',
    'Língual Portuguesa Didático' : '806.9',
    'Literatura Geral (Didático)' : '82',
    'Geografia (Didático)' : '911',
    'Biografia' : '929',
    'Histótia' : '930',

    'História do Rio Grande do Sul' : '981.65',
    'Literatura Riograndense' :  '869.0(816.5)',
    'Literatura Riograndense (Poesia)' : '869.0(816.5)-1',
    'Literatura Riograndense (Teatro)' : '869.0(816.5)-2',
    'Literatura Riograndense (Sátira)' : '869.0(816.5)-7',
    'Literatura Riograndense (Novela)' : '869.0(816.5)-32',
    'Literatura Riograndense (Conto)' : '869.0(816.5)-34',
    'Literatura Riograndense (Crônicas)' : '869.0(816.5)-94',
    }

    posic = generos.get(atual.get())

    classificacao_input.delete(0, "end")
    classificacao_input.insert('0', posic)

def revisarFunc(cutter):

    nome = ''
    global g_codigo
    global g_autor

    codigo = g_codigo
    
    if(len(autor_input.get()) >= 1):
        nome = logic.FormataNome(autor_input.get())
        g_autor = nome

    if(nome != autor.cget("text").split(':')[1][1:]):
        codigo = pegaCodigo(cutter)
        g_codigo = codigo

    volume = volume_input.get()
    exemplares = exemplares_input.get()
    if(exemplares == ''):
        exemplares = '1'
    if(int(exemplares) <= 0):
        exemplares = '1'

    local_aux = 'Localização: ' + classificacao_input.get() + ' ' + livroCodigo(codigo)

    if(volume != '' and int(volume) >= 1):
        local_aux = local_aux + ' ' + str(volume)

    titulo.configure(text= 'Título: ' + livro_input.get())
    autor.configure(text= 'Autor: ' + nome)
    local.configure(text = local_aux)
    exemp.configure(text='Exemplares: ' + exemplares)

def enviarFunc(driver, cutter):
    
    global g_codigo
    global g_autor
    global bibliografia

    driver.get(bibliografia)
    
    revisarFunc(cutter)

    nome = g_autor
    titul = livro_input.get()
    codigo = livroCodigo(g_codigo)
    classif = classificacao_input.get()
    exemp = exemplares_input.get()
    volume_n = volume_input.get()
    if(volume_n == ''):
        volume_n = '0'

    logic.novo_registro_func(nome, titul, codigo, classif, exemp, volume_n, driver)

    Existentes(driver)

def limparFunc():

    autor_input.delete(0, "end")
    autor_input.insert('0', '')

    livro_input.delete(0, "end")
    livro_input.insert('0', '')

    classificacao_input.delete(0, "end")
    classificacao_input.insert('0', '')
    atual.set("Classificações padrões...")

    exemplares_input.delete(0, "end")
    exemplares_input.insert('0', '1')

    volume_input.delete(0, "end")
    volume_input.insert('0', '')

    titulo.configure(text= 'Título: ')
    autor.configure(text= 'Autor: ')
    local.configure(text = 'Localização: ')
    exemp.configure(text='Exemplares: ')

def login_bib(driver):

    global bibliografia

    user = usuario_input.get()
    senha = senha_input.get()

    bibliografia = logic.login(user, senha, driver)
    
    if (bibliografia != ''):
        login.destroy()
        window.deiconify()
    else:
        erro = CTkLabel(login_info, text="Usuário ou senha inválidos", font=CTkFont("Calibri", 16, weight='bold'), text_color='#1f1f1f',
                        fg_color='#ff78ac', corner_radius=4)
        erro.pack(ipadx=5, ipady=5, pady=(5, 0))
        senha_input.delete(0, "end")
        senha_input.insert('0', '')

def fechar():
    login.destroy()
    window.destroy()
    exit()

def NovoExemplar(driver, index, pesquisa):

    driver.get(bibliografia)

    logic.NovoExemplar(driver, index, pesquisa)

    Existentes(driver)
    

def Existentes(driver):

    sleep(0.5)

    try:

        while True:
            buttons_frame_labels[0].destroy()
            buttons_frame_buttons[0].destroy()

            buttons_frame_buttons.pop(0)
            buttons_frame_labels.pop(0)

    except IndexError:
        pass

    try:
        buttons_frame_item[0].pack_forget()
        buttons_frame_item[0].destroy()
        buttons_frame_item.pop(0)
    except:
        pass

    buttons_frame_item.append(CTkScrollableFrame(results_frame, fg_color='#ffffff'))
    buttons_frame_item[0].pack(fill = BOTH, expand = False)

    results_label = CTkLabel(buttons_frame_item[0], text='', font=CTkFont("Calibri", 16, weight='bold'), text_color='#1f1f1f')
    results_label.pack() 



    nome = f'{autor_input.get()} {livro_input.get()}'

    driver.get(bibliografia)    
    number = logic.ResultsSearch(nome, driver)

    if(nome != '' and number != 0):
        
        results_label.configure(text=f'{number} resultado(s)')

        for i in range(1, number + 1):
            buttons_frame_labels.append(CTkLabel(buttons_frame_item[0], text=logic.GetTextIndex(driver, i), font=CTkFont("Calibri", 14, weight='bold'), text_color='#1f1f1f'))
            buttons_frame_labels[i - 1].pack()

            buttons_frame_buttons.append(CTkButton(buttons_frame_item[0], text=f'NOVO EXEMPLAR', border_width=2, corner_radius=3, border_color='black',
                   text_color='black', fg_color='#d1daff', font=CTkFont("Calibri", 12, weight='bold'),
                    command=lambda d=driver, i=i, s=nome: NovoExemplar(d, i, s)))
            buttons_frame_buttons[i-1].pack(pady=(5,10))

    else:
        results_label.configure(text=f'0 resultado(s)')

#------------------------

window = CTk()
window.title("Facilitador de Catalogação")

window.resizable(False, False)

ciep = ImageTk.PhotoImage(file='./ciep.png')
window.wm_iconbitmap()
window.iconphoto(False, ciep)

g_codigo = ''
g_autor = ''

cutter = ''
driver = ''
bibliografia = ''

search = '' # Last searched item

cutter = logic.inicia_cutter()
driver = logic.inicia_driver()

login = CTkToplevel()
login.title('Login')
login.resizable(False, False)

login.wm_iconbitmap()
login.iconphoto(False, ciep)

login_info = CTkFrame(login)
login_info.pack(ipadx=10, ipady=10)

usuario = CTkLabel(login_info, text="Nome de usuario no Biblivre: ", font=CTkFont("Calibri", 16, weight='bold'), text_color='#1f1f1f')
usuario.pack() 

usuario_input = CTkEntry(login_info, width=230, corner_radius=3,
                       border_color='black', border_width=0, fg_color='#e8edff')
usuario_input.pack()

senha = CTkLabel(login_info, text="Senha no Biblivre: ", font=CTkFont("Calibri", 16, weight='bold'), text_color='#1f1f1f')
senha.pack() 

senha_input = CTkEntry(login_info, show="*", width=230, corner_radius=3,
                       border_color='black', border_width=0, fg_color='#e8edff')
senha_input.bind('<Return>', lambda event, d=driver: login_bib(d))

senha_input.pack(pady=(0,10))

entrar = CTkButton(login_info, text='Entrar', border_width=2, corner_radius=3, border_color='black',
                   text_color='black', fg_color='#d1daff', font=CTkFont("Calibri", 16, weight='bold'),
                    command= lambda d=driver: login_bib(d))
entrar.pack()

cancelar = CTkButton(login_info, text='Cancelar', border_width=2, corner_radius=3, border_color='black',
                   text_color='black', fg_color='#d1daff', font=CTkFont("Calibri", 16, weight='bold'),
                    command= lambda : fechar())
cancelar.pack(pady=5)


mega_frame = CTkFrame(window, corner_radius=0)
mega_frame.pack()

#------------------------------

preenchivel = CTkFrame(mega_frame, fg_color='#d1daff', corner_radius=0)
preenchivel.pack(side=LEFT, ipadx=10, ipady=10, padx=(0, 10), anchor="w")

autor_frame = CTkFrame(preenchivel, fg_color='#ffffff', corner_radius=3)
autor_frame.pack(pady=(10, 15), ipadx=10, ipady=5)

autor_label = CTkLabel(autor_frame, text="Nome do autor: ", font=CTkFont("Calibri", 16, weight='bold'), text_color='#1f1f1f')
autor_label.pack() 

autor_input = CTkEntry(autor_frame, width=230, corner_radius=3, placeholder_text="ex: Octavia Butler",
                       border_color='black', border_width=0, fg_color='#e8edff', placeholder_text_color='#5c5c5c')
autor_input.pack()
autor_input.bind('<Return>', lambda event, d=driver: Existentes(d))

#-------------------------------

#-------------------------------

livro_frame = CTkFrame(preenchivel, fg_color='#ffffff', corner_radius=3)
livro_frame.pack(pady=(0, 15), ipadx=10, ipady=5)

livro_label = CTkLabel(livro_frame, text="Título do Livro: ", font=CTkFont("Calibri", 16, weight='bold'), text_color='#1f1f1f')
livro_label.pack() #.place(x=100, y=80)

livro_input = CTkEntry(livro_frame, width=230, corner_radius=3, placeholder_text="ex: Kindred: Laços de sangue",
                       border_color='black', border_width=0, fg_color='#e8edff', placeholder_text_color='#5c5c5c')
livro_input.pack() #.place(x=200, y=80)
#livro_input.bind("<Return>", lambda event: livroCodigo())
livro_input.bind('<Return>', lambda event, d=driver: Existentes(d)) #Verify if exists

#-------------------------------


#----------------------------------
classificacao_frame = CTkFrame(preenchivel, fg_color='#ffffff', corner_radius=3)
classificacao_frame.pack(pady=(0, 10), ipadx=10, ipady=5)

classificacao_label = CTkLabel(classificacao_frame, text="Classificação do livro: ", font=CTkFont("Calibri", 16, weight='bold'), text_color='#1f1f1f')
classificacao_label.pack() #.place(x=70, y=110)

classificacao_input = CTkEntry(classificacao_frame, width=230, corner_radius=3, placeholder_text="ex: 028.5, 869.0(81), etc...",
                       border_color='black', border_width=0, fg_color='#e8edff', placeholder_text_color='#5c5c5c')
classificacao_input.pack() #.place(x=200, y=110)
classificacao_input.bind("<Return>", lambda event: atual.set("Classificações padrões..."))
#or

generos = [
    'Literatura Infantojuvenil',
    'Literatura Infantojuvenil (Poesia)',
    'Literatura Infantojuvenil (Teatro)',
    'Literatura Infantojuvenil (Conto)',
    'Literatura Infantojuvenil (Crônicas)',

    'História em Quadrinhos',

    'Literatura Brasileira',
    'Literatura Brasileira (Poesia)',
    'Literatura Brasileira (Teatro)',
    'Literatura Brasileira (Sátira)',
    'Literatura Brasileira (Novela)',
    'Literatura Brasileira (Conto)',
    'Literatura Brasileira (Crônicas)',

    'Literatura Estrangeira',
    'Gramática',
    'Língua Inglesa',
    'Língua Espanhola',
    'Língual Portuguesa Didático',
    'Literatura Geral (Didático)',
    'Geografia (Didático)',
    'Biografia',
    'Histótia',

    'História do Rio Grande do Sul',
    'Literatura Riograndense',
    'Literatura Riograndense (Poesia)',
    'Literatura Riograndense (Teatro)',
    'Literatura Riograndense (Sátira)',
    'Literatura Riograndense (Novela)',
    'Literatura Riograndense (Conto)',
    'Literatura Riograndense (Crônicas)'
]

atual = StringVar()
atual.set("Classificações padrões...")

style= ttk.Style()
style.theme_use('clam')
style.configure("TCombobox", fieldbackground= "white", background="#d1daff",
                arrowcolor='black', borderwidth=50, bordercolor='gray',
                padding=5)

classificacao_menu = ttk.Combobox(classificacao_frame, textvariable=atual, width=32) #*generos, command = lambda a=atual: muda_input(atual))
classificacao_menu['values'] = generos
classificacao_menu.bind('<<ComboboxSelected>>', lambda event, a=atual: muda_input(a))

classificacao_menu.pack(pady=2) #.place(x=200, y=135)
#----------------------------------------------

exemplares_frame = CTkFrame(preenchivel, fg_color='#ffffff', corner_radius=3)
exemplares_frame.pack(side=LEFT, padx=(30,0), ipadx=10, ipady=5)

exemplares_label = CTkLabel(exemplares_frame, text="Exemplares:", font=CTkFont("Calibri", 16, weight='bold'), text_color='#1f1f1f')
exemplares_label.pack() #.place(x=120, y=170)

exemplares_input = CTkEntry(exemplares_frame, width=60, corner_radius=3, border_color='black', 
                        border_width=0, fg_color='#e8edff')
exemplares_input.pack() #.place(x=200, y=170)
exemplares_input.insert(0, '1')

volume_frame = CTkFrame(preenchivel, fg_color='#ffffff', corner_radius=3)
volume_frame.pack(side=RIGHT, padx=(0,30), ipadx=10, ipady=5)

volume_label = CTkLabel(volume_frame, text="Volume:", font=CTkFont("Calibri", 16, weight='bold'), text_color='#1f1f1f')
volume_label.pack()

volume_input = CTkEntry(volume_frame, width=60, corner_radius=3, border_color='black', 
                        border_width=0, fg_color='#e8edff')
volume_input.pack()

#--------------------------

revisao_frame = CTkFrame(mega_frame, fg_color='transparent')
revisao_frame.pack(side=RIGHT, ipadx=30, ipady=10, padx=(0, 10), anchor="c")

info_frame = CTkFrame(revisao_frame, fg_color='#d9d9d9', corner_radius=4, border_width=2, border_color='black')
info_frame.pack(ipadx=10, pady=(10, 20))

titulo = CTkLabel(info_frame, text="Título:", width=200, anchor='w', wraplength=200, justify='left',
                    font=CTkFont("Calibri", 15, slant='italic'))
titulo.pack() #.place(x=200, y=300)

autor = CTkLabel(info_frame, text="Autor:", width=200, anchor='w', font=CTkFont("Calibri", 15, slant='italic'))
autor.pack() #.place(x=200, y=300)

local = CTkLabel(info_frame, text="Localização:", width=200, anchor='w', font=CTkFont("Calibri", 15, slant='italic'))
local.pack()

exemp = CTkLabel(info_frame, text="Exemplares:", width=200, anchor='w', font=CTkFont("Calibri", 15, slant='italic'))
exemp.pack()

revisar = CTkButton(revisao_frame, text='REVISAR', border_width=2, corner_radius=3, border_color='black',
                   text_color='black', fg_color='#d1daff',
                     command= lambda c=cutter: revisarFunc(c))

revisar.pack(pady=6, ipadx=3, ipady=3)

limpar = CTkButton(revisao_frame, text='LIMPAR', border_width=2, corner_radius=3, border_color='black',
                   text_color='black', fg_color='#d1daff',
                    command= lambda d=driver: limparFunc())

limpar.pack(pady=6, ipadx=3, ipady=3)

pesquisar = CTkButton(revisao_frame, text='PESQUISAR', border_width=2, corner_radius=3, border_color='black',
                   text_color='black', fg_color='#d1daff', font=CTkFont("Calibri", 16, weight='bold'),
                    command= lambda d=driver: Existentes(d))

pesquisar.pack(pady=6, ipadx=3, ipady=3)

enviar = CTkButton(revisao_frame, text='ENVIAR', border_width=2, corner_radius=3, border_color='black',
                   text_color='black', fg_color='#d1daff', font=CTkFont("Calibri", 16, weight='bold'),
                    command= lambda d=driver, c=cutter: enviarFunc(d, c))

enviar.pack(pady=6, ipadx=3, ipady=3)

#-----------------------------------------------

results_frame = CTkFrame(window, fg_color='#ffffff')
results_frame.pack(fill = BOTH, expand = True)


buttons_frame_item = []

buttons_frame_labels = []
buttons_frame_buttons = []

#.configure(text='New Text')

window.withdraw()
window.mainloop()

driver.quit()
cutter.quit()

exit(0)