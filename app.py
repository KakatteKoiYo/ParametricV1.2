import ipaddress
import tkinter as tk, requests, serial,time, re, os, socket
from xml.etree import ElementTree
from tkinter import messagebox
from PIL import ImageTk,Image 
from datetime import datetime
from threading import Timer
####Configuracion inicial del programa   ##################################
window = tk.Tk()
window.attributes("-fullscreen", True)
#window.geometry("770x480")
#window.geometry("800x800")
#window.geometry("1900x1080")
global filtro, cantidad_escaneo, modelo

_version_ = "1.2.2"

window.update()
screen_width = window.winfo_width()#window.winfo_screenwidth()
screen_height = window.winfo_height()#window.winfo_screenheight()


sizeDic = {
    "CamporespuestaX" : int(screen_width * 0.038),
    "CamporespuestaY" : int(screen_height * 0.562),
    "CamposerialX" : int(screen_width * 0.1229),
    "CamposerialY" : int(screen_height * 0.4058),
    "CamposerialW" :int(screen_width * 0.0519),
    "BotonesX" : int(screen_width * 0.3155),
    "BotonesY" : int(screen_height * 0.0312),
    "BotonOKX" : int(screen_width * 0.7376),
    "BotonOKY" : int(screen_height * 0.1666),
    "BotonConfX" : int(screen_width * 0.0220),
    "BotonConfY" : int(screen_height * 0.2083),
    "BotonAllX" : int(screen_width * 0.0220),
    "BotonAllY" : int(screen_height * 0.03125),
    "BotonClearX" : int(screen_width * 0.7376),
    "BotonClearY" : int(screen_height * 0.0312),
    "BotonSize" : int(((screen_width * 0.1250)/ 5) * 1.50),
    "BotonW" : int(screen_height * 0.0649 ),
    "FixtureIMGSizeW" : int(screen_width * 0.389),
    "FixtureIMGSizeH" : int(screen_height * 0.5208),
    "FixtureX" : int(screen_width * 0.2857),
    "FixtureY" : int(screen_height * 0.1875),
    "BotonListoX" : int(screen_width * 0.7532),
    "BotonListoY" : int(screen_height * 0.1666),
    "BotonCancelarX" : int(screen_width * 0.0129),
    "BotonCancelarY" : int(screen_height * 0.1666),
    "BotonesLadosSize" : int((((screen_width * 0.1900)/10)*1.50)),
    "RespuestaFontSize" : int((((screen_width * 0.7587)/75)*1.50)),
    "SerialLabelFontSize" : int((((screen_width * 0.0777)/5)*1.50)),
    "SerialInputFontSize" : int((((screen_width * 0.6218)/40)*1.50)),
    "RespuestaLabelFontSize" : int((((screen_width * 0.0981)/8)*1.50)),
    "EspacioAppInfoX" : int(screen_width * 0.1257),
    "AppInfoFontSize" : int((((screen_width * 0.0698)/10)*1.50)),

}



#print(sizeDic["RespuestaFontSize"])

try:
    imgdb = ImageTk.PhotoImage(Image.open("fixture.png").resize((sizeDic["FixtureIMGSizeW"], sizeDic["FixtureIMGSizeH"])))
    imgFlechaAr = ImageTk.PhotoImage(Image.open("up.png").resize((70, 70)))
    imgFlechaAb = ImageTk.PhotoImage(Image.open("down.png").resize((70, 70)))
    imgFlechaD = ImageTk.PhotoImage(Image.open("right.png").resize((70, 70)))
    imgFlechaI = ImageTk.PhotoImage(Image.open("left.png").resize((70, 70)))
except:
    imgdb = ImageTk.PhotoImage(Image.open("/oktotest_pmc/imagen/fixture.png").resize((sizeDic["FixtureIMGSizeX"], sizeDic["FixtureIMGSizeH"])))
    imgFlechaAr = ImageTk.PhotoImage(Image.open("/oktotest_pmc/imagen/up.png").resize((70, 70)))
    imgFlechaAb = ImageTk.PhotoImage(Image.open("/oktotest_pmc/imagen/down.png").resize((70, 70)))
    imgFlechaD = ImageTk.PhotoImage(Image.open("/oktotest_pmc/imagen/right.png").resize((70, 70)))
    imgFlechaI = ImageTk.PhotoImage(Image.open("/oktotest_pmc/imagen/left.png").resize((70, 70)))


error = 0
filtro = 0

cantidad_escaneo = 0
mensaje = ""
modelo = ""



