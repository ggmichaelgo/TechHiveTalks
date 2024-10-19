# Running LLM from my basement servers

[Slides](https://docs.google.com/presentation/d/16ua_Qrf6wINBp1K6E3TIHrxFRsYxoPXTII1xOFL4-l8/edit#slide=id.g30af8efd1ea_0_147)

## Setting up Ollama Docker container

Docker image: https://hub.docker.com/r/ollama/ollama

CPU only mode
```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```
