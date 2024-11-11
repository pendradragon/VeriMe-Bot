package com.example.verime;

import net.dv8tion.jda.api.JDABuilder;
import net.dv8tion.jda.api.entities.Activity;
import javax.security.auth.login.LoginException;

public class Bot {
    public static void main(String[] args) throws LoginException {
        String token = System.getenv("DISCORD_TOKEN");
        JDABuilder builder = JDABuilder.createDefault(token);
        builder.setActivity(Activity.playing("Hello World!"));
        builder.build();
    }
}

