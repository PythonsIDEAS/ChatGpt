/* global puter */
import React, { useState, useEffect, useRef } from "react";
import { SplitText } from "./SplitText";
import "./App.css";

export default function App() {
  const [messages, setMessages] = useState([
    { text: "Hello! How can I assist you? 😊", sender: "bot" },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(false);
  const chatBoxRef = useRef(null);

  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { text: input, sender: "user" };
    setMessages([...messages, userMessage]);
    setIsLoading(true);

    try {
      const response = await puter.ai.chat(input, {
        model: "gpt-4.1-nano",
        stream: true
      });

      let fullResponse = "";
      for await (const part of response) {
        fullResponse += part?.text || "";
        setMessages(prevMessages => {
          const withoutLastBot = prevMessages.filter((msg, idx) => 
            !(msg.sender === "bot" && idx === prevMessages.length - 1)
          );
          return [...withoutLastBot, { text: fullResponse, sender: "bot" }];
        });
      }
    } catch (error) {
      console.error("Error:", error);
      const errorMessage = { text: "Sorry, I encountered an error. Please try again.", sender: "bot" };
      setMessages(prevMessages => [...prevMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }

    setInput("");
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  };

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
  };

  return (
    <div className={`chat-container ${isDarkMode ? "dark-mode" : ""}`}>
      <button className="dark-mode-toggle" onClick={toggleDarkMode}>
        {isDarkMode ? "☀️" : "🌙"}
      </button>
      <div className="chat-box" ref={chatBoxRef}>
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            {msg.sender === "bot" ? (
              <SplitText text={msg.text} delay={50} /> // Use SplitText for bot messages
            ) : (
              msg.text // Display user messages normally
            )}
          </div>
        ))}
        {isLoading && <div className="message bot">Typing...</div>}
      </div>

      <div className="input-box">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type a message..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}