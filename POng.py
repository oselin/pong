#Pierfrancesco Oselin
#Mini gioco in multiplayer, connessione locale
#-------------------------------------------------------------------------------


import time, socket, pygame #Importazione delle librerie
from Tkinter import *
from pygame.locals import *


s = socket.socket()#Assegnazione del socket a una variabile
tipo=None#Variabile che indichera' se il giocatore fa da host o da client
t=Tk()#Assegnazione di Tkinter a una vaiabile
code=""#Variabile nella quale verra' assegnato l'ip da inserire


#Gioco---------------------------------------------------------------------------------------------------------------------------
def startGame():#definizione del gioco
    try:t.destroy()#Chiusura della finestra Tkinter. Messa in un try perche' alla seconda partita potrebbe dare errore
    except: pass#Siccome e' gia' stata chiusa
    #Impostazoni generali della schermata pygame
    pygame.init()#Inizializzazione della schermata pygame
    width, height = 800, 600#Assegnazione di valori per larghezza e altezza
    screen=pygame.display.set_mode((width, height))#costruzione della schermata con i valori precedenti
    pygame.display.set_caption('POng')#Assegnazione del titolo
    pygame.mouse.set_visible(False)#Il mouse non sara' visibile
    font=pygame.font.SysFont("Corbel",50)#assegnazione dei font per le scritte
                            
    #Impostazione variabili locali del gioco
    game=True#Variabile del gioco tale per cui se e' false si interrompera'
    enemy_x, enemy_y = (width-100)/2,  20#assegnazione di coordinate x e y all'avversario
    player_x, player_y = (width-100)/2, (height-20-30)#coordinate per il giocatore
    ball_x, ball_y = width/2, height/2#coordinate per la palla
    data=""#variabile in cui verranno inseriti i valori da ricevere
    radious=18#raggio della palla 
    player=pygame.draw.rect(screen, (255,255,255), Rect((player_x, player_y), (100,30)))#costruzione del giocatore
    enemy=pygame.draw.rect(screen, (255,255,255), Rect((enemy_x, enemy_y), (100,30)))#costruzione dell'avversario
    ball=pygame.draw.circle(screen, (255,255,255),(ball_x, ball_y),radious,0)#costruzione della palla
    pygame.display.flip()#aggiornamento della schermata
    moving_player=0#il giocatore non si muove (variabile che serve a far muovere il giocatore in modo fluido
    enemy_life, player_life=3 , 3#Vite di ogni giocatore
    block_ball=0#variabile che interrompe il movimento della palla
    stop_input=False#Variabile che ferma la ricezione di dati in input
    if tipo==2:#se il giocatore ha creato l'host
        dir_x=1#movimento x della palla +1
        dir_y=1#movimento y della palla -1
    else:#altrimenti
        dir_x=-1#movimento x della palla -1
        dir_y=-1#movimento y della palla -1
    rallenty=0#variabile che rallenta la palla e la fa muovere non ad ogni ciclo
    actived_fullscreen=False#Variabile che indica se il gioco e' a schermo intero
    sent_data=0#variabile che indica quanti dati sono stati scambiati
    block_data=False#variabile che blocca la ricezione di dati via socket
    #Nuova Creazione | Connessione di scambio di dati
    if tipo==2:#se il giocatore ha creato l'host
        x,y=s.accept()#accettazione della connessione per un cliente
        time.sleep(2)#aspetta 2 secondi in modo che venga inizializzata la schermata anche nell'altro pc
        x.send("start")#trasmette il comando start, per cominciare
        print "Socket riconnesso con successo"
    else:
        h=socket.socket()#assegnazione del socket a un altra variabile
        h.connect((server_ip,80))#connessione al socket
        while True:#finche' vero
            start=h.recv(1024)#ricezione dati
            if start=="start":#se il comando ricevuto e' giusto
                print "Socket riconnesso con successo"
                break#esci dal ciclo
    #Inizio ciclo di gioco
    while game:#finche' il gioco e' attivo
        if enemy_life==0:#se l'avversario ha perso
            risultato= "Hai Vinto!!"
            screen.blit(scritta, (400,300))
            break#interrompi il gioco
        if player_life==0:#se il giocatore ha perso
            risultato= "Hai Perso!!"
            screen.blit(scritta, (400,300))
            break#interrompi il gioco
        for event in pygame.event.get():#per ogni evento da tastiera
            if event.type==QUIT:#se si preme sul tasto di uscita
                game=False#game finisce
                if tipo==2: x.send("gameStop")#se hai creato l'host, invia di fermare il gioco
                else: h.send("gameStop")#altrimenti invia di fermare il gioco
            elif event.type==KEYDOWN:#se tasto premuto
                if event.key==K_F11:#se f11: attiva disattiva lo schermo intero
                   if tipo==2: x.send("fullscreenMODE")#invia all'altro giocatore
                   else: h.send("fullscreenMODE")#invia all'altro giocatore
                   if actived_fullscreen==False:#se non a schermo itero
                       actived_fullscreen=True#allora a schermo intero
                       pygame.display.set_mode((width, height),pygame.FULLSCREEN)#metto a schermo intero
                       time.sleep(2)#aspetto che la schermata sia inizializzata correttamente
                       rallenty=3#variabile della palla a 3, cioe' si sposta ad ogni ciclo
                   else:#altrimenti
                       actived_fullscreen=False#schermo intero disattivato
                       pygame.display.set_mode((width, height),0)#tolgo lo schermo intero
                       time.sleep(2)#aspetto
                       rallenty=0#la palla e' rallentata
                elif event.key==K_ESCAPE:#se premo tasto esc
                    game=False
                    if tipo==2: x.send("gameStop")
                    else: h.send("gameStop")
                if not stop_input:#se stop input e' falso
                    if event.key==K_RIGHT or  event.key==K_d:  #freccia destra o tasto d
                        moving_player=1#variabile del movimento fluido a 1 (a destra)
                    elif event.key==K_LEFT or  event.key==K_a:#se freccia sinistra o tasto a
                        moving_player=2#metto a 2 cioe' a sinistra
        #Raccolta | Invio dati
        try:
            if tipo==2:#se avevi creato l'host
                if block_data==False:#se posso mandare dati
                    x.send(str(player_x))#mando la coordinata x sotto forma di stringa
                else:#altrimenti
                    block_data=False#rimetto la variabile a False, cioe' posso mandare ancora
                data=x.recv(1024)#ricezione dati
                sent_data+=1#aggiungo di +1 il valore di scambio dati
            else:#se ero un client
                if block_data==False:#se posso mandare i dati
                    h.send(str(player_x))#mando i dati
                else:#altrimenti
                    block_data=False#imposto che si possono madare
                data=h.recv(1024)#ricezione
                sent_data+=1#+1 allo scambio dati
        except: pass
        #Analisi dati ricevuti
        if data=="gameStop":#se ricevo gameStop
            game=False#fermo il gioco
        elif data=="reset-1":#se ricevo reset-1
            block_ball=600#tempo di attesa per la palla
            enemy_life-=1#tolgo una vita all'avversario
            if tipo==2:#reimposto i valori della palla come all'inizio
                dir_x=1
                dir_y=1
            else:
                dir_x=-1
                dir_y=-1
        elif data=="reset+1":#se ricevo reset+1
            block_ball=600#reimposto il tempo di attesa per la palla
            player_life-=1#tolgo una vita al giocatore
            if tipo==2:#reimposto i valori della palla
                dir_x=1
                dir_y=1
            else:
                dir_x=-1
                dir_y=-1
        elif data=="fullscreenMODE":#se ricevo fullscreenmode
            if actived_fullscreen==False:#se ero a schermo normale
                actived_fullscreen=True#metto a schermo intero
                pygame.display.set_mode((width, height),pygame.FULLSCREEN)
                time.sleep(2)
                rallenty=3
            else:
                actived_fullscreen=False #altrimenti rimetto a schermo normale
                pygame.display.set_mode((width, height),0)
                time.sleep(2)
                rallenty=0
        else:#infine
            enemy_x=(width-int(data)-100)#i dati ricevuti li trasformo in numeri e li impost come coordinate dell'avversario capovolte
        #Movimento fluido del giocatore
        if moving_player==1:#se andavo a destea
            if player_x!=(width-100):#se non tocco il bordo
                player_x+=1#coordinata x +1
        elif moving_player==2:#se andavo a sinistra
            if player_x!=0:#se non tocco il bordo
                player_x-=1#coordinata x -1
        #Movimento palla
        if ball_y ==50+radious:#se la palla e' all'y l'avversario
            if ball_x in range(enemy_x, enemy_x+100):#se e' comepresa tra le coordiante x dell'avversario
                dir_y=alg_ball_y(abs(dir_y))#richiamo funzione per scambio di coordinate x e y
                dir_x=alg_ball_x(abs(dir_x))
        elif ball_y ==player_y-radious:#se la palla e' all'y del giocatore
            if ball_x in range(player_x, player_x+100):#se la palla e' compresa tra le x del giocatore
                dir_y=-alg_ball_y(abs(dir_y))#richiamo funzione per il rimbalzo
                dir_x=-alg_ball_x(abs(dir_x))
        elif ball_y<=(-radious):#se la palla e' uscita dalla schermata dall'alto
            if tipo==2:x.send("reset+1")#perde una vita l'avversario e lo mando via socket
            else: h.send("reset+1")
            block_data=True#blocco l'invio di dati per evitare che si sovrappongano
            ball_x, ball_y = width/2, height/2#rimetto i giocatori + palla alle coordiate iniziali
            player_x, player_y = (width-100)/2, (height-20-30)
            moving_player=0#il giocatore non si muove
        elif ball_y>=(height+radious):#se la palla e' uscita dal basso
            if tipo==2:x.send("reset-1")#perdo una vita e lo mando via socket
            else: h.send("reset-1")
            block_data=True#blocco l'invio dati
            ball_x, ball_y = width/2, height/2
            player_x, player_y = (width-100)/2, (height-20-30)
            moving_player=0
        if ball_x in range(width-radious-5, width-radious+5):#se la palla tocca i bordi laterali
            dir_x=-alg_ball_x(abs(dir_x))#funzione per il rimbalzo
        elif ball_x in range(radious-5,radious+5):
            dir_x=alg_ball_x(abs(dir_x))

        screen.fill((10,20,150))#imposto lo sfondo
        if block_ball==0:#se il blocco della palla e' 0
            stop_input=False#posso muovere il giocatore
            if rallenty==1:#se il rallentamento e' a 1
                rallenty=0#lo metto a zero
                ball_x+=dir_x#muovo la palla
                ball_y+=dir_y
            elif rallenty==3:#se e' a 3
                ball_x+=dir_x#muovo subito la palla
                ball_y+=dir_y
            else:rallenty+=1#altrimenti(0) aumento di 1 la palla

            ball=pygame.draw.circle(screen, (255,255,255),(ball_x, ball_y),radious,0)#costruisco la palla
            player=pygame.draw.rect(screen, (255,255,255), Rect((player_x, player_y), (100,30)))#il giocatore
            enemy=pygame.draw.rect(screen, (255,255,255), Rect((enemy_x, enemy_y), (100,30)))#e l'avversario
        else:#altrimenti se la palla e' bloccata
            stop_input=True#blocco la ricezione dati
            scritta=font.render(pausa(block_ball),1,(255,255,255))#costruisco la scritta 3, 2, 1
            screen.blit(scritta, ((width/2)-10,height/2))#la stampo
            block_ball-=1#diminuisco di 1 il blocco

	    
        pygame.display.flip()#aggiorno la schermata
        

    pygame.quit()#esco da pygame
    if tipo==2: x.close()#se avevo creato l'host, chiudo
    else: h.close()#altrimeti chiudo
    print "Dati mandati | ricevuti: ",sent_data#stampo i dati scambiati
    while True:#finche' vero
        domanda=raw_input("Vuoi giocare di nuovo? (s/n): ")#chiedo se si vuole rigiocare
        if domanda=="s":#se si ricomincio
            startGame()#avvio il gioco
            break#fermo il ciclo
        elif domanda=="n": #se no chiudo il socket
            s.close()
            exit(0)#ed esco
        else: print "comando non riconosciuto"#se non e' ne si ne no