#print(sizeDic)
###Metodo con todo el diseno de la interfaz principal ##################################
def iniciar():
    try: 
        global datos_entrada, campo_informacion, ventanaPrincipal
        global boton_uno, boton_dos, boton_tres, boton_cuatro, cantidad_seleccion


        ventanaPrincipal = tk.Frame(window)
        ventanaPrincipal.pack(fill="both", expand="yes")

        ### Tamano de los numeros de los botones, su ancho y espacio en Y y X ##################################
        numero_size = ("arial", sizeDic["BotonSize"])
        ancho_boton = 5
        espacio_botonx = 5
        espacio_botony = 5
        
        ### Creando las variables de botones como null ##################################
        boton_uno = boton_dos = boton_tres = boton_cuatro = None

        botonFrame = tk.Frame(ventanaPrincipal)
        botonFrame.place(x = sizeDic["BotonesX"], y = sizeDic["BotonesY"])

        filaUno = tk.Frame(botonFrame)
        filaUno.pack()
        filaDos = tk.Frame(botonFrame)
        filaDos.pack()

        ###Botones de seleccion de imagenes de PARAMETRIC ##################################
        boton_uno = tk.Button(filaUno, text= "1", font = numero_size, width = ancho_boton, 
            command = lambda: seleccionEscaneo(boton_uno, reset= True ) )
        boton_uno.pack(side = tk.LEFT, padx = espacio_botonx, pady = espacio_botony)

        boton_dos = tk.Button(filaUno, text= "2", font = numero_size, width = ancho_boton,
            command = lambda: seleccionEscaneo(boton_dos, reset= True ) )
        boton_dos.pack(side = tk.LEFT, padx = espacio_botonx, pady = espacio_botony)

        boton_tres = tk.Button(filaDos, text= "3", font = numero_size, width = ancho_boton,
            command = lambda: seleccionEscaneo(boton_tres, reset= True ) )
        boton_tres.pack(side = tk.LEFT, padx = espacio_botonx, pady = espacio_botony)

        boton_cuatro = tk.Button(filaDos, text= "4", font = numero_size, width = ancho_boton,
            command = lambda: seleccionEscaneo(boton_cuatro, reset= True))
        boton_cuatro.pack(side = tk.LEFT, padx = espacio_botonx, pady = espacio_botony)


        ###Boton ALL: habilita todos los botones de seleccion ##################################
        boton_all = tk.Button(ventanaPrincipal, text= "ALL", font =  ("arial", sizeDic["BotonesLadosSize"]), width = 10, bg = "SeaGreen1",
            command = lambda: seleccionEscaneo(all = True, reset= True ) )
        boton_all.place(x = sizeDic["BotonAllX"], y = sizeDic["BotonAllY"])
        ###Boton CLEAR: deshabilita todos los botones de seleccion ##################################
        boton_clear = tk.Button(ventanaPrincipal, text= "CLEAR", font =  ("arial", sizeDic["BotonesLadosSize"]), width = 10, bg = "SkyBlue1",
            command = lambda: seleccionEscaneo(clear = True, reset= True))
        boton_clear.place(x = sizeDic["BotonClearX"], y = sizeDic["BotonClearY"])
        ###Boton CONF: modo soporte, para configuracion del programa, usar teclado o teclas ##################################
        boton_conf = tk.Button(ventanaPrincipal, text= "CONF", font =  ("arial", sizeDic["BotonesLadosSize"]), width = 10, bg = "grey",
            command = askPassword )
        #boton_conf.place(x = sizeDic["BotonConfX"], y = sizeDic["BotonConfY"])
        ###Boton OK: para cerrar ventana emergente. Llama a funcion que envia un dato por com serial al arduino para enviar un Enter ####
        boton_ok = tk.Button(ventanaPrincipal, text= "OK", font =  ("arial", sizeDic["BotonesLadosSize"]), width = 10, height = 2,bg = "SkyBlue1",
            command = lambda: enviarDatos("OK"))
        boton_ok.place(x = sizeDic["BotonOKX"], y = sizeDic["BotonOKY"])


        serialFrame = tk.Frame(ventanaPrincipal)
        serialFrame.place(x = sizeDic["CamposerialX"], y = sizeDic["CamposerialY"])

        serial_label = tk.Label(serialFrame, text = "SERIAL", font = ("arial", sizeDic["SerialLabelFontSize"]))
        serial_label.pack()

        datos_entrada = tk.Entry(serialFrame, width = 40, font = ("arial", sizeDic["SerialInputFontSize"]))
        datos_entrada.pack(side = tk.LEFT)
        datos_entrada.focus()
        datos_entrada.bind('<Return>', lambda event: retenerSeriales(event, datos_entrada.get()))
        cantidad_seleccion = tk.Label(serialFrame, text = "", font = ("arial bold", 30))
        cantidad_seleccion.pack(side = tk.LEFT)


        respuestaFrame = tk.Frame(ventanaPrincipal)
        respuestaFrame.place(x = sizeDic["CamporespuestaX"], y = sizeDic["CamporespuestaY"])

        respuesta_label = tk.Label(respuestaFrame, text = "RESPUESTA", font = ("arial", sizeDic["RespuestaLabelFontSize"]))
        respuesta_label.pack()

        campo_informacion = tk.Text(respuestaFrame, width =  75, height = 7, font =("arial", sizeDic["RespuestaFontSize"]))
        campo_informacion["state"] = "disabled"
        campo_informacion.pack()
        #Obtencion de IP Adress
        hostname=socket.gethostname() 
        ipaddress = socket.gethostbyname(hostname)

        appInfoFrame = tk.Frame(respuestaFrame)
        appInfoFrame.pack()
        
        ipLabel = tk.Label(appInfoFrame, text = "[IP:"+ipaddress+"]", font= ("arial", sizeDic["AppInfoFontSize"]), fg = "grey")
        ipLabel.pack(side = tk.LEFT, padx= sizeDic["EspacioAppInfoX"])

        versionLabel = tk.Label(appInfoFrame, text = "[V"+_version_+"]", font= ("arial", sizeDic["AppInfoFontSize"]), fg = "grey")
        versionLabel.pack(side = tk.LEFT, padx= sizeDic["EspacioAppInfoX"])

        ### Configuro los botones en color verde, que el programa entiende como habilitados
        boton_uno["bg"] = boton_dos["bg"] = boton_tres["bg"] = boton_cuatro["bg"] = "green"
    except Exception as e:
        escribirLogFallas("iniciar(): " + str(e))

