
## **Search Engine Smart: Advanced Image-based Text Search System**

### **Overview**

"Search Engine Smart" is a state-of-the-art platform melding image processing with natural language processing. By harnessing the power of Optical Character Recognition (OCR) and sophisticated text embeddings, this application empowers users to search for images via their embedded textual content, ensuring remarkable precision and relevance.

### **Core Features**

1. **Image-to-Text Transformation with easyOCR**: Leveraging the `paddleOCR` library, the system meticulously scans images, converting visual text into coherent and accurate digital text.
2. **Embedding Generation with all-mpnet-base-v2**: The application taps into the `sentence-transformers` library to metamorphose extracted text into profound embeddings using the `all-mpnet-base-v2` model, thus fostering semantic-centric searches.
3. **Data Storage & Retrieval**: MongoDB stands as the infrastructure pillar, promising structured and efficient data storage.
4. **Real-time Data Synchronization**: The architecture ensures seamless data sync between MongoDB and Elasticsearch, fusing MongoDB's robustness with Elasticsearch's agile search prowess.
5. **Precision-Driven Search**: Through cosine similarity computations, the system evaluates the affinity between query embeddings and stored image embeddings, delivering unmatched search results.

### **About easyOCR**

`easyOCR` is a trailblazing Optical Character Recognition (OCR) library crafted for Python. It's particularly designed to decipher textual content from images, a task it executes with outstanding accuracy and efficiency. Here are its standout features:

- **Deep Learning Driven**: Rooted in neural networks, it's tailored explicitly for OCR tasks, ensuring high accuracy even in complex scenarios.
- **Multilingual**: Recognizes over 80 languages, making it one of the most versatile OCR tools.
- **Real-world Adaptability**: From tilted images and diverse fonts to low-light conditions, `paddleOCR` is adept at handling a wide array of challenges.
- **Open-Source & Community-Backed**: The continuous influx of contributions from the community guarantees its evolution, adaptability, and improvement.

### **About the all-mpnet-base-v2 Model**

The `all-mpnet-base-v2` model stands as a pillar in the `sentence-transformers` library realm. It translates sentences and paragraphs into a 768-dimensional dense vector space, proving invaluable for tasks like clustering or semantic search. Developed during Hugging Face's Community week using JAX/Flax for NLP & CV, it was honed on over 1 billion sentence pairs via a self-supervised contrastive learning objective.

**Intended Uses**: Designed as a sentence and short paragraph encoder, it outputs vectors encapsulating the semantic essence of input text, making it apt for information retrieval, clustering, or sentence similarity challenges.

**Training Data**: The model's finesse comes from its extensive training on multiple datasets, amalgamating to over 1 billion sentence pairs. This includes data from diverse sources like Reddit comments, S2ORC Citation pairs, and many more.

### **Setup and Configuration**

**Prerequisites**:
- Python 3.x
- MongoDB
- Elasticsearch
- OS Agnostic

**Dependency Installation**:
```bash
pip install -r requirements.txt
```

**Elasticsearch Configuration**:
- Tweak the `example.ini` in `search_engine/data/` as per your Elasticsearch setup.

### **Usage Guide**

**Starting the Application**:
```bash
streamlit run pipeline.py
```

**User Interface Guide**:
- **Image Upload**: Seamlessly index individual images for subsequent searches.
- **Bulk Upload via RAR**: Enable mass indexing by uploading images in a `.rar` format.
- **Semantic Search**: Input textual queries, fine-tune precision, and behold highly pertinent image results.

### **Technical Insights**

- **Image-to-Text Conversion**: `paddleOCR` delves deep into images, translating discerned patterns into digital text.
- **Textual Embedding**: The `all-mpnet-base-v2` model from the Sentence Transformers library crafts embeddings that encapsulate the textual essence.
- **Data Maneuvers**: MongoDB orchestrates data, storing each image and its metadata as distinctive documents.
- **Search Mechanism**: The underpinning search is empowered by cosine similarity computations. By juxtaposing vector angles, the system ascertains similarity scores, ranking images accordingly.

### **Contributors and Acknowledgements**

- [PhucNTT2, ThongND10, TrangVV2]
- Immense gratitude to the open-source realm, especially the visionaries behind `sentence-transformers`, `easyOCR`, and the stalwarts of the `all-mpnet-base-v2` model. Their tools serve as the cornerstone of this project.
