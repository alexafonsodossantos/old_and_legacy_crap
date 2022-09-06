from threading import Thread
import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
from random import randint
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
PATH = "C:\Program Files (x86)\chromedriver.exe"

accounts = [["conta1", "senha1"],
            ["conta2", "senha2"],
            ]

accounts2 = [["conta1", "senha1"],
            ["conta2", "senha2"],
            ]

random.shuffle(accounts)
random.shuffle(accounts2)


from datetime import datetime

BAD_ACCOUNTS = []

chrome_opt = webdriver.ChromeOptions()
chrome_opt.add_argument('--disable-gpu')
chrome_options.add_argument("--window-size=680,780")
def writelog(msg, account):
    now = datetime.now()
    log = open("log.txt", "a")
    log.write(str(now) + " ; " + msg + " ; " + account + "\n")
    log.close()

def Skip(driver):
    #skipSave = driver.find_element_by_xpath("//*[contains(text(), 'Agora não')]").click()
    time.sleep(4.5)
    skipNotifications = driver.find_element_by_xpath("//*[contains(text(), 'Agora não')]").click()

def GNI_Login(driver, gni_usr, gni_pass):
    driver.get("https://www.ganharnoinsta.com/painel/")
    searchUsername = driver.find_element_by_id('uname')
    searchUsername.send_keys(gni_usr)
    time.sleep(2)
    searchPassword = driver.find_element_by_id('pwd')
    searchPassword.send_keys(gni_pass)
    time.sleep(2)
    login = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div/form/div/div[3]/button').click()
    time.sleep(2)

def GNI_SetAccount(driver, account):
    driver.get("https://www.ganharnoinsta.com/painel/?pagina=sistema")
    time.sleep(1.5)
    igaccount = driver.find_element_by_id('contaig').click()
    igaccount = driver.find_element_by_name('contaig').send_keys(account)
    igaccount = driver.find_element_by_name('contaig').send_keys(Keys.RETURN)

def GNI_StartSystem(driver):
    start = driver.find_element_by_id('btn_iniciar').click()
    time.sleep(1)

def INSTAGRAM_Login(driver, user, password):
    driver.get("https://www.instagram.com")
    time.sleep(1.5)
    searchUsername = driver.find_element_by_name('username')
    searchUsername.send_keys(user)
    time.sleep(1)
    searchPassword = driver.find_element_by_name('password')
    searchPassword.send_keys(password)
    time.sleep(1)
    searchPassword.send_keys(Keys.RETURN)

