GGUF is the modern, recommended file format used by the llama.cpp project for running large language models (LLMs) efficiently on a variety of hardware, including CPUs and low-resource environments.
What is GGUF?
The GGUF (GGML Universal File) format is a binary file format designed to store both model tensors and metadata in a single file.
Origin: It was introduced by the llama.cpp project in August 2023 to succeed the previous GGML format, primarily to ensure better backward compatibility and support for new model architectures.
Efficiency: GGUF files are optimized for fast loading and saving of model data and are well-suited for inference, especially on CPU hardware.
Portability: The format is widely adopted and supported by many different clients and libraries, such as text-generation-webui, KoboldCpp, LM Studio, and various Python bindings like llama-cpp-python.
llama.cpp and GGUF
llama.cpp is the reference implementation and the primary project that popularized the use of GGUF. It provides the necessary tools and runtime environment to interact with these files.
Key functions include:
Inference: The core llama.cpp executable (./main) can load GGUF files and run the model for inference directly from the command line.
Quantization: The project includes scripts (e.g., convert_hf_to_gguf.py) to convert models from other popular formats (like Hugging Face PyTorch models) into the optimized GGUF format, often applying quantization (reducing the precision of the model weights to save memory).
Hardware Support: llama.cpp and GGUF models support GPU acceleration across various platforms, including Apple Silicon (Metal), NVIDIA (CUDA), and Intel GPUs (SYCL).
How to use GGUF with llama.cpp
Obtain llama.cpp: You need to build or download the llama.cpp project from its GitHub repository.
Find a GGUF model: Model repositories like Hugging Face have numerous GGUF files, often provided by community members such as "TheBloke".
Run the model: You can run the model using the command line interface provided by llama.cpp, for example: ./main -m <model_file.gguf> -p "Your prompt here:".
For a more user-friendly experience, many GUI applications and Python libraries use llama.cpp under the hood to load GGUF files, such as LM Studio or llama-cpp-python.
