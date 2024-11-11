package com.example.verime.config;

//import com.example.verime.config.GlobalVariables;

import net.dv8tion.jda.api.events.message.MessageReceivedEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;

public class CommandHandler extends ListenerAdapter {
    @Override
    public void onMessageReceived(MessageReceivedEvent event) {
        String message = event.getMessage().getContentRaw();
        
        if (message.startsWith("!setage")) {
            // Example: !setage 25
            String[] parts = message.split(" ");
            if (parts.length > 1) {
                String age = parts[1];
                event.getChannel().sendMessage("Age set to: " + age + " years.").queue();
                GlobalVariables.minAge = Integer.parseInt(age);   
            }
        }
    }
}

