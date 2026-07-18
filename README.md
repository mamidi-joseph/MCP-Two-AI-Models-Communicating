# MCP: Two AI Models Communicating

A Python-based AI chatbot that demonstrates how two independent open-source Large Language Models (LLMs) can communicate using the Model Context Protocol (MCP).

The first AI model (Qwen) interacts directly with the user and can consult a second AI model (Llama) whenever it determines that a second opinion or additional reasoning may be useful. Both models run locally using Ollama without requiring any paid APIs or cloud services.

---

## Features

- Two independent AI models communicating through MCP.
- Runs completely on your local machine.
- No paid APIs or cloud services required.
- Uses Ollama to run both LLMs locally.
- Supports terminal-based interaction.
- Includes an optional Streamlit web interface.
- Demonstrates tool calling and multi-model collaboration.

---

## Technologies Used

- Python
- Ollama
- MCP (Model Context Protocol)
- Streamlit
- Qwen 2.5 (1.5B)
- Llama 3.2 (1B)

---

## Project Structure

```text
project-folder/
│
├── app.py
├── client.py
├── server.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## System Requirements

- Ubuntu (Recommended)
- Python 3.10 or above
- Ollama
- Internet connection (only required for downloading Ollama and the LLM models)
- Python Virtual Environment (Recommended)

---

## Clone the Repository

```bash
git clone https://github.com/mamidi-joseph/MCP-Two-AI-Models-Communicating.git
cd MCP-Two-AI-Models-Communicating
```

---

## Create a Virtual Environment

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

Verify that it is activated:

```bash
which python
```

---

## Install Python Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

(Optional) Upgrade pip:

```bash
pip install --upgrade pip
```

---

## Install Ollama

Run the following command:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Verify the installation:

```bash
ollama --version
```

---

## Download the Required LLM Models

This project uses two local LLM models.

### Download Qwen 2.5 (1.5B)

```bash
ollama pull qwen2.5:1.5b
```

### Download Llama 3.2 (1B)

```bash
ollama pull llama3.2:1b
```

---

## Verify the Installed Models

Run:

```bash
ollama list
```

You should see both models installed:

```text
qwen2.5:1.5b
llama3.2:1b
```

If both models are listed, you are ready to run the project.

---

## Running the Project

### Recommended Method - Ubuntu Terminal

The recommended way to use this project is through the Ubuntu terminal using `client.py`.

Run:

```bash
python client.py
```

You should see something similar to:

```text
============================================================
Two AI models are now connected.
You are talking to Model 1 (Qwen2.5).
It can privately consult Model 2 (Llama 3.2) when useful.
Type 'quit' to exit.
============================================================
```

You can now start asking questions directly from the terminal.

To exit the application:

```text
quit
```

or

```text
exit
```

> **Note:** `client.py` is the recommended way to use this project and best demonstrates how the two AI models communicate using MCP.

---

## Optional Web Interface

This project also includes a simple Streamlit-based web interface.

Run:

```bash
streamlit run app.py
```

After running the command, Streamlit will provide a local URL similar to:

```text
http://localhost:8501
```

Open the URL in your browser to interact with the chatbot.

> **Note:** `app.py` is completely optional. The terminal-based version (`client.py`) is recommended for demonstrating MCP-based communication between the two AI models.

---

## Example Prompts

The first AI model decides whether it needs to consult the second AI model. Because of this, some prompts may be answered directly without invoking MCP.

If you want to clearly demonstrate communication between both AI models, try prompts that explicitly request a second opinion or ask the first model to consult the second AI model.

Examples:

```text
Ask the second AI what it thinks, then tell me if you agree.

Get a second opinion on whether cats or dogs make better pets.

Check with the other AI whether my plan makes sense: [describe your plan]

Consult the second AI and explain how MCP works.

Ask the other AI for its opinion on learning Python.
```

> **Note:** The use of MCP depends on the first AI model's decision. Prompts that explicitly request a second opinion are more likely to demonstrate the interaction between the two AI models.

---

## How It Works

```text
            User
              |
              v
         client.py
              |
              v
      Qwen 2.5 (1.5B)
              |
              v
        MCP Tool Call
              |
              v
          server.py
              |
              v
      Llama 3.2 (1B)
              |
              v
      Response Returned
              |
              v
   Qwen Generates Final Answer
              |
              v
             User
```

---

## Workflow

1. The user asks a question.

2. Qwen receives the question.

3. If required, Qwen consults the second AI model through MCP.

4. The MCP server forwards the question to Llama.

5. Llama generates its response.

6. The response is returned to Qwen.

7. Qwen combines the information and generates the final answer.

8. The final response is displayed to the user.

---

## Important Notes

- This project was developed and tested on Ubuntu.
- Using a Python virtual environment is recommended.
- Both LLM models must be downloaded before running the project.
- `client.py` is the recommended way to use the project.
- `app.py` is optional and provides a simple Streamlit web interface.
- No paid APIs or cloud services are required.
- Internet access is only required when downloading Ollama and the LLM models.
- All AI models run locally on your machine using Ollama.
- The first AI model decides when it should consult the second AI model.
- Not every prompt will result in communication between both models.

---

## Troubleshooting

### Ollama Command Not Found

Verify that Ollama is installed:

```bash
ollama --version
```

If the command is not recognized, reinstall Ollama:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

---

### Model Not Found

Check the installed models:

```bash
ollama list
```

If a model is missing, download it again:

```bash
ollama pull qwen2.5:1.5b
```

or

```bash
ollama pull llama3.2:1b
```

---

### Python Packages Not Found

Ensure that your virtual environment is activated:

```bash
source venv/bin/activate
```

Then reinstall the dependencies:

```bash
pip install -r requirements.txt
```

---

## Author

**Mamidi Joseph**

- Email: mrjoseph569@gmail.com , mamidijoseph9@gmail.com
- GitHub: https://github.com/mamidi-joseph
- LinkedIn: https://www.linkedin.com/in/mamidi-joseph/

Feel free to connect with me or reach out if you have any questions, suggestions, or feedback regarding this project.

---

## License

This project is intended for educational and learning purposes.
