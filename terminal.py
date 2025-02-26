from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.chrome.service import Service
from time import sleep


# from webdriver_manager.chrome import ChromeDriverManager

def FormataNome(nome):

    aux = nome.split(' ')

    if(len(aux) == 1):
        return nome

    final = len(aux) - 1

    inicio = aux[final]
    del(aux[final])

    resto = " ".join(aux)

    novo_nome = inicio + ', ' + resto

    return novo_nome

def CodigoAutor(nome, cutter):

    cutter.get('https://www.tabelacutter.com/?e=' + nome.split(',')[0] +'&c=')
    codigo = cutter.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div/form/div[1]/div/span[2]').text

    return codigo

def CodigoLivro(codigo, titulo):
    
    aux = titulo.lower().split(' ')

    if(aux[0] == 'a' or aux[0] == 'o'):
        codigo = codigo + aux[1][0]

    else:
        codigo = codigo + aux[0][0]

    return codigo


#options = Options()
#options.add_experimental_option("detach", True)


def inicia_cutter():

    options = Options()
    options.add_argument("--headless=new")

    service_cutter = Service(ChromeDriverManager().install())
    cutter = webdriver.Chrome(service=service_cutter, options=options)
    return cutter

def inicia_driver():

    options = Options()
    options.add_argument("--headless=new")

    service_driver = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service_driver, options=options)

    # uncomment this line and comment the above to see the browser
    #driver = webdriver.Chrome()

    return driver


#driver.implicitly_wait(0.5)


### user = input('Usuario: ')
### senha = input('Senha: ')

def login(user, senha, driver):

    driver.get("http://localhost/Biblivre5/")

    username = driver.find_element(by=By.NAME, value="username")
    password = driver.find_element(by=By.NAME, value="password")

    username.send_keys(user)
    password.send_keys(senha)

    entrar = driver.find_element(By.XPATH, '/html/body/form/div[1]/div[6]/ul/li[4]/button')
    entrar.click()

    try:
        ret = driver.find_element(By.XPATH, '/html/body/form/div[1]/div[6]/ul/li[3]/ul/li[1]/a').get_attribute('href')
        return ret
    except:
        return ''

def bib(driver):

    return driver.find_element(By.XPATH, '/html/body/form/div[1]/div[6]/ul/li[3]/ul/li[1]/a').get_attribute('href')


def main_loop(driver, cutter):

    continuar = 's'
    bibliografia = bib(driver)
    
    while(continuar == 's'):
        
        driver.get(bibliografia)

        classif = input('Qual a classificação? ')
        nome = FormataNome(input('Qual o nome do autor? '))
        #codigo = input('Qual o código do autor? ')
        titul = input('Qual o titulo do livro? ')
        exemp = input('Quantos exemplares tem o livro? ')

        codigo = CodigoAutor(nome, titul, cutter)
        
        novo_registro = driver.find_element(By.XPATH, '//*[@id="new_record_button"]')
        novo_registro.click()

        classificacao = driver.find_element(By.XPATH, '/html/body/form/div[3]/div[2]/div[2]/div[1]/div[5]/div[2]/div[2]/div/div[11]/fieldset/div[2]/div[1]/div[2]/input')
        classificacao.send_keys(classif)

        codigo_autor = driver.find_element(By.XPATH, '/html/body/form/div[3]/div[2]/div[2]/div[1]/div[5]/div[2]/div[2]/div/div[11]/fieldset/div[2]/div[2]/div[2]/input')
        codigo_autor.send_keys(codigo)

        #volume = driver.find_element(By.XPATH, '/html/body/form/div[3]/div[2]/div[2]/div[1]/div[5]/div[2]/div[2]/div/div[11]/fieldset/div[2]/div[3]/div[2]/input')

        nome_autor = driver.find_element(By.XPATH, '/html/body/form/div[3]/div[2]/div[2]/div[1]/div[5]/div[2]/div[2]/div/div[13]/fieldset/div[2]/div[2]/div[2]/input')
        nome_autor.send_keys(nome)

        titulo = driver.find_element(By.XPATH, '/html/body/form/div[3]/div[2]/div[2]/div[1]/div[5]/div[2]/div[2]/div/div[20]/fieldset/div[2]/div[3]/div[2]/input')
        titulo.send_keys(titul)

        exemplares = driver.find_element(By.XPATH, '/html/body/form/div[3]/div[2]/div[2]/div[1]/div[5]/div[2]/div[4]/div/fieldset/div[1]/div[2]/input')
        exemplares.send_keys(exemp)

        salvar_registro = driver.find_element(By.XPATH, '/html/body/form/div[3]/div[2]/div[2]/div[1]/div[5]/div[3]/div[2]/a[1]')
        salvar_registro.click()

        continuar = input('Deseja Continuar (s/n)? ')

