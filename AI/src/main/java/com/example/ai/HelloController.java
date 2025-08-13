package com.example.ai;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.control.Label;
import javafx.scene.control.TextArea;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class HelloController {
    @FXML
    private Label outputLabel;

    @FXML
    private TextArea textarea;

    @FXML
    void analyser(ActionEvent event) {
        try {
            String inputText = textarea.getText().trim();
            if (inputText.isEmpty()) {
                outputLabel.setText("⚠️ الرجاء إدخال نص.");
                return;
            }

            
            ProcessBuilder pb = new ProcessBuilder("python", "prsn.py", textarea.getText());
            pb.redirectErrorStream(true);
            Process process = pb.start();

            
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), "UTF-8"));
            String line;
            StringBuilder output = new StringBuilder();
            while ((line = reader.readLine()) != null) {
                output.append(line);
            }

            outputLabel.setText(output.toString());
            System.out.println(output.toString());

        } catch (Exception e) {
            outputLabel.setText(e.getMessage());
            
        }
    }
    @FXML
    void effacer(ActionEvent event) {
        textarea.clear();
        outputLabel.setText("");
    }

}