#Pausa---------------------------------------------------------------------------------------------------------------------------
def pausa(num): #funzione per cambiare il 3 in 2 e poi in 1
    if num>400:#se il blocco e' maggiore di 400 ritorno 3
        return "3"
    elif num<=400 and num>200:#se e' compreso tra 400 e 200 ritorno2
        return "2"
    else:#altrimenti ritorno 1
        return "1"
#Algoritmo direzione costante palla---------------------------------------------------------------------------------------
def alg_ball_x(x):#algoritmo per muovere la palla
    if x==1: x=3#se era a 1 imposto3
    elif x==2: x=1#se era a 2 imposto 1
    else: x=2#se era a 3 imposto 2
    return x#ritorno il valore assoluto, non i segni

def alg_ball_y(y):#lo stesso per la y, ma solo con 2 casi
    if y==1: y=2#se a 1 allora 2
    else: y=1#altrimenti 1
    return y#ritorno
#Connessione al Socket------------------------------------------------------------------------------------------------------
def conn_connect():#funzione di connessione
    global tipo#tipo e' globale
    tipo=1#e' un client perche' mi connetto
    hide_buttons(False)#richiamo la funzione con valore False
    ip_text.place(x=60, y=100)#costruzione della schermata Tkinter
    Button(t, text="OK", height=1, command=get_text).place(x=200, y=100)#aggiungo un pulsante che richiama la funzione get_text
    

