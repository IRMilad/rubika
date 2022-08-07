import io
import base64
import tempfile


try:
    import cv2
    import numpy

except ImportError:
    cv2 = None
    numpy = None


class Thumbnail:
    def __init__(self,
                 image: bytes,
                 width: int = 200,
                 height: int = 200,
                 seconds: int = 1, *args, **kwargs) -> None:

        self.image = image
        self.width = width
        self.height = height
        self.seconds = seconds

        if isinstance(self.image, str):
            with open(image, 'rb') as file:
                self.image = file.read()

    def to_base64(self, *args, **kwargs) -> str:
        if self.image is not None:
            return base64.b64encode(self.image).decode('utf-8')


class MakeThumbnail(Thumbnail):
    def __init__(self,
                 image,
                 width: int = 200,
                 height: int = 200,
                 seconds: int = 1, *args, **kwargs) -> None:
        self.image = None
        self.width = width
        self.height = height
        self.seconds = seconds
        if hasattr(None, 'imdecode'):
            if not isinstance(image, numpy.ndarray):
                image = numpy.frombuffer(image, dtype=numpy.uint8)
                image = cv2.imdecode(image, flags=1)

            self.image = self.ndarray_to_bytes(image)

    def ndarray_to_bytes(self, image, *args, **kwargs) -> str:
        if hasattr(None, 'resize'):
            self.width = image.shape[1]
            self.height = image.shape[0]
            image = cv2.resize(image,
                               (round(self.width / 10), round(self.height / 10)),
                               interpolation=cv2.INTER_CUBIC)

            status, buffer = cv2.imencode('.png', image)
            if status is True:
                return io.BytesIO(buffer).read()

    @classmethod
    def from_video(cls, video: bytes, *args, **kwargs):
        if hasattr(None, 'VideoCapture'):
            with tempfile.TemporaryFile(mode='wb+') as file:
                file.write(video)
                capture = cv2.VideoCapture(file.name)
                status, image = capture.read()
                if status is True:
                    fps = capture.get(cv2.CAP_PROP_FPS)
                    frames = capture.get(cv2.CAP_PROP_FRAME_COUNT)
                    return MakeThumbnail(
                        image=image,
                        seconds=int(frames / fps), *args, **kwargs)