def novo_registro_func(nome, titul, codigo, classif, exemp, volume_n, driver):
        
    novo_registro = driver.find_element(By.XPATH, '//*[@id="new_record_button"]')
    novo_registro.click()

    classificacao = driver.find_element(By.XPATH, '/html/body/form/div[3]/div[2]/div[2]/div[1]/div[5]/div[2]/div[2]/div/div[11]/fieldset/div[2]/div[1]/div[2]/input')
    classificacao.send_keys(classif)

    codigo_autor = driver.find_element(By.XPATH, '/html/body/form/div[3]/div[2]/div[2]/div[1]/div[5]/div[2]/div[2]/div/div[11]/fieldset/div[2]/div[2]/div[2]/input')
    codigo_autor.send_keys(codigo)

    if(int(volume_n) > 1):
        volume = driver.find_element(By.XPATH, '/html/body/form/div[3]/div[2]/div[2]/div[1]/div[5]/div[2]/div[2]/div/div[11]/fieldset/div[2]/div[3]/div[2]/input')
        volume.send_keys(volume_n)

    nome_autor = driver.find_element(By.XPATH, '/html/body/form/div[3]/div[2]/div[2]/div[1]/div[5]/div[2]/div[2]/div/div[13]/fieldset/div[2]/div[2]/div[2]/input')
    nome_autor.send_keys(nome)

    titulo = driver.find_element(By.XPATH, '/html/body/form/div[3]/div[2]/div[2]/div[1]/div[5]/div[2]/div[2]/div/div[20]/fieldset/div[2]/div[3]/div[2]/input')
    titulo.send_keys(titul)

    exemplares = driver.find_element(By.XPATH, '/html/body/form/div[3]/div[2]/div[2]/div[1]/div[5]/div[2]/div[4]/div/fieldset/div[1]/div[2]/input')
    exemplares.send_keys(exemp)

    salvar_registro = driver.find_element(By.XPATH, '/html/body/form/div[3]/div[2]/div[2]/div[1]/div[5]/div[3]/div[2]/a[1]')
    salvar_registro.click()    

def ResultsSearch(titulo, driver):

    search = driver.find_element(By.XPATH, '/html/body/form/div[3]/div[2]/div[2]/div[1]/div[6]/div[1]/div[1]/input')
    search.send_keys(titulo)

    send = driver.find_element(By.XPATH, '/html/body/form/div[3]/div[2]/div[2]/div[1]/div[6]/div[1]/div[2]/a')
    send.click()

    sleep(0.5)

    i = 0
    results = 0

    while i <= 20:

        i += 1

        try:    
            driver.find_element(By.XPATH, f'/html/body/form/div[3]/div[2]/div[2]/div[1]/div[8]/div[6]/div/div[{i}]/div[3]')
            results += 1
        
        except:

            try:
                driver.find_element(By.XPATH, f'/html/body/form/div[3]/div[2]/div[2]/div[1]/div[8]/div[6]/div/div')
                return results
            
            except:
                i = 32

    return results

