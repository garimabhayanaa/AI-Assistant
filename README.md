# AI Assistant Project

## Overview
This project is an AI-powered assistant that can perform various tasks, answer questions, and interact with users through voice commands and a graphical user interface (GUI). It utilizes several libraries and APIs to provide functionalities such as speech recognition, text-to-speech, real-time information retrieval, and application control.

## Features
- **Voice Interaction**: Users can interact with the assistant using voice commands.
- **Task Automation**: The assistant can perform tasks such as opening applications, playing music, and generating content.
- **Real-time Information**: It can fetch real-time data from the internet, such as news and current events.
- **Image Generation**: The assistant can generate images based on user prompts using AI models.
- **Chat History**: Maintains a chat log for context and reference.
- **Graphical User Interface**: A user-friendly GUI built with PyQt5 for easy interaction.

## Technologies Used
- Python
- PyQt5
- Cohere API
- Groq API
- Hugging Face API for image generation
- Selenium for web automation
- Various other libraries for functionality (e.g., `pyautogui`, `pygame`, `requests`, etc.)

## Installation

### Prerequisites
- Python 3.7 or higher
- Pip (Python package installer)

### Steps
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Required Packages**:
   Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

   Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file in the root directory and add the necessary environment variables:
   ```plaintext
   COHERE_API_KEY=<your-cohere-api-key>
   GROQ_API_KEY=<your-groq-api-key>
   HUGGINGFACE_API_KEY=<your-huggingface-api-key>
   USERNAME=<your-username>
   ASSISTANT=<assistant-name>
   INPUT_LANGUAGE=<language-code>
   ASSISTANT_VOICE=<voice-name>
   ```

## Usage
1. **Run the Application**:
   Execute the main script to start the assistant:
   ```bash
   python main.py
   ```

2. **Interact with the Assistant**:
   - Use voice commands to ask questions or give tasks.
   - The assistant will respond verbally and display text in the GUI.

3. **Accessing Features**:
   - **Voice Commands**: Speak commands like "open Chrome", "play music", or "generate an image of a cat".
   - **Text Commands**: You can also type commands in the GUI.

## Contributing
Contributions are welcome! If you have suggestions or improvements, feel free to create a pull request or open an issue.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- Thanks to the developers of the libraries and APIs used in this project.
- Special thanks to the open-source community for their contributions.