def seleccionEscaneo(objeto = False, reset = False, all = False, clear = False, mensaje  = ""):
    try:
        global  error, cantidad, cantidad_escaneo, serialesArr, cantidadPasoFinal, modelo
        
        cantidad = 0
        serialesArr = []
        mensaje_serial = ""

        limpiarCampo()
        modelo = ""
        
        if reset == True:
            
            if all == True:
                boton_uno["bg"] = boton_dos["bg"] = boton_tres["bg"] = boton_cuatro["bg"] = "green"
            if clear == True:
                boton_uno["bg"] = boton_dos["bg"] = boton_tres["bg"] = boton_cuatro["bg"] = "grey"
            cantidad_escaneo = 0
            error = 0
            campo_informacion["bg"] = "white"
            
        if objeto != False:
            if objeto["bg"] == "green":
                objeto["bg"] = "grey"
                objeto["activebackground"] = "grey"
            else:
                objeto["bg"] = "green"
                objeto["activebackground"] = "green"


        if boton_uno["bg"] == "green":
            cantidad = cantidad+1
            mensaje_serial += "1"
        else:
            mensaje_serial += "0"
        if boton_dos["bg"] == "green":
            cantidad = cantidad+1
            mensaje_serial += "1"
        else:
            mensaje_serial += "0"
        if boton_tres["bg"] == "green":
            cantidad = cantidad+1
            mensaje_serial += "1"
        else:
            mensaje_serial += "0"
        if boton_cuatro["bg"] == "green":
            cantidad = cantidad+1
            mensaje_serial += "1"
        else:
            mensaje_serial += "0"

        if mensaje_serial == "0000":
            datos_entrada["state"] = "disabled"
        else:
            datos_entrada["state"] = "normal"
        ##print(cantidad)

        texto_seleccion = "0" + "/" + str (cantidad)
        cantidad_seleccion["text"] = texto_seleccion

        campo_informacion["state"] = "normal"
        campo_informacion.insert(tk.INSERT, mensaje)
        campo_informacion["state"] = "disabled"
        
        if cantidad_escaneo == cantidad and cantidad != 0:
            if error == 0:
                
                cantidad_escaneo = 0
                confirmacion(mensaje_serial)
            if error == 1:
                datos_entrada.focus()
                campo_informacion["state"] = "normal"
                campo_informacion.insert(tk.INSERT, "Una o mas de las unidades no lleva el flujo correcto. Verifica el historial" )
                campo_informacion["bg"] = "red"
                campo_informacion["state"] = "disabled"
                error = 0
                
                cantidad_escaneo = 0
                cantidadPasoFinal = 0
    except Exception as e:
        escribirLogFallas("seleccionEscaneo(): " + str(e))
                    
def timerFunc(opcionTimer):
    try: 
        if opcionTimer == "reinicio":
            seleccionEscaneo(reset=1)
        if  opcionTimer == "cerrar": 
            cerrarVentana()
            seleccionEscaneo(mensaje="Se agoto tiempo de espera en confirmacion")
    except Exception as e:
        escribirLogFallas("timerFunc(): " + str(e))

