import cv2
import mediapipe as mp
import os

# IA que captura a cara do individuo
mp_face_mesh=mp.solutions.face_mesh
face_mesh=mp_face_mesh.FaceMesh(max_num_faces=1)
#Max num faces é pra deixar bem claro que ele só vai procurar a cara de uma pessoa.

# Na teoria o ID padrão da camera é 0 (Verificar depois)
cam = cv2.VideoCapture(0)

#       ------------------- FUNCOES DE LOGICA --------------------

def calculo_boca(face_landmarks):
    labio_sup=face_landmarks.landmark[13]
    labio_inf=face_landmarks.landmark[14]

    # ARRUMANDO O PROBLEMA DA ESCALA
    altura=abs(labio_sup.y-labio_inf.y)
    largura = abs(face_landmarks.landmark[61].x - face_landmarks.landmark[291].x)

    
    ratio=altura/(largura+0.001)

    if ratio>0.35:
        return True
    else:
        return False
    
def olho_arregalado(face_landmarks):
    
    # ARRUMANDO O PROBLEMA DA ESCALA

    #Olho Esquerdo
    palp_sup_e=face_landmarks.landmark[159]
    palp_inf_e=face_landmarks.landmark[145]
    altura_e=abs(palp_sup_e.y-palp_inf_e.y)
    largura_e=abs(face_landmarks.landmark[33].x-face_landmarks.landmark[133].x)
    ratio_e=altura_e/(largura_e+0.001)

    #Olho Direito
    palp_sup_d=face_landmarks.landmark[386]
    palp_inf_d=face_landmarks.landmark[374]
    altura_d=abs(palp_sup_d.y-palp_inf_d.y)
    largura_d=abs(face_landmarks.landmark[362].x - face_landmarks.landmark[263].x)

    ratio_d=altura_d/(largura_d+0.001)
    # Calculando a média (pra testar precisao)
    media=(ratio_d+ratio_e)/2

    if media>0.55:
        return True
    else:
        return False
    
def olho_fechado(face_landmarks):

    #Olho Esquerdo
    palp_sup_e=face_landmarks.landmark[159]
    palp_inf_e=face_landmarks.landmark[145]
    altura_e=abs(palp_sup_e.y-palp_inf_e.y)
   
    largura_e=abs(face_landmarks.landmark[33].x-face_landmarks.landmark[133].x)
    ratio_e=altura_e/(largura_e+0.001)

    #Olho Direito
    palp_sup_d=face_landmarks.landmark[386]
    palp_inf_d=face_landmarks.landmark[374]
    altura_d=abs(palp_sup_d.y-palp_inf_d.y)

    largura_d=abs(face_landmarks.landmark[362].x - face_landmarks.landmark[263].x)

    ratio_d=altura_d/(largura_d+0.001)
    media=(ratio_d+ratio_e)/2
    return media

frames_olho_fechado = 0
OLHO_FECHADO_ESTADO = False

#   Funcao verifica sorriso 
def sorriso(face_landmarks):
    boca_esq=face_landmarks.landmark[61]
    boca_dir=face_landmarks.landmark[291]

    largura_boca=abs(boca_esq.x-boca_dir.x)

    bochecha_e=face_landmarks.landmark[234]
    bochecha_d=face_landmarks.landmark[454]
    largura_rosto=abs(bochecha_e.x-bochecha_d.x)

    ratio=largura_boca/(largura_rosto+0.001)

    if ratio>0.46:
        return True
    else:
        return False

def boca(face_landmarks):
    lab_sup=face_landmarks.landmark[13]
    lab_inf=face_landmarks.landmark[14]

    boca_esq=face_landmarks.landmark[61]
    boca_dir=face_landmarks.landmark[291]

    altura_boca=abs(lab_sup.y-lab_inf.y)
    largura_boca=abs(boca_esq.x-boca_dir.x)

    ratio=altura_boca/(largura_boca+0.001)

    if ratio>0.35:
        return True
    else:
        return False
    
#           -TENTANDO ARRUMAR OUTRO PROBLEMA DE PERSPECTIVA

# Tenta determinar o quao inclinado meu rosto ta baseado na distancia do nariz até os...
#... pontos extremos da minha cara
def fator_inclinacao(face_landmarks):
    topo = face_landmarks.landmark[10]
    nariz = face_landmarks.landmark[1]
    queixo = face_landmarks.landmark[152]

    dist_cima = abs(topo.y - nariz.y)
    dist_baixo = abs(nariz.y - queixo.y)


    ratio = dist_cima / (dist_baixo+0.001)
    return ratio


#Loop infinito das infinitas fotos sendo tiradas pra formar o video da camera
while True:
    
    #ret retorna True se der tudo certo, e o frame é só o frame mesmo 
    # cam.read() ta retornando uma tupla, um booleano e um frame
    ret, frame = cam.read()

    #Caso nao funcione, sai do loop
    if not ret:
        break

    #Imagem originalmente espelhada, esse funcao desespelha
    frame=cv2.flip(frame,1)
    #Converte BGR em RGB
    frame_rgb=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #Funcao pra procurar o rosto (resultado guardado variavel)
    resultados=face_mesh.process(frame_rgb)

    imagem_gato="assets/dinho_neutro.png"

    if resultados.multi_face_landmarks:
        #Rosto de indice 0, primeiro e unico rosto que aparece.
        rosto=resultados.multi_face_landmarks[0]

        inclinacao=fator_inclinacao(rosto)
        limite_dormindo=0.455

        #Quanto menor a inclinacao, mais pra cima eu olho
        if inclinacao<0.88:
            limite_dormindo=0.30

        #Quanto maior a inclinacao, mais pra baixo eu olho
        elif inclinacao>1.50:
            limite_dormindo=0.50

        ratio_atual=olho_fechado(rosto)


        if ratio_atual<limite_dormindo:
            frames_olho_fechado+=1
        else:
            frames_olho_fechado=0
            OLHO_FECHADO_ESTADO=False
        
        if frames_olho_fechado>10:
            OLHO_FECHADO_ESTADO=True

        #Tamanho da imagem da camera
        altura,largura, _ = frame.shape

        if olho_arregalado(rosto):
            imagem_gato="assets/gato_arregalado.png"
            
        elif sorriso(rosto):
            imagem_gato="assets/gato_sorrindo.png"

        elif OLHO_FECHADO_ESTADO:
            imagem_gato="assets/gato_dormindo.png"

    cv2.imshow('Camera_Orig', frame) #Vai abrir uma janela com a camera e o frame atual (Considerando o loop, é só uma janela com a camera ligada)

    #Criando a segunda janela
    img_gato=cv2.imread(imagem_gato)

    if img_gato is not None:
        img_gato_resized=cv2.resize(img_gato,(400,400))
        
        cv2.imshow('Gatito Reacao', img_gato_resized)
    else:
        print("caminho da imagem ta errado")

    tecla=cv2.waitKey(1)    # Apertar ESC pra fechar sair do loop.
    if tecla==27:
        break


#Provavelmente a ultima parte do programa
#Caso o loop acabe, fecha TUDO
cam.release()
cv2.destroyAllWindows()


