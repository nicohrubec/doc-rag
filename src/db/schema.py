from docarray import BaseDoc
from docarray.typing import NdArray


class Doc(BaseDoc):
    text: str = ''
    embedding: NdArray[384]