def retenerSeriales(event, serial):
    try: 
        #BORRAR serialesArr
        global cantidad_escaneo, serialesArr, datos_entrada, seriales2DArray, serialesMasterArray, filtro, mensaje, modelo, error, tiempoReinicio
        if serial == "":
            return
        if cantidad_escaneo <= cantidad:
            serialesMasterArray = []
            seriales2DArray = []
            cantidad_escaneo += 1
            texto_seleccion = str(cantidad_escaneo) + "/" + str (cantidad)
            cantidad_seleccion["text"] = texto_seleccion
            limpiarCampo()
            if cantidad_escaneo == 1:
                try:
                    if tiempoReinicio.is_alive():
                        tiempoReinicio.cancel()
                        
            
                except: 
                    pass
                tiempoReinicio = Timer(20.0, timerFunc, ["reinicio"])
                tiempoReinicio.start()
            

            if serial in serialesArr:
                error = 1
                seleccionEscaneo(reset=  1, mensaje = "Uno de los seriales es repetido\n")
                
                return
            serialesArr.append(serial)
            try:
                datos_entrada.delete('0', 'end')
                
                try:
                    if not "," in serial:
                        if modelo != "" and modelo != serial[0: serial.rindex("-")]:
                            seleccionEscaneo(reset=1, mensaje = "Uno de los seriales no pertenece al mismo modelo.\n Modelos:\n- " + modelo + ":\n-"+ serial.split(",")[0])
                            return
                        modelo = serial[0: serial.rindex("-")]
                    elif len(serial.split(",")[1]) > 11:
                        if modelo != "" and modelo != serial.split(",")[0]:
                            seleccionEscaneo(reset=1, mensaje = "Uno de los seriales no pertenece al mismo modelo.\n Modelos:\n- " + modelo + ":\n-"+ serial.split(",")[0])
                            return

                        modelo = serial.split(",")[0]
                    else:
                        if modelo != "" and modelo != serial[0: serial.rindex("-")]:
                            error = 1
                            seleccionEscaneo(reset=1, mensaje = "Uno de los seriales no pertenece al mismo modelo.\n Modelos: " + modelo + ", "+ serial[0: serial.rindex("-")])
                            return
                        modelo = serial[0: serial.rindex("-")]
                except Exception as e: 
                    messagebox.showinfo(title="ERROR", message="Serial no valido: "+ serial +"\n" + "Asegurese de escanear el serial 2D")
                    seleccionEscaneo(reset=1)
                    print(e)
                    return
                print(modelo)
                if len(serialesArr) == cantidad:
                    tiempoReinicio.cancel()
                    mensaje = ""
                    datos_entrada["state"] = "disabled"
                    window.focus()
                    #datos_entrada.mainloop()
                    window.update()
                    seriales2DArray = serialesArr
                    getGolden(serialesArr)

            except Exception as e: 
                print(e)
            filtro = 0
    except Exception as e:
        escribirLogFallas("retenerSeriales(): " + str(e))        
    
def limpiarCampo():
    try: 
        campo_informacion["state"] = "normal"
        campo_informacion.delete('1.0','end')
        campo_informacion["state"] = "disabled"
        datos_entrada.delete('0', 'end')
    except Exception as e:
        escribirLogFallas("limpiarCampo(): " + str(e))

def getGolden(array):

    try: 
        isGolden = 0
        isRegistered = 0
        preventFlag = 0


        url = "http://mxgdlm0webte02/OkToTesterWebServiceInterface/OkToTesterWebServiceInterface.asmx"

        headers = {"Content-Type" : "text/xml; charset=utf-8"}

        body = """<?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
        <soap:Body>
        <GetWhiteListFromCustomer xmlns="http://tempuri.org/">
        <customer>ACLARA</customer>
        </GetWhiteListFromCustomer>
        </soap:Body>
        </soap:Envelope>
        """

        ### Convierto texto recibido en XML
        response = requests.post(url, data = body, headers = headers)
        txtmesstep = response.text 
        


        xmlgolden = ElementTree.fromstring(txtmesstep)
        goldentxt = xmlgolden[0][0][0].text
        for i in array:
            if re.search(i, goldentxt):
                isGolden = 1
                if escribirLeerMasterDeGolden(i) != False and preventFlag == 0:
                    isRegistered = 1
                    serialesMasterArray.append(escribirLeerMasterDeGolden(i))
                else:
                    isRegistered = 0
                    preventFlag = 1
                
        
        #print(isGolden)
        if isRegistered == 1 and len(array) == len(serialesMasterArray):
            #print(array)
            #print(serialesMasterArray)
            okToTest(array, serialesMasterArray, isGolden, 0)
        else:
            toMaster(array, isGolden, 0)


        
    except Exception as e:
        escribirLogFallas("getGolden(): " + str(e))

def toMaster(serial_2dArray, isGolden = 0, contador = 0):
    try:
        try:
            global filtro, modelo, error

            if isGolden == 1:
                raise Exception()
            
            url = "http://mxgdlm0webte02/wsMesInterface/MesWebServiceInterface.asmx"

            headers = {"Content-Type" : "text/xml; charset=utf-8"}
        

            body = """<?xml version="1.0" encoding="utf-8"?>
            <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
            <soap:Body>
            <GetBoardHistoryFromMesInstance xmlns="http://tempuri.org/">
            <mesInstance>1</mesInstance>
            <customerID>68</customerID>
            <serialNumber>"""+serial_2dArray[contador]+"""</serialNumber>
            </GetBoardHistoryFromMesInstance>
            </soap:Body>
            </soap:Envelope>"""
            response = requests.post(url, data = body, headers = headers)
            
            txtmes = response.text 
            txtmes2 = txtmes.replace("&lt;", "<").replace("&gt;", ">")
            xmlmes2d = ElementTree.fromstring(txtmes2)

            serialrespuesta = xmlmes2d[0][0][0][0][1].text
            ##print(xmlmes2d[0][0][0][0][1].text)

        except:    
            
            url = "http://mxgdlm0webte02//OkToTesterWebServiceInterface/OkToTesterWebServiceInterface.asmx"

            headers = {"Content-Type" : "application/soap+xml; charset=utf-8"}
            body = """<?xml version="1.0" encoding="utf-8"?>
            <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
            <soap12:Body>
            <GetMesSerialFromLinkedCode xmlns="http://tempuri.org/">
            <customer>ACLARA</customer>
            <linkedCode>"""+serial_2dArray[contador]+"""</linkedCode>
            <instance>1</instance>
            </GetMesSerialFromLinkedCode>
            </soap12:Body>
            </soap12:Envelope>"""


            response = requests.post(url, data = body, headers = headers)

            xmlmes2d = ElementTree.fromstring(response.text)
        
            serialrespuesta = xmlmes2d[0][0][0].text

        serialesMasterArray.append(serialrespuesta)
        escribirLeerMasterDeGolden(serial_2dArray[contador], serialrespuesta)

        if serialrespuesta == "Serial Linked Not Founded" and filtro == 0:

            mensajeError ="Serial no valido: "+ serial_2dArray[contador] + " Asegurese de escanear el serial 2D\n"
            filtro = 1
            

        contador = contador + 1
        if contador == cantidad:
            if filtro == 1:
                error = 1
                seleccionEscaneo(mensaje = "[MODELO: " + modelo + "]\n" + mensajeError)
                return
            else: 
                #print("Hola estoy aqui")
                okToTest(serial_2dArray, serialesMasterArray, isGolden, 0)
        else: 
            
            toMaster(serial_2dArray, isGolden, contador)
        return
    except Exception as e:
        escribirLogFallas("toMaster(): " + str(e))

