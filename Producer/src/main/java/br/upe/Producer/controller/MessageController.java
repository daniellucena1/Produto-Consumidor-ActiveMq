package br.upe.Producer.controller;

import br.upe.Producer.services.MessageProducer;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
public class MessageController {

    private final MessageProducer messageProducer;

    public MessageController(MessageProducer messageProducer) {
        this.messageProducer = messageProducer;
    }

    @PostMapping("/send/{message}")
    public String sendMessage(@PathVariable String message) {
        messageProducer.sendMessage(message);
        return "Mensagem enviada: " + message;
    }
}