def main(accounts, GNI_USR, GNI_PASS, x, thread):
            while True:

                print("Laço principal.")
                
                # Accounts loop
                for each in accounts:
                    try:
                        os.system('cls')
                        print('Contas cadastradas: ')
                        for a in accounts:
                                print("-- "+ a[0])
                        print('Contas que receberam block action: ')
                        for a in BAD_ACCOUNTS:
                                print("-- "+ a[0])

                        print('Inicializando o driver...')
                        driver = webdriver.Chrome(PATH, options=chrome_options)
                        if thread == 1:
                            driver.set_window_position(0, 0, windowHandle ='current')
                        elif thread ==2:
                            driver.set_window_position(680, 0, windowHandle ='current')
                        print('Fazendo login em ganharnoinsta...')
                        GNI_Login(driver, "Seu email ganharnoinsta", "Sua senha ganharnoinsta")
                        print('Aguardando (3)')
                        time.sleep(3)
                        print('Fazendo login no instagram com a conta: ' + each[0])
                        INSTAGRAM_Login(driver, each[0], each[1])
                        time.sleep(2.5)
                        writelog("Login no instagram", each[0])
                        try:
                            block_action =  driver.find_element_by_xpath("//*[contains(text(), 'Confirme que é você fazendo login')]")
                            BLOCKED_ACCOUNT_AT_LOGIN = 1
                        except:
                            BLOCKED_ACCOUNT_AT_LOGIN = 0

                        if BLOCKED_ACCOUNT_AT_LOGIN == 1:
                            print('A conta ' + each[0] +' recebeu block action! removendo da lista de contas...')
                            BAD_ACCOUNTS.append(each)
                            accounts.remove(each)
                            writelog("Block Action", each[0])
                            driver.quit()
                            break
                        else:
                            pass

                        Skip(driver)
                        time.sleep(1.5)
                        print('Selecionando a conta no painel')
                        GNI_SetAccount(driver, each[0])
                        time.sleep(2.5)
                        print('Iniciando o sistema!')
                        GNI_StartSystem(driver)
                        time.sleep(1.5)
                        i = 0
                        TASK_TYPE = 0
                        while i < 20:
                            
                            time.sleep(2.5)

                            try:
                                time.sleep(1.5)
                                a =  driver.find_element_by_xpath("//*[contains(text(), 'Seguir Perfil')]")
                                TASK_TYPE = 0
                            except:
                                try:
                                    time.sleep(1.5)
                                    b = driver.find_element_by_xpath("//*[contains(text(), 'Curtir Publicação')]")
                                    TASK_TYPE = 1
                                except:
                                    try:
                                        time.sleep(1.5)
                                        c = driver.find_element_by_xpath("//*[contains(text(), 'Tarefas Esgotadas')]")
                                        TASK_TYPE = 2
                                    except:
                                        TASK_TYPE = 3
                            
                            if TASK_TYPE == 0:
                                print('Tipo de tarefa: seguir.')
                                driver.switch_to.window(driver.window_handles[0])
                                print('Acessando perfil...')
                                time.sleep(1.5)
                                opentask = driver.find_element_by_id("btn-acessar").click()
                                time.sleep(1.5)
                                driver.switch_to.window(driver.window_handles[1])
                                time.sleep(1.5)
                                print('Realizando tarefa...')
                                try:
                                    follow = driver.find_element_by_xpath("//*[contains(text(), 'Seguir')]").click()
                                    time.sleep(2.5)
                                except:
                                    print('Não foi possível seguir a conta.')
                                finally:
                                    try:
                                        block_action = driver.find_element_by_xpath("//*[contains(text(), 'Tente novamente mais tarde')]")
                                        ACCOUNT_BLOCKED = 1
                                    except:
                                        ACCOUNT_BLOCKED = 0
                                
                                if ACCOUNT_BLOCKED == 1:
                                    print('A conta' + each[0] +' recebeu block action! removendo da lista de contas...')
                                    BAD_ACCOUNTS.append(each)
                                    accounts.remove(each)
                                    writelog("Block action!", each[0])
                                    driver.quit()
                                    break
                                else:
                                    pass
                                time.sleep(2.5)
                                driver.close()
                                time.sleep(1.5)
                                driver.switch_to.window(driver.window_handles[0])
                                time.sleep(2.5)
                                print('Confirmando tarefa...')
                                try:
                                    time.sleep(2.5)
                                    confirm = driver.find_element_by_id("btn-confirmar").click()
                                except:
                                    print('Não foi possível concluir a ação.')
                                    break
                                time.sleep(1.5)
                                i = i + 1
                                
                                print("Tarefas executadas com a conta " + each[0] + ": " + str(i))
                                writelog("Tarefa concluída", each[0])
                                time.sleep(2.5)
                                os.system('cls')
                                print('Contas cadastradas: ')
                                for a in accounts:
                                    print("-- "+ a[0])
                                print('Contas que receberam block action: ')
                                for a in BAD_ACCOUNTS:
                                    print(a[0])

                            elif TASK_TYPE == 1:
                                print('Tipo de tarefa: curtir')
                                driver.switch_to.window(driver.window_handles[0])
                                print('Acessando perfil...')
                                opentask = driver.find_element_by_id('btn-acessar').click()
                                time.sleep(1.5)
                                print('Realizando tarefa...')
                                driver.switch_to.window(driver.window_handles[1])
                                firstLike = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button").click()
                                time.sleep(1.5)
                                driver.close()
                                print('Confirmando tarefa...')
                                driver.switch_to.window(driver.window_handles[0])
                                time.sleep(1.5)
                                confirm = driver.find_element_by_xpath("//*[contains(text(), 'Confirmar Ação')]").click()
                                time.sleep(1.5)
                                i = i + 1
                                time.sleep(2.5)
                                print("Tarefas executadas com a conta " + each[0] + ": " + str(i))
                                writelog("Tarefa concluída", each[0])
                                time.sleep(2.5)
                            elif TASK_TYPE == 2:
                                print("Sem tarefas para esse perfil, mudando de perfil.")
                                driver.quit()
                                writelog("Sem tarefas para o perfil.", each[0])
                                break
                            elif TASK_TYPE == 3:
                                print('Houve um erro ao obter tarefas.')
                                driver.quit()
                                break
                    except:
                        print('Erro inesperado.')
                        driver.quit()
                        writelog("Erro na execução.", "SYSTEM")
                        continue

GNI_USR = "Seu email ganharnoinsta"
GNI_PASS = "Sua senha ganharnoinsta"
random.shuffle(accounts)
random.shuffle(accounts2)

class Th_1(Thread):
    def _init_ (self):
            Thread._init_(self)

    def run(self):
            main(accounts, GNI_USR, GNI_PASS, 20, 1)

class Th_2(Thread):
    def _init_ (self):
        Thread._init_(self)

    def run(self):
        main(accounts2, GNI_USR, GNI_PASS, 20, 2)



a = Th_1()
b = Th_2()
a.start()
time.sleep(3)
b.start()