def okToTest(serial_2dArray, serial_masterArray, isGolden, contador):
    try:
        #print(serial_masterArray[contador])
        #print(serial_2dArray[contador])
        global  error, cantidadPasoFinal, mensaje, modelo, isGoldenGlobal
        #print(serial_masterArray)
        isGoldenGlobal = isGolden
        ##print(serial_2d + " " + serial_master)
        
        #url = "http://mxgdlm0tis01/MES-TIS/tis.asmx"
        url = "https://mes-tis.gdl.corp.jabil.org:1010/MES-TIS/"

        headers = {"Content-Type" : "application/soap+xml; charset=utf-8"}

        body = """<?xml version="1.0" encoding="utf-8"?>
        <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
        <soap12:Body>
        <GetCurrentRouteStep xmlns="http://jabil.com/GMS/MES_TIS">
        <SerialNumber>"""+serial_masterArray[contador]+"""</SerialNumber>
        </GetCurrentRouteStep>
        </soap12:Body>
        </soap12:Envelope>
        """
        #print(serial_masterArray[contador])
        try:
            response = requests.post(url, data = body, headers = headers, verify = False)
            txtmes = response.text 
            txtmes2 = txtmes.replace("&lt;", "<").replace("&gt;", ">")
            xmlmes = ElementTree.fromstring(txtmes2)

            paso = xmlmes[0][0][0][0][0][6].text
            status = xmlmes[0][0][0][0][0][14].text
            tiempoprueba = xmlmes[0][0][0][0][0][12].text

            

            isTimeOK = testtime(tiempoprueba)
            ##print(isTimeOK)

        
            if isGolden == 1:
                if paso == "MDA" and status == "Fail":
                    respuesta_programa = "Golden fallada en MDA. No puede probarse"
                    error = 1
                    
                else: 
                    respuesta_programa = "Se puede probar"
                    campo_informacion["bg"] = "white"

            else:
                if paso == "MDA" and status == "Pass" and isTimeOK[2] == True:
                    respuesta_programa = "Se puede probar"
                    campo_informacion["bg"] = "white"
                else:
                    if isTimeOK[2] == False and status != "Pass":
                        respuesta_programa = "Necesario: "+isTimeOK[0].strip()+" min. Se probo hace: " + isTimeOK[1] + " min"
                    else:
                        if status == "Fail":
                            respuesta_programa = "Unidad fallada en paso: " + paso
                        else:
                            respuesta_programa = "ultimo dato: " + paso
                    error = 1
                
                # if revisarSerialesBloqueados(serial_2dArray[contador]) == 0:
                #     respuesta_programa =  "Esta unidad ya fue escaneada. Debe esperar 10 min para volver a probarla"
                #     error = 1
            

            #respuesta_historial =  paso + " " + status 
            mensaje += serial_2dArray[contador] + " " + respuesta_programa + "\n"
            
            contador = contador + 1
            #print(contador)
            if contador  == cantidad:
                
                seleccionEscaneo(mensaje = "[MODELO: " + modelo + "]\n" + mensaje)
            else:
                #print(contador)
                okToTest(serial_2dArray, serialesMasterArray, isGolden, contador)
                

        except Exception as e:
            messagebox.showinfo(title="ERROR", message="Ocurrio un error\n Verifique el serial. " + str(e) )
            datos_entrada["state"] = "normal"
            
            seleccionEscaneo(reset = 1)

    except Exception as e:
        escribirLogFallas("okToTest(): " + str(e))        
        print(e)

