

![image](https://github.com/Shahad-Mohammed/AraGorilla/assets/74230739/84be9f67-0c14-425d-b42c-44c9424c3c59)

# AraGorilla: Arabic Large Language Model Connected with Massive APIs



https://github.com/Shahad-Mohammed/AraGorilla/assets/74230739/a55fa04b-8d79-4283-9e29-37f8f469f725


AraGorilla is an Arabic Large Language Model (LLM) specifically designed to understand Arabic requests and produce precise API responses. This README provides an overview of the project, its features, and how to get started.

## About the Project
AraGorilla addresses the limitations of existing Arabic LLMs in generating APIs for requests. It aims to create a dataset in the instruct-API format for fine-tuning, reduce hallucinations, and improve efficiency. The model comprehends Arabic queries and generates relevant API calls using a structured pipeline inspired by the self-instruct paradigm.

### Built With
- GPT-3.5 Turbo
- Retrieval-Augmented Generation (RAG)

## Getting Started
Follow these instructions to set up the project locally.

### Prerequisites
- Python 3.x
-NVIDIA GPU (optional but recommended for better performance)

### Installation
Clone the repository:

sh
Copy code
git clone https://github.com/AraGorilla/aragorilla.git
Install dependencies:

sh
Copy code
cd aragorilla
pip install -r requirements.txt


## Usage
* Train AraGorilla on your dataset.
* Fine-tune the LLaMA3-8B model using the provided Arabic instruction-API pairs.
* Evaluate API requests using AST sub-tree matching and cosine similarity.

## Roadmap
Enhance the model's performance by incorporating additional retrieval techniques.
Expand the dataset to cover a wider range of API domains.
Provide pre-trained models for easier integration into existing projects.
Contributing
Contributions are welcome! Please follow the contribution guidelines outlined in CONTRIBUTING.md.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For inquiries or support, please contact:

Shahad Mohammed Aboukozzana: shahadmoh232@gmail.com

Maryam Hussain Saif: maryam.h.saif@gmail.com

Batool Shaker Al-Goraibi: batool.ghoraibi@gmail.com

## Acknowledgements
We would like to acknowledge the support of [references to papers and contributors]. Special thanks to [additional acknowledgments].

