## Introduction

This project is a learning exercise aimed at understanding and implementing langchain and GPT (Generative Pre-trained Transformer) models.

## Purpose

The purpose of this project is to explore the capabilities of langchain and GPT models and gain hands-on experience with their implementation. By building this project, the aim to deepen my understanding of natural language processing and generation.

## Features

- Langchain implementation: This project includes an implementation of langchain, a language modeling technique that leverages GPT models.
- GPT integration: I've integrated a GPT model into the langchain implementation to generate coherent and context-aware text.

## Getting Started

To get started with this project, follow these steps:

1. Clone the repository: `git clone https://github.com/your-username/LangchainPy.git`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Run the project: `python main.py`

## Resources

- [Langchain documentation](https://langchain-docs.com)
- [GPT model documentation](https://gpt-model-docs.com)
- [Tutorial: Introduction to langchain](https://langchain-tutorial.com)
- [Tutorial: Building a GPT model](https://gpt-tutorial.com)

## License

This project is licensed under the [MIT License](LICENSE).

## Notes

- When memory is added to the AgentExecutor, it doesn't behave as one might expect.
- Messages from intermediate_steps are wiped out as soon as the while loop stops.
- It doesn't get persisted to memory. The only thing that gets transferred to memory is the **final Ai message received that stops the while loop (Usually seen as the result received from GPT) & the initial Human Message**.