def confirmacion(mensaje):
    try: 

        global ventanaConfirmar, cantidadPasoFinal, tiempoConfirmar
        cantidadPasoFinal = 0
        ventanaPrincipal.pack_forget()
        ventanaConfirmar  = tk.Frame(window)
        ventanaConfirmar.pack(fill="both", expand="yes")

        avisoLabel = tk.Label(ventanaConfirmar, text = "    CIERRA EL FIXTURE Y BAJA LA PALANCA", font = ("arial", 25))
        avisoLabel.place(x= 20, y = 10)

        tiempoConfirmar = Timer(10.0, timerFunc, ["cerrar"])
        tiempoConfirmar.start()


        labeldb = tk.Label(ventanaConfirmar, image = imgdb)
        labeldb.place(x = sizeDic["FixtureX"], y = sizeDic["FixtureY"])


        btnConfirmar = tk.Button(ventanaConfirmar, text = "LISTO",activebackground = "green" ,command = lambda x = mensaje: enviarDatos(x, 1), font = ("arial", 20), bg = "green", width = 10, height = 8)
        btnConfirmar.place(x = sizeDic["BotonListoX"], y = sizeDic["BotonListoY"])
        btnCancelar = tk.Button(ventanaConfirmar, text = "CANCELAR",activebackground = "red", command = cerrarVentana, font = ("arial", 20), bg = "red", width = 10, height = 8)
        btnCancelar.place(x = sizeDic["BotonCancelarX"], y = sizeDic["BotonCancelarY"])
        #ventanaPrincipal.mainloop()
    except Exception as e:
        escribirLogFallas("confirmacion(): " + str(e))    

def enviarDatos(datos, confirmacion = 0):
    try:
        ser = serial.Serial('/dev/ttyS0',9600)  
        ser.write(datos.encode())
        ser.close()
        datos_entrada.focus()
        if confirmacion == 1:
            cerrarVentana()
            #print("IsGoldenGlobal" + str(isGoldenGlobal))
            ##print("GoldenGLobal = " + str(isGoldenGlobal))
            if isGoldenGlobal == 0:
                bloquearSeriales()
    except Exception as e:
        escribirLogFallas("enviarDatos(): " + str(e))

def askPassword():
    try:
        global ventanaPassword

        def pass_verify(password_reset):
            if password_reset == "aclara":
                cerrarVentanaPassword()
                panelDeControl()
                
            else: 
                label_password["fg"] = "red"
                input_password.delete('0', 'end')

        try:
            cerrarVentanaPassword()
        except:
            pass
        x = window.winfo_rootx()
        y = window.winfo_rooty()
        ventanaPassword = tk.Toplevel(bg = "ivory4")
        ventanaPassword.geometry("%dx%d+%d+%d" % (500, 300, x+200 , y+100))
        ventanaPassword.resizable(False, False)
        ventanaPassword.overrideredirect(1)

        label_password = tk.Label(ventanaPassword, text = "PASSWORD", font = ("arial", 20))
        label_password.pack(pady = 20)

        input_password = tk.Entry(ventanaPassword,  font = ("arial", 20))
        input_password.pack(pady = 20)
        input_password.focus()
        input_password.bind('<Return>', lambda event: pass_verify(input_password.get()))
        

        boton_cerrar = tk.Button(ventanaPassword ,text = "CANCELAR", command = cerrarVentanaPassword,  font = ("arial", 20))
        boton_cerrar.pack(pady = 20)
    except Exception as e:
        escribirLogFallas("askPassword(): " + str(e))    

def cerrarVentanaPassword():
    try: 
        ventanaPassword.destroy()
    except Exception as e:
        escribirLogFallas("cerrarVentanaPassword(): " + str(e))

