import cv2
from easyocr import Reader


class PlateRecognizer:
    def __init__(self, language='en', enable=False):
        self.reader = Reader([language], gpu=enable)

    def cleanup_text(self, text):
        return "".join([c if ord(c) < 128 else "" for c in text]).strip()

    def ocr(self, image, box):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        results_text = ""

        (x, y, w, h) = box
        roi = gray[y:y + h, x:x + w]

        results = self.reader.readtext(roi)
        for (bbox, text, prob) in results:
            cleaned_text = self.cleanup_text(text)
            print("[INFO] {:.4f}: {}".format(prob, cleaned_text))
            results_text += " " + cleaned_text

        return results_text
