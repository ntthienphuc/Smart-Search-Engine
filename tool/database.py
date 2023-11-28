from source.paddleOcr import ImageToText
from .postgress import PostgreSQLManager

from PIL import Image
from transformers import AutoTokenizer, AutoModel
import numpy as np
import os
import torch


class DatabaseManager:
    """
    A class to manage interactions with the PostgreSQL database and process image data.
    """

    def __init__(self):
        """
        Initializes the DatabaseManager with a connection to PostgreSQL
        and pre-trained models for tokenization and embeddings.
        """
        self.db = PostgreSQLManager(
            dbname="trangvv",
            user="postgres",
            password="123456",
            host="localhost",
            port="5432"
        )
        self.tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-mpnet-base-v2')
        self.model = AutoModel.from_pretrained('sentence-transformers/all-mpnet-base-v2')

    def return_path(self) -> str:
        """
        Returns the current working directory path.

        Returns:
            str: The current working directory path with backslashes replaced by forward slashes.
        """
        path = str(os.getcwd())
        path = path.replace("\\", "/")
        return path

    def text(self,
             image: np.ndarray) -> str:
        """
        Extracts text from the given image using PaddleOCR.

        Args:
            image (np.ndarray): The image to extract text from.

        Returns:
            str: Extracted text from the image. Returns '=' if extraction fails.
        """
        try:
            labels = ImageToText().ocr_image_to_text(image)
            return labels
        except:
            labels = '='
            return labels

    from transformers import AutoTokenizer, AutoModel
    tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-mpnet-base-v2')
    model = AutoModel.from_pretrained('sentence-transformers/all-mpnet-base-v2')
    import torch
    import numpy as np

    def get_dense_vector(text):
        data = text.split(' ')
        if len(data) > 1:
            inputs = tokenizer(text, padding=True, truncation=True, return_tensors="pt")
            with torch.no_grad():
                outputs = model(**inputs)
                embeddings = outputs.last_hidden_state
            dense_vector = torch.mean(embeddings, dim=1)
            dense_vector = dense_vector.tolist()
            dense_vector = dense_vector[0]
            return dense_vector
        else:
            if len(data[0]) > 1:
                inputs = tokenizer(text, padding=True, truncation=True, return_tensors="pt")
                with torch.no_grad():
                    outputs = model(**inputs)
                    embeddings = outputs.last_hidden_state
                dense_vector = torch.mean(embeddings, dim=1)
                dense_vector = dense_vector.tolist()
                dense_vector = dense_vector[0]
                return dense_vector
            else:
                num_dimensions = 768
                default_value = 1e-10
                dense_vector = np.full(num_dimensions, default_value)
                dense_vector = dense_vector.tolist()
                return dense_vector

    def up_data(self,
                list_image: list):
        """
        Processes and stores the images in the list to the database.

        Args:
            list_image (list): A list of images to process and store.

        Returns:
            None
        """
        pathr = self.return_path()
        paths = f"{pathr}/search_engine_v1.1/data/image/"
        list_ima = os.listdir(paths)

        for i in list_image:
            if i[0] not in list_ima:
                path_images = paths + i[0]
                save_path = "/search_engine_v1.1/data/image/" + str(i[0])

                im1 = Image.open(i[1])
                image_array = np.array(im1)
                im1.convert('RGB').save(path_images)

                labels = self.text(image_array)
                vectors = self.vector(labels)

                data = (save_path, [labels], vectors)
                self.db.insert_data('data', data)


