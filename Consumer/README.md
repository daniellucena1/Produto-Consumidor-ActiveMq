# Consumer (ActiveMQ + Spring Boot)

Este projeto implementa um **consumidor JMS** para ActiveMQ usando Spring Boot.
Ele escuta uma fila configurável (por padrão `test`) e registra as mensagens recebidas.

## Requisitos
- Java 21
- Maven 3.9+
- ActiveMQ disponível (ex.: via `docker-compose.yml` do seu repositório)

## Configuração
As principais variáveis podem ser definidas via ambiente:
- `ACTIVEMQ_BROKER_URL` (default: `tcp://localhost:61616`)
- `ACTIVEMQ_USER` (default: `admin`)
- `ACTIVEMQ_PASSWORD` (default: `admin`)
- `QUEUE_NAME` (default: `test`)

> **Importante:** Ajuste `QUEUE_NAME` para bater com a fila usada pelo Producer.
No seu Producer atual, o código envia para **`"test"`**.

## Como rodar
1. Suba o ActiveMQ (ex.: `docker compose up -d`).
2. Rode o Consumer:
   ```bash
   mvn spring-boot:run
   ```

Com o Producer em execução, você deverá ver logs como:
```
Mensagem recebida da fila 'test': Hello World
```
