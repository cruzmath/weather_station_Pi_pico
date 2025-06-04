from machine import Pin,I2C
from bmp280 import *
import time
import socket
import network
import dht

# Definições
sdaPIN = Pin(18)
sclPIN = Pin(19)
dhtPIN = Pin(16)
wifi_name = "projeto_ea801"
wifi_password = "projeto_ea801"

# Configurações WIFI
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(wifi_name, wifi_password)

# Conexões
bus = I2C(1,sda=sdaPIN, scl=sclPIN, freq=400000)

# Configurações sensores
bmp = BMP280(bus)
bmp.use_case(BMP280_CASE_INDOOR)
sensor = dht.DHT22(dhtPIN)

sensor_data = [] #lista para guardar os dados dos sensores em forma de linhas para tabela html

# Função para conectar ao wifi
# Recebe um parâmetro opcional tentativas que representa o número de tentativas e retorna o servidor
def wifi_connect(tentativas = 10):
    # Esperando se conectar ou falhar
    while tentativas > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        tentativas -= 1
        print('Esperando conexão...')
        time.sleep(1)

    # Lidar com erros de conexão
    if wlan.status() != 3:
        raise RuntimeError('Conexão wifi falhou')
    else:
        print('Conectado')
        ip=wlan.ifconfig()[0]
        print('IP: ', ip)
    
    # Abrir socket
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', 80))
    server.listen(5)
    print('ouvindo em', addr)
    
    return server
    
# Função para ler a temperatura e a pressão do bmp280
# Não requer nenhum parâmetro e retorna a temperatura e a pressão
def get_temp_press():
    try:
        pressure=bmp.pressure
        p_bar=pressure/100000
        p_mmHg=pressure/133.3224
        temperature=bmp.temperature
        print("Temperatura: {} C".format(temperature))
        print("Pressão: {} Pa, {} bar, {} mmHg".format(pressure,p_bar,p_mmHg))
        return temperature, pressure
    except:
        print("Erro no bmp280")
        return 0, 0
    
# Função para ler a umidade do dht22
# Não requer nenhum parâmetro e retorna a temperatura e a umidade
def get_umid():
    try:
        sensor.measure()
        temp_dht = sensor.temperature()
        umid = sensor.humidity()
        print("Umidade relativa {} %".format(umid))
        return temp_dht, umid
    except:
        print("Erro no dht22")
        return 0, 0

# Função para ler o tempo atual do rtc
# Não requer nenhum parâmetro e retorna o tempo 
def get_time():
    try:
        pass
    except:
        print("Erro no rtc")
        return 0

# Atualiza as linhas da tabela a cada 5 segundos
def update_table(time, temp_bmp, temp_dht, press, umid):
    sensor_data.append(f"<tr><td>{time}</td><td>{temp_bmp}</td><td>{temp_dht}</td><td>{press}</td><td>{umid}</td></tr>")

# Função para configurar a página web
# Recebe os valores de tempo, temperatura, pressão e umidade através da lista sensor_data e retorna o html para o site
def web_page():
    table_content = "\n".join(sensor_data)
    html = f"""<html><head>
        <meta http-equiv="refresh" content="5">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta charset="utf-8"/>
        <style>
            body {{ text-align: center; font-family: Helvetica, Arial; }}
            table {{ border-collapse: collapse; width:55%; margin-left:auto; margin-right:auto; border: 2px solid black;}}
            th {{ padding: 12px; background-color: #87034F; color: white; text-align: center;}}
            tr:nth-child(odd) {{ background-color: #f2f2f2; }}  <!-- Cor para linhas ímpares -->
            tr:nth-child(even) {{ background-color: #ffffff; }} <!-- Cor para linhas pares -->
            tr:hover {{ background-color: #bcbcbc; }}
            td {{ border: none; padding: 14px; text-align: center;}}
            .sensor {{ color:DarkBlue; font-weight: bold; background-color: #ffffff; }}
        </style>
    </head>
    <body>
        <h1>BMP280 + DHT22 Pi Pico W Estação Climática</h1>
        <table>
            <tr><th>Hora</th><th>Temp BMP [°C]</th><th>Temp DHT [°C]</th><th>Pressão [Pa]</th><th>Umidade [%]</th></tr>
            {table_content}
        </table>
    </body></html>"""
    return html.encode("utf-8")

server = wifi_connect()

while True:
    try:
        conn, addr = server.accept()
        conn.settimeout(3.0)
        print('client connected from', addr)
        request = conn.recv(1024)
        conn.settimeout(None)
        # Receber HTTP-Request
        print('Request:', request)              
        # Enviar HTTP-Response
        temp_bmp, press = get_temp_press()
        temp_dht, umid = get_umid()
        time = get_time()
        update_table(time, temp_bmp, temp_dht, press, umid)
        response = web_page()
        conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        conn.sendall(response)
        conn.close()
    except OSError as e:
        conn.close()
        print('conexão fechada')
