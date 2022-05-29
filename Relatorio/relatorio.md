# Relatório - Projeto Integrador
## 2º Semestre / 2022, L:EF
## Felipe Coutinho e Cauã Veiga

# Introdução

O projeto desenvolvido consiste num controlador para equilíbrio em 1 dimensão de um protótipo de *drone*. Consiste na implementação de um algoritmo PID num microcontrolador *ESP32-PICO-KIT*, de modo a estabilizar o eixo longitudinal de uma haste com motores ligados a hélices nas extremidades e um eixo de rotação no seu centro geométrico.

Para isso, foram utilizados motores sem escovas obtidos a partir de um *drone* inativo que foi cedido para efeito deste trabalho. Estes motores foram por sua vez controlados pela *ESP32*, através de unidades ESC (*Electronic Speed Control*), também retiradas do *drone*. Ainda, utilizou-se um sensor *MPU6050*, que integra um acelerómetro de 3 eixos e um giroscópio. 

Finalmente, de modo a obter informação quantitativa sobre a estabilização, se aproveitou das funcionalidades *Wi-Fi* da placa para, a partir de um servidor hospedado nela, acessar aos dados em tempo real por computadores conectados à mesma rede.

Nota-se ainda que a escolha da placa favoreceu a programação na linguagem *MicroPython*.

# Controlo dos motores

<span style="color:red">Adicionar explicação sobre funcionamento dos brushless motors e vantagens para seu uso em drones</span>

Os motores sem escovas têm um princípio de funcionamento relativamente complexo, sendo operados por um sinal *AC* trifásico criado pelas unidades *ESC* a partir de um sinal *PWM* (*Pulse Width Modulation*). Sendo assim, o esquema de controlo é efetivamente análogo ao de um servomotor, bastando fornecer à *ESC* um sinal *PWM* com frequência de $50 \, Hz$, amplitude de $5 \, V$ e *duty-cycle* entre $[10,\, 15]\,\%$. Assim, a potência dos motores é controlada diretamente fazendo variar o *duty-cycle* do sinal *PWM*.

<span style="color:red">Adicionar representação do sinal PWM e do sinal 'pós-ESC'</span>

<span style="color:red">Adicionar esquema da ligação da ESC no circuito</span>

# Sensor

<span style="color:red">To do...</span>

# Algoritmo PID

<span style="color:red">To do...</span>

# Comunicação Wi-Fi

<span style="color:red">To do...</span>

# Resultados

<span style="color:red">To do...</span>