def panelDeControl():
    try:
        def seleccionOpcionesPanel(opcionSel, btnObjeto):

            opcion1["bg"] = opcion2["bg"] = opcion3["bg"] = opcion4["bg"] = "grey"
            
            if btnObjeto["bg"] == "grey":
                btnObjeto["bg"] = "white"

            if opcionSel == 1:
                controlFrame.pack_forget()
                generalFrame.pack(side = tk.LEFT, fill = "y")
            if opcionSel == 2:
                generalFrame.pack_forget()
                controlFrame.pack(side = tk.LEFT, fill = "y")
        def salirPanel():
            ventanaPanel.pack_forget()
            ventanaPrincipal.pack(fill="both", expand="yes")

        ventanaPrincipal.pack_forget()
        ventanaPanel  = tk.Frame(window)
        ventanaPanel.pack(fill="both", expand="yes")
        letraSizeMenu = ("arial", 20)
        letraSizeTeclasC =  ("arial", 17)
        letraSizeGeneral = ("arial", 20)

        ############################################MENU##################################################vvv


        panelMenu =  tk.Frame(ventanaPanel, bg ="yellow")
        panelMenu.pack(side = tk.LEFT, fill = "y")

        opcion1 = tk.Button(panelMenu, text = "General", font = letraSizeMenu, width= 15, bg = "white", 
            command = lambda: seleccionOpcionesPanel(1, opcion1) )
        opcion1.pack()
        opcion2 = tk.Button(panelMenu, text = "Control Teclas", font = letraSizeMenu, width= 15, bg = "grey",
            command = lambda: seleccionOpcionesPanel(2, opcion2) )
        opcion2.pack()
        opcion3 = tk.Button(panelMenu, text = "Tiempo de Espera", font = letraSizeMenu, width = 15, bg = "grey")
        opcion3.pack()
        opcion4 = tk.Button(panelMenu, text = "Salir", font = letraSizeMenu, width = 15, bg = "grey",
            command = salirPanel)
        opcion4.pack()

        ############################################GENERAL##################################################vvv

        generalFrame = tk.Frame(ventanaPanel)
        generalFrame.pack(side = tk.LEFT, fill = "y")


        modoELabel = tk.Label(generalFrame, text = "MODO ESTRICTO ", font = letraSizeGeneral)
        modoELabel.grid(column = 1, row = 1)
        modoEBtn = tk.Button(generalFrame, text = modoESel, width = 3, font = letraSizeGeneral)
        modoEBtn.grid(column = 2, row = 1)

        bloqueoLabel = tk.Label(generalFrame, text = "BLOQUEAR SELECCIoN ", font = letraSizeGeneral)
        bloqueoLabel.grid(column = 1, row = 2)
        bloqueoBtn = tk.Button(generalFrame, text = bloqueoSel, width = 3, font = letraSizeGeneral)
        bloqueoBtn.grid(column = 2, row = 2)



        ############################################CONTROL TECLAS###########################################vvv

        controlFrame = tk.Frame(ventanaPanel)
        #controlFrame.pack(side = tk.LEFT, fill = "y")

        controlOpciones = tk.Frame(controlFrame)
        controlOpciones.pack(side = tk.LEFT, padx = 50)


        btnF11 = tk.Button(controlOpciones, text = "TEST PLAN", width= 10, font = letraSizeTeclasC, bg = "cyan"
        , command = lambda : enviarDatos("TESTPLAN"))
        btnF11.grid(column = 1, row = 0, pady = 15)
        btnF11 = tk.Button(controlOpciones, text = "F11", width= 8, font = letraSizeTeclasC, bg = "cyan"
        , command = lambda : enviarDatos("1111"))
        btnF11.grid(column = 1, row = 1, pady = 15)
        btnTab = tk.Button(controlOpciones, text = "Tab", width= 8, font = letraSizeTeclasC, bg = "cyan"
        , command = lambda : enviarDatos("TAB"))
        btnTab.grid(column = 1, row = 2, pady = 15)
        btnEnter = tk.Button(controlOpciones, text = "Enter", width= 8, font = letraSizeTeclasC, bg = "green"
        , command = lambda : enviarDatos("OK"))
        btnEnter.grid(column = 1, row = 3, pady = 15)
        btnEnter = tk.Button(controlOpciones, text = "Espacio", width= 8, font = letraSizeTeclasC, bg = "cyan"
        , command = lambda : enviarDatos("ESPACIO"))
        btnEnter.grid(column = 1, row = 4, pady = 15)


        
        btnAltF4 = tk.Button(controlOpciones, text = "Alt+F4", width= 8, font = letraSizeTeclasC, bg = "cyan"
        , command = lambda : enviarDatos("CERRAR"))
        btnAltF4.grid(column = 1, row = 5, pady = 90)

        flechasFrame = tk.Frame(controlFrame)
        flechasFrame.pack(side = tk.LEFT,  padx = 30)


        btnAr = tk.Button(flechasFrame, image = imgFlechaAr, command = lambda : enviarDatos("UP"))
        btnAr.grid(column = 2, row = 1)

        btnI = tk.Button(flechasFrame, image = imgFlechaI, command = lambda : enviarDatos("LEFT"))
        btnI.grid(column = 1, row = 2)
        btnD = tk.Button(flechasFrame, image = imgFlechaD, command = lambda : enviarDatos("RIGHT"))
        btnD.grid(column = 3, row = 2)
        btnAb = tk.Button(flechasFrame, image = imgFlechaAb, command = lambda : enviarDatos("DOWN"))
        btnAb.grid(column = 2, row = 3)


        ventanaPanel.mainloop()
    except Exception as e:
        escribirLogFallas("panelDeControl(): " + str(e))

def cerrarVentana():
    try:
        global filtro, cantidad_escaneo, cantidad, serialesArr
        global tiempoConfirmar
        tiempoConfirmar.cancel()
        ventanaConfirmar.destroy()
        ventanaPrincipal.pack(fill="both", expand="yes")
        cantidad_escaneo  = 0
        texto_seleccion = "0" + "/" + str (cantidad)
        cantidad_seleccion["text"] = texto_seleccion
        serialesArr = []
        datos_entrada.focus()
        limpiarCampo()
    except Exception as e:
        escribirLogFallas("cerrarVentana(): " + str(e))    

def initConf():
    try:
        global modoESel, bloqueoSel
        try:
            archivoconf = open('conf.conf', 'r')
        except: 
            archivoconf = open('/oktotest_pmc/conf.conf', 'r')
        textosBtn = []
        while True:
            line = archivoconf.readline()
            if re.search("=1", line):
                textosBtn.append("Si")
            else:
                textosBtn.append("NO")

            if not line:
                break

        archivoconf.close()
        modoESel = textosBtn[0]
        bloqueoSel = textosBtn[1]
    except Exception as e:
        escribirLogFallas("initConf(): " + str(e))

