import cv2
from vizlpr.camera.threaded_frame_capture import ThreadedFrameCapture
from vizlpr.detector.plate_detector import PlateDetector
from vizlpr.recognizer.plate_recognizer import PlateRecognizer


class Camera:
    def __init__(self, src, output_file, display=True):
        self.src = src
        self.output_file = output_file
        self.cap = cv2.VideoCapture(src, cv2.CAP_FFMPEG)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.frame = ThreadedFrameCapture(self.cap)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.display = display
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter(output_file, self.fourcc, 30, (self.width, self.height), isColor=True)
        self.plate_detector = PlateDetector("../weights/license_plate.pt")
        self.plate_recognizer = PlateRecognizer()

    def start_capture(self):
        try:
            while True:
                _, img = self.frame.read()

                if img is not None:
                    boxes = self.plate_detector.detect(img)
                    for box in boxes:
                        x, y, w, h = box
                        cv2.rectangle(img, (x, y), (w, h), (0, 255, 255), 2)
                        ocr_result = self.plate_recognizer.ocr(img, box)
                        cv2.putText(img, ocr_result, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2,
                                    cv2.LINE_AA)

                    self.out.write(img)
                    if self.display:
                        cv2.imshow('VizALPR', img)

                key = cv2.waitKey(1)
                if key == 27:
                    break

        except KeyboardInterrupt:
            pass
        finally:
            self.stop_capture()

    def stop_capture(self):
        self.frame.release()
        self.out.release()
        self.cap.release()
        if self.display:
            cv2.destroyAllWindows()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop_capture()
