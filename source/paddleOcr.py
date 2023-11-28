from typing import List
from paddleocr import PaddleOCR

class ImageToText:
    @staticmethod
    def ocr_image_to_text(image_path: str) -> str:
        """
        Initialize the ImageToText with specific PaddleOCR configurations.

        Args:
        - rec_batch_num (int): Batch size for inference. Default is 16.
        - use_angle_cls (bool): Whether to use angle classifier to detect image orientation. Default is True.
        - lang (str): Language mode used in recognition. Default is 'en'.
        - det_lang (str): Language mode used in detection. Default is 'ml'.
        - det_algorithm (str): Detection algorithm to be used. Default is 'DB'.
        """
        ocr = PaddleOCR(use_angle_cls=True,
                        lang='en',
                        det_lang='ml',
                        det_algorithm="DB")
        try:
            results = ocr.ocr(image_path, cls=True)

            # Extracting text
            sentences = [item[1][0].strip() for sublist in results for item in sublist if item[1][0].strip() != ""]

            extracted_text = " ".join(sentences)

        except Exception as e:
            print(traceback.format_exc())

        return extracted_text