def testtime(tiempo):
    try:
        formatodia = tiempo[0: tiempo.find("T")]
        formatohora = tiempo[tiempo.find("T") + 1: tiempo.find("T") + 9]
        formatodiaarray =  formatodia.split("-")
        formatohoraarray = formatohora.split(":")
        anio = int(formatodiaarray[0])
        mes = int(formatodiaarray[1])
        dia = int(formatodiaarray[2])

        h = int(formatohoraarray[0])
        m = int(formatohoraarray[1])
        s = int(formatohoraarray[2])

        diferencia = datetime(anio, mes, dia, h, m, s)

        duracion = datetime.now() - diferencia
        duracionsegundos = duracion.total_seconds()
        duracionminutos = duracionsegundos/60

        #print(duracionminutos)
        try:
            archivotexto = open('testtime.txt', 'r')
        except: 
            archivotexto = open('/oktotest_pmc/testtime.txt', 'r')

        resultado = []
        while True:
            
            line = archivotexto.readline()
            if re.search(modelo + "=", line):
                minutosespera = line.split("=")[1]
                if duracionminutos < int(minutosespera):
                    archivotexto.close()
                    resultado = [minutosespera ,str(int(duracionminutos)), False]
                    return resultado
                else:
                    archivotexto.close()
                    resultado = ["", "", True]
                    return resultado
            if not line:
                break
        resultado = ["", "", True]
        archivotexto.close()
        return resultado
    except Exception as e:
        escribirLogFallas("testtime(): " + str(e))

# def revisarSerialesBloqueados(serial):
#     try:
#         puedeProbarse = 1
        
#         try:
#             ruta = "serialesbloqueados.txt"
#             listaBloqueadostxt = open(ruta, "r")
#         except: 
#             ruta = "/oktotest_pmc/serialesbloqueados.txt"
#             listaBloqueadostxt = open(ruta, "r")

        
#         #listaBloqueadostxt.seek(0)
#         while True:
#             linea = listaBloqueadostxt.readline()
#             if not linea:
#                 break
            
#             if re.search(serial, linea):
                
#                 diferencia =  datetime.now() - datetime.fromisoformat(linea.split("#T")[1].strip())
#                 diferenciasegundos = diferencia.total_seconds()
#                 diferenciaminutos = int(diferenciasegundos/60)
#                 ##print(diferenciaminutos)
#                 ##print(diferenciaminutos<10)
#                 if diferenciaminutos<10:
#                     puedeProbarse = 0

        
#         listaBloqueadostxt.close
#         return puedeProbarse
#     except Exception as e:
#         escribirLogFallas("revisarSerialesBloqueados(): " + str(e))

def bloquearSeriales():
    try:
        global seriales2DArray
        arrayListaBloqueados = []
        try:
            ruta = "serialesbloqueados.txt"
            listaBloqueadostxt = open(ruta, "r")
        except: 
            ruta = "/oktotest_pmc/serialesbloqueados.txt"
            listaBloqueadostxt = open(ruta, "r")
        #os.remove(ruta)
        arrayListaBloqueados = listaBloqueadostxt.readlines()
        listaBloqueadostxt.close()

        listaBloqueadostxt = open(ruta, "w")
        for serial in seriales2DArray:
            arrayListaBloqueados.append(serial+" #T"+ str(datetime.now())+"\n" )
            ##print(arrayListaBloqueados)
            if len(arrayListaBloqueados) > 10:
                arrayListaBloqueados.pop(1)
        listaBloqueadostxt.writelines(arrayListaBloqueados)
        listaBloqueadostxt.close()
    except Exception as e:
        escribirLogFallas("bloquearSeriales(): " + str(e))

def escribirLeerMasterDeGolden(serial2DG, serialMasterG = ""):
    flagG = 0
    try:
        ruta = "serialesMasterGolden.txt"
    except: 
        ruta = "/oktotest_pmc/serialesMasterGolden.txt"
    if serialMasterG == "":
        try: 
            masterGFSO = open(ruta, "r")
        except:
            masterGFSO = open(ruta, "x")
            masterGFSO.close()
            return

        while True:
                linea = masterGFSO.readline()
                if not linea:
                    break

                if re.search(serial2DG, linea):

                    serialMasterG = linea.split(":")[1].strip()
                    flagG = 1
                    break
        if flagG == 1:
            masterGFSO.close()
            return serialMasterG
        else:
            masterGFSO.close()
            return False
    else:
        masterGFSO = open(ruta, "a")
        masterGFSO.write(serial2DG+":"+serialMasterG+"\n")
        masterGFSO.close()

def escribirLogFallas(error):
    
    try:
        ruta = "log.txt"
        log = open(ruta, "a")
    except: 
        ruta = "/oktotest_pmc/log.txt"
        log = open(ruta, "a")

    log.write(error + "   " + str(datetime.now()) + "\n")
    log.write("-----------------------------------------------------------------" + "\n")
    log.close()

iniciar()
initConf()
seleccionEscaneo(reset=1)

window.mainloop()