#Connessione al Socket------------------------------------------------------------------------------------------------------
def get_text():#Funzione per connettersi al socket
    cod = ip_text.get()#ottengo il valore inserito nel campo di testo dall'utente
    try:#provo
        s.connect((cod,80))#mi connetto con l'ip inserito e porta 80
        s.send(socket.gethostname())#mando il nome del mio pc
        data=""#variabile data
        while True:#finche vero
            data=s.recv(1024)      #ricevo          
            if data=="startGame":#se =startGame
                print "Gioco avviato con successo"
                startGame()#comincio
            else:#altrimenti
                global server_ip#variabile globale del nome pc (quindi anche ip) per riconnettermi durante il gioco
                server_ip=data#assegno il nuovo valore
                print "Connessione riuscita -",data,"|",socket.gethostbyname(data)#stampo il nome e l'ip
            time.sleep(1)#aspetto 1 s per ridurre le prestazioni e stressare meno la cpu
        
    except Exception as e:
        print str(e)


#Modifica Interfaccia per la connessione---------------------------------------------------------------------------------
def hide_buttons(var):#funzione che pulisce la schermata Tkinter
    collega.place_forget()#cancello il tasto collega
    crea.place_forget()#cancello il tasto crea
    if var:#se true
        global procedi
        procedi=Button(t, text="Procedi", command=ricerca)#aggiungo il pulsante procedi che avviera' la ricerca dati
        procedi.place(x=120, y=80) #assegno x e y
        stringVar.set(socket.gethostbyname(socket.gethostname()))#assegno a una casella di testo il mio ip da comunicare all'altro giocatore
        sugg.set("Clicca procedi per continuare")#suggerimento dato all'utente
    else:
        sugg.set("Inserisci l'indirizzo IP del primo giocatore")#se false: suggerimento di inserire l'ip


