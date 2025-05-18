# Estação climática com Pi Pico

## Descrição do Projeto

O objetivo do projeto foi desenvolver um sistema que possua a capacidade de medir dados climáticos do ambiente e enviá-los a um servidor web para melhor visualização e possível armazenamento.

### Diagrama 

O diagrama abaixo apresenta o fluxo da informação no sistema
```mermaid
graph LR
A[Pi Pico] <-->|Wi-Fi| B[Servidor Web]
C[BMP280] <-->|I2C| A
D[DHT22] <-->|OneWire| A
```

### Funcionamento esperado

Do diagrama anterior, deverá se estabelecer uma conexão física entre os dois sensores e a a Pico para que a comunicação entre ambos seja possibilitada. Além disso, será necessário desenvolver um código que possibilite a leitura das informações provenientes deles. Após a leitura, deverá ser necessário desenvolver uma página web (website) para apresentar os dados no navegador e escolher como a conexão entre essa página se dará.

Em suma, seguimos os seguintes passos para desenvolver o sistema:
1. Conectar fisicamente todos os componentes;
2. Desenvolver duas funções (uma para cada sensor) para coletar as informações que eles enviam;
3. Criar uma página web em html, por simplicidade;
4. Criar uma função que conecte o microcontrolador à internet;
5. Escolher o protocolo de comunicação do micro para a internet;
6. Fazer um loop infinito que abrigue as funcionalidades do software que sempre deverão ser refeitas (leitura e envio dos dados);

### Protocolo de comunicação com a internet

Os outros pontos ou são auto explicativos, ou serão explicados na seção "Código", mas esse é necessário uma maior explicação sobre o motivo de termos escolhido sockets para nos comunicarmos com a internet.
Poderíamos utilizar o protocolo HTTP e fazer, por exemplo, requisição do tipo POST para atualizar o website, porém isso se tornaria mais lento e, como não possuímos um DNS, iria ser necessário fazer essas requisições para um endereço de IP a cada atualização. Esse procedimento, além de trabalhoso, não seria eficaz pela necessidade de passar novamente todas as informações em um body com algum tipo de autenticação para que outros na mesma rede não consigam enviar requisições.

Por isso, o melhor procedimento para esse caso é o socket. Ele abre uma requisição e mantém a conexão aberta para continuar com o envio de dados sem que seja necessário passar todos os parâmetros da requisição novamente, apenas os dados que necessitam ser atualizados.

## Componentes utilizados
Neste projeto foram utilizados 2 sensores diferentes para obter todas as informações climáticas relevantes. Estes são
* DHT22: Obtém dados de temperatura e umidade relativa do ar
* BMP280: Obtém dados de temperatura e pressão atmosférica
* Placa de desenvolvimento BITDOGLAB com o microcontrolador Raspberry Pi Pico
* Jumpers e protoboard para conectar os sensores à placa

## Linguagem usada
Utilizou-se a linguagem micropython devido à facilidade na configuração de componentes e a grande disponibilidade de bibliotecas compatíveis com os sensores e as funcionalidades utilizadas.
Bibliotecas utilizadas:
* machine
* bmp280
* time
* socket
* network
* dht

obs: A biblioteca bmp280 não é nativa do micropython. Dessa forma, usando a IDE Thonny, o arquivo bmp280.py foi salvo na Pico para que fosse possível usar os recursos dela.

## Código

O código principal está no arquivo `main.py` e abriga todas as funções bem como o seu método de uso.

Algo relevante a se comentar é que os dados do wifi foram *hardcoded* no código, o que não é recomendado, tendo sido feito apenas por simplicidade. O ideal seria criar variáveis de ambiente para armazenar esses valores e apenas usar eles sem explicitá-los.

Após as definições das constantes do projeto: [Pinos dos sensores, nome e senha do wifi, tipo do sensor DHT: 11 ou 12, são definidas as funções explicitadas na subseção "Funcionamento esperado", em que:
* `wifi_connect`: Função para conectar ao wifi. Recebe um parâmetro opcional tentativas que representa o número de tentativas e retorna o servidor.

* `get_temp_press`: Função para ler a temperatura e a pressão do BMP280. Não requer nenhum parâmetro e retorna a temperatura e a pressão.

* `get_umid`: Função para ler a umidade do DHT22. Não requer nenhum parâmetro e retorna a umidade.

* `web_page`: Função para configurar a página web.# Recebe os valores de temperatura (BMP e DHT), pressão e umidade e retorna o html para o site.

## Resultados
O resultado está apresentado na imagem abaixo, que mostra o funcionamento do site, com os valores recebidos pela Pico através do Wi-Fi.

![Imagem do WhatsApp de 2025-05-14 à(s) 17 02 26_065a8d4a](https://github.com/user-attachments/assets/bd94dccf-d87c-441f-8083-2d991b25831e)

A seguir, temos um vídeo que mostra o site se atualizando em tempo real com novos dados a cada 5s.


https://github.com/user-attachments/assets/a16f1e07-73cd-4090-8fcb-7ba2206d0394
