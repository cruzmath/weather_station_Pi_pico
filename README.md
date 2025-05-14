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

## Componentes utilizados

## Linguagem usada

## Código

## Resultados
