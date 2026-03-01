# Teach-Me Chatbot (Python CLI)

A simple chatbot that can be taught new responses and remembers them between sessions using a local JSON file.

## Features
- Teach the bot new Q&A pairs
- Persists learning to disk (memory.json)
- Commands to manage memory: /list, /forget, /clear, /quit
- Input normalisation to improve matching

## Tech Stack
Python, JSON (file persistence)

## Run Locally
python chatbot.py

## How It Works
- The bot loads saved Q&A from memory.json on startup
- When taught a new answer, it saves updates back to memory.json