#Creazione del Socket--------------------------------------------------------------------------------------------------------    
def conn_start():#creazione del socket di flusso
    global tipo
    tipo=2#giocatore che crea l'host
    ip=socket.gethostbyname(socket.gethostname())#trovo il mio ip con le funzioni gethostbyname(cioe' trova l'ip tramite nome) di gethostname(ottieni il mio nome)
    try:
        s.bind((ip,80))#avvio
        s.listen(5)#predispogo le connessioni
        print "Host avviato con successo"
        hide_buttons(True)#richiamo la funzione con valore true
    except Exception as e:
        print str(e)
    return


#Ricerca dei dispositivi--------------------------------------------------------------------------------------------------------
def ricerca():#funzione ricerca di client
    try:
        conn,addr=s.accept()#accetto la connessione
        recv=conn.recv(1024)#ricevo dati
        if recv!="":#se dati diverso da nulla
            conn.send(socket.gethostname())#invio il mio nome
            conn.send("startGame")#mando l'ok per la partenza
            conn.close()#chiudo
            print "Connessione riuscita -",recv,"|",socket.gethostbyname(recv)#stampo con chi mi sono connesso
            startGame() #avvio il gioco
        else:#altrimenti
            conn.close()#chiudo
            time.sleep(1)#riduco i processi della cpu aspettando
            ricerca()#ricorsione
    except Exception as ex:
        print str(ex)


#Creazione dell'interfaccia grafica------------------------------------------------------------------------------------------
def tk_init():#inizializzo l'interfaccia Tkinter
    global ip_label, stringVar, crea, collega, sugg, ip_text#valori globali che verranno riassegnati
    stringVar = StringVar()#stringa variabile per le interfacce
    sugg = StringVar()#altra stringa variabile
    t.title("Opzioni")#titolo dell'interfaccia
    t.geometry("300x150+350+200")#dimensioni dell'interfaccia
    t.resizable(False, False)#non e' ridimensionabile
    ip_label = Label(t, textvariable=stringVar, justify=CENTER)#imposto la posizione dell'ip che verra' inserito
    ip_label.place(x=120, y=120)
    ip_text=Entry(t)#imposto la casella di input ma non la posiziono
    Label(t, textvariable=sugg, justify=CENTER).place(x=80, y=10)#imposto il testo suggerimento
    collega = Button(t, text="Collegati", width=8, height=1, command=conn_connect)#imposto e posiziono i 2 pulsanti che richiameranno funzioni diverse
    collega.place(x=60, y=100)
    crea = Button(t, text="Crea", width=8, heigh=1, command=conn_start)
    crea.place(x=180, y=100)
    t.mainloop()#avvio l'interfaccia


#Main----------------------------------------------------------------------------------------------------------------------------
def main():
    tk_init()#richiamo l'interfaccia


#Avvio programma-----------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()#avvio il programma
