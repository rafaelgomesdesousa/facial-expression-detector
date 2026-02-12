# Real Time Facial Expression Detector

Detector de expressões faciais em tempo real desenvolvido em Python, utilizando **MediaPipe** e **OpenCV**. O projeto captura a webcam e reage as expressões do usuário (olhos fechados, olhos arregalados e sorriso)
exibindo imagens correspondentes na tela.

## Correção de perspectiva
O maior desafio desse projeto foi lidar com a geometria facial quando o usuário inclina a cabeça.
- Problema: Ao olhar para cima, a distância entre as pálpebras superiores e inferiores diminuía devido a perspectiva, gerando "falsos positivos" de olhos fechados. Ao inclinar a cabeça para baixo, o oposto ocorria.
- Solução: Implementei um algoritmo de **Dynamic Thresholding**. O código calcula a inclinação vertical da face (relação testa-nariz vs. nariz-queixo) e ajusta a sensibilidade da detecção dos olhos.

## Tecnologias Utilizadas
- **Python 3.10**
- **OpenCV**
- **MediaPipe**
- **NumPy**

## Funcionalidades
**Detecção de Estados:**
- Neutro
- Sorrindo (Cálculo de largura da boca vs. rosto)
- Surpreso/Olho Arregalado
- Dormindo/Olho Fechado (Com estabilização de frames para evitar flickering)

## Como rodar o projeto

1. Clone o repositório: bash
   git clone https://github.com/rafaelgomesdesousa/facial-expression-detector.git
2. Instale as dependências: pip install opencv-python mediapipe numpy
3. Execute o arquivo principal: main.py