def GetTextIndex(driver, index):

    titulo = 0
    autor = 0
    exemplares = -1

    try:
        result = driver.find_element(By.XPATH, f'/html/body/form/div[3]/div[2]/div[2]/div[1]/div[8]/div[6]/div/div[{index}]/div[3]').text
        result = result.split("\n")

        i = 0
        while i < len(result):

            if titulo != 0 and autor != 0:
                i = 100
            elif result[i].find('Título') != -1:
                titulo = i
            elif result[i].find('Autor') != -1:
                autor = i

            i += 1

        return f"{result[titulo]}\n{result[autor]}\n{result[exemplares]}"
    except:
        return 'Erro procurando valores'


def NovoExemplar(driver, index, pesquisa):

    search = driver.find_element(By.XPATH, '/html/body/form/div[3]/div[2]/div[2]/div[1]/div[6]/div[1]/div[1]/input')
    search.send_keys(pesquisa)

    print(f"Pesquisa: {pesquisa} | Index = {index}")

    send = driver.find_element(By.XPATH, '/html/body/form/div[3]/div[2]/div[2]/div[1]/div[6]/div[1]/div[2]/a')
    send.click()

    sleep(0.2)

    reg = driver.find_element(By.XPATH, f'/html/body/form/div[3]/div[2]/div[2]/div[1]/div[8]/div[6]/div/div[{index}]/div[2]/a[1]')
    reg.click()                        
                                        
    sleep(0.2)

    exemplares = driver.find_element(By.XPATH, '/html/body/form/div[3]/div[2]/div[2]/div[1]/div[5]/ul/li[4]')

    sleep(0.5)
    exemplares.click()
    
    i = 1
    ultimo_exemplar = ''

    try:
        while True:
            aux = driver.find_element(By.XPATH, f'/html/body/form/div[3]/div[2]/div[2]/div[2]/div[4]/div[2]/div/div[{i}]/div[2]/a[1]')
            ultimo_exemplar = aux
            i += 1
    except:
        pass
    
    ultimo_exemplar.click()

    sleep(1)
    editar = driver.find_element(By.XPATH, '/html/body/form/div[3]/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[1]/a[1]')
    sleep(1)
    editar.click()                         #/html/body/form/div[3]/div[2]/div[2]/div[1]/div[4]/div/div[1]/div[1]/a[1]
                                           #/html/body/form/div[3]/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[1]/a[1]
                                           #/html/body/form/div[3]/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[1]/a[1]
                                           #/html/body/form/div[3]/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[1]/a[1]
                                           #/html/body/form/div[3]/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[1]/a[1]
                                           #/html/body/form/div[3]/div[2]/div[2]/div[1]/div[4]/div/div[1]/div[1]/a[1] # Rad
                                           #/html/body/form/div[3]/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[1]/a[1]

    numero_exemplar = driver.find_element(By.XPATH, '/html/body/form/div[3]/div[2]/div[2]/div[2]/div[3]/div[2]/div[1]/div/div[1]/fieldset/div[2]/div[4]/div[2]/input')
    numero_exemplar.clear()
    numero_exemplar.send_keys(f"ex.{i}")

    tombo = driver.find_element(By.XPATH, '/html/body/form/div[3]/div[2]/div[2]/div[2]/div[3]/div[2]/div[1]/div/div[5]/fieldset/div[2]/div/div[2]/input')
    tombo.clear()
    
    save_as_new = driver.find_element(By.XPATH, '/html/body/form/div[3]/div[2]/div[2]/div[2]/div[3]/div[3]/div[1]/a[2]')
    save_as_new.click()
    
    #/html/body/form/div[3]/div[2]/div[2]/div[1]/div[8]/div[6]/div/div[1]
    #/html/body/form/div[3]/div[2]/div[2]/div[1]/div[8]/div[6]/div/div[1]/div[3]
    #/html/body/form/div[3]/div[2]/div[2]/div[1]/div[8]/div[6]/div/div