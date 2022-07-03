import io
import base64
import typing
import pathlib
import warnings
import tempfile


try:
    import cv2
    import numpy

except ImportError:
    cv2 = None


class Thumbnail:
    def __init__(self,
                 image: typing.Union[pathlib.Path, bytes],
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
        return base64.b64encode(self.image).decode('utf-8')


class MakeThumbnail(Thumbnail):
    warn_cv2 = None

    def __init__(self,
                 image: typing.Any,
                 width: int = 200,
                 height: int = 200,
                 seconds: int = 1, *args, **kwargs) -> None:
        if cv2 is not None:
            self.width = width
            self.height = height
            self.seconds = seconds
            if not isinstance(image, numpy.ndarray):
                image = numpy.frombuffer(image, dtype=numpy.uint8)
                image = cv2.imdecode(image, flags=1)

            self.image = self.ndarray_to_bytes(image)
        else:
            self.warning()

    def ndarray_to_bytes(self, image: numpy.ndarray, *args, **kwargs) -> str:
        self.width = image.shape[1]
        self.height = image.shape[0]

        status, buffer = cv2.imencode('.png', image)
        if status is True:
            return io.BytesIO(buffer).read()

    @classmethod
    def from_video(cls, video: bytes, *args, **kwargs) -> numpy.ndarray:
        if cv2 is None:
            return cls.warning()
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

    @classmethod
    def warning(cls):
        if not cls.__class__.warn_cv2:
            cls.__class__.warn_cv2 = True
            warnings.warn(
                'the library needs "cv2" library to '
                'make auto thumbnails for "videos" and "gifs" and etc.')
