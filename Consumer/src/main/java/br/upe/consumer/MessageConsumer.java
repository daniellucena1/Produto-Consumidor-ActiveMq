package br.upe.consumer;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.jms.annotation.JmsListener;
import org.springframework.stereotype.Component;

@Component
public class MessageConsumer {

    private static final Logger log = LoggerFactory.getLogger(MessageConsumer.class);

    @Value("${app.queue.name}")
    private String queueName;

    @JmsListener(destination = "${app.queue.name}")
    public void receive(String message) {
        log.info("Mensagem recebida da fila '{}': {}", queueName, message);
    }
}
