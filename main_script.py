import os
import transform
import pathlib

if __name__ == "__main__":
    source = "test.js"

    language = source.split('.', 1)[1]
    tr = transform.Transformer(language)
    tr.transform_code(source)


