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

Os motores sem escovas têm um princípio de funcionamento relativamente complexo, sendo operados por um sinal *AC* trifásico criado pelas unidades *ESC* a partir de um sinal *PWM* (*Pulse Width Modulation*).

Sendo assim, o esquema de controlo é efetivamente análogo ao de um servomotor, bastando fornecer à *ESC* um sinal *PWM* com frequência de $50 \, Hz$, amplitude de $5 \, V$ e *duty-cycle* entre $[10,\, 15]\,\%$. Assim, a potência dos motores é controlada diretamente fazendo variar o *duty-cycle* do sinal *PWM*.

<span style="color:red">Adicionar representação do sinal PWM e do sinal 'pós-ESC'</span>

As unidades *ESC* utilizadas contém ainda um *Battery Eliminator Circuit* (*BEC*), pelo que o sistema necessitaria de apenas uma bateria para alimentar tanto a *ESC* ($5\,V$) e o motor ($8-12\,V$). Contudo, como a estrutura tem apenas 1 grau de liberdade, optamos por alimentar o motor com uma fonte externa, evitando recorrer ao uso de baterias.

<span style="color:red">Adicionar esquema da ligação da ESC no circuito</span>

Considerando que a placa *ESP32* funciona em lógica de $3.3 ~V$, para alimentar a *ESC* e gerar o sinal *PWM* adequado, é necessário ainda subir a sua tensão para *5 ~ V*.

Numa primeira montagem, isto foi feito recorrendo a dois amplificadores operacionais *TL081* em configuração não-inversora (um para cada sinal *PWM*). Escolhendo para as resistências $R_1$, $R_2$ valores satisfazendo $R_2 \approx 0.51 R_1$, obtém-se o ganho necessário.

Entretanto, esta montagem não é eficiente em termos de custo e de espaço. Com isto em mente, simplificamos o circuito introduzindo para tal um *Bi-directional Logic Level Converter* (*LLC*) (*SparkFun*).

Como este integrado contém 4 canais para conversão, consegue-se realizar todas as conversões necessárias recorrendo-se a apenas uma unidade.

<span style="color:red">Adicionar esquema dos Opamps</span>


<span style="color:red">Adicionar esquema do LLC</span>

# Sensor

O sensor *MPU6050* escolhido contém um acelerómetro de 3 eixos e um giroscópio.

O protocolo de comunicação em série adotado pelo dispositivo é o *I2C*. Tratando-se de um protocolo síncrono, a comunicação é estabelecida por 2 fios (*SDA* - *Serial Data*, *SCL* - *Serial Clock*).

<span style="color:red">To do: adicionar esquema de ligação do sensor na ESP <span>

A linguagem *MicroPython* contém as funções básicas para estabelecer este tipo de comunicação, sendo o sinal do relógio e a emissão dos *bits* feita automaticamente. Sendo assim, recorrendo à *datasheet* do sensor, basta ler os endereços corretos para aceder aos dados desejados.

<span style="color:red">To do: inserir print da datasheet onde estão os endereços do acelerometro e girscópio <span>

É importante notar que cada medição é representada 16 *bits*, em complemento para 2, mas estão armazenadas em dois registros de 8 *bits* cada. Sendo assim, é necessário agregar a informação dos dois registros num único valor para obter o resultado da medição. O método mais eficiente encontrado, em termos de código, recorre a operações binárias. O algoritmo é descrito a seguir:

- Ler os 8 *bits* mais significativos e armazenar na variável $n_1$; 
- Realizar um *bitshift* de 8 dígitos para esquerda (i.e dividir por $2^8$);
- Ler os 8 *bits* menos significativos e armazenar na variável $n_2$; 
- Aplicar operador lógico *or* entre os *bits* em $n_1, \, n_2$

<span style="color:red">To do: adicionar ilustração (exemplo) deste algoritmo <span>

Assim, com duas operações conseguimos reconsturir o número de 16 *bits*, restando agora sua conversão entre complemento para 2 e decimal:

- Inverter valor lógico dos *bits*
- Adicionar $1$

Reliazar estas operações de modo eficiente é importante para que a latência vinda da execução do código não prejudique a taxa de amostragem. 

Outro aspecto importante é notar que os valores obitdos pela conversão acima não correspondem às unidades esperadas (e.g $\deg / s$ para leitura do giroscópio). Os valores de conversão são também encontrados na *datasheet* e dependem dos valores fim-de-escala escolhidos para cada componente do sensor. 

- Giroscópio:  $131.0 \,\, \textrm{LSB}/\deg/s$
- Acelerómetro: $16384 \,\, \textrm{LSB}/g$

Estes valores correspondem a escalas de $\pm 250 \deg/s$ para a leitura do giroscópio e $\pm 2g$ para leitura do acelerómetro. Estas configurações, dentre as disponíveis, foram as escolhidas a gama de medição esperada as preenche bem (o que implica numa maior resolução).

# Algoritmo PID

Para realizar o controlo dos motores, utilizou-se um algoritmo *PID* (*Proportional, Integral, Differential*).

O algoritmo baseia-se em calcular o ajuste necessário à potência dos motores, de modo a manter o valor de $\theta$ medido pelo sensor próximo a um valor fixado (*setpoint*) $\theta_{sp} = 0^{\small{\circ}}$. A resposta $u$ é então calculada a partir do erro $e = \theta - \theta_{sp}$ como:

$$
u = K_p e + \frac{1}{T_d}\frac{de}{dt} + \frac{1}{T_i}\int e\,\,dt \equiv P + D + I
$$

As constantes $K_p$, $T_i$ (tempo de integração) e $T_d$ são determinadas empiricamente por um processo de calibração.

O termo *P* é a contribuição mais fundamental para o controlador, que faz com que a resposta do sistema seja tão maior quanto o erro. Contudo, esta contribuição se utilizada sozinha levaria a transientes longos e o ponto de operação do sistema teria $u \ne 0$. A inclusão do termo $D$ ajuda a diminuir a duração do transiente, pois ajusta a resposta no tempo presente baseando-se numa estimativa do erro no instante seguinte. Por outro lado, o sistema ainda poderia estabilizar em torno de um ponto de equilíbrio diferente de $\theta_{sp}$, pelo que o termo $I$ garante que nesta situação, o erro seja eventualmente compensado uma vez que é acumulado ao longo do tempo (sendo $u$ atualizado de modo correspondente).

Para implementar este algoritmo com o microcontrolador, seguiu-se as indicações encontradas no livro 
<span style="color:red">Incluir referencia do livro do Astrom</span>

# Comunicação Wi-Fi

<span style="color:red">To do...</span>

# Resultados

<span style="color:red">To do...</span>