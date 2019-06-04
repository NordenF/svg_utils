import argparse
import os

from jinja2 import Template
from wand.image import Image


def _get_bytes(string: str) -> bytes:
    return string.encode("utf-8")


def convert(svg_text: str, result_format: str) -> bytes:
    """
    Converts SVG to specified image format and return binary data, ready for save to file.
    :param svg_text: SVG as simple text.
    :param result_format: Format of resulting image (for example, "png").
    """
    svg_blob = _get_bytes(svg_text)
    with Image(blob=svg_blob) as wand_image_img:
        return wand_image_img.make_blob(format=result_format)


def convert_and_save_to_file(svg_text: str, filename: str) -> None:
    """
    Saves SVG as image file (with conversion to need format, definec by filename extension).
    :param svg_text: SVG as simple text.
    :param filename: Name of resulting file (for example, "sample.png").
    """
    svg_blob = _get_bytes(svg_text)
    with Image(blob=svg_blob) as wand_image:
        wand_image.save(filename=filename)


class _StoreDictKeyPair(argparse.Action):
    """See https://stackoverflow.com/a/42355279"""
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super().__init__(option_strings, dest, nargs=nargs, **kwargs)
        self._nargs = nargs

    def __call__(self, parser, namespace, values, option_string=None):
        key_values = {}
        for kv in values:
            if kv.count(":") != 1:
                parser.error("wrong format of replacement pair.")
                return
            k, v = kv.split(":")
            key_values[k] = v
        setattr(namespace, self.dest, key_values)


def parse_args() -> argparse.Namespace:
    argparser = argparse.ArgumentParser(
        description="The script processes SVG-file by Jinja2 template engine, "
                    "replaces variables (such as {{ some_test_variable }})  with specified values "
                    "and converts the resulting SVG to needed image format.")
    argparser.add_argument("-i", "--in", required=True, help="Input SVG-file.", metavar="path/to/file.svg")
    argparser.add_argument("--replacements", action=_StoreDictKeyPair, nargs="+", metavar='var_name:"Text content"')
    out = argparser.add_mutually_exclusive_group(required=True)
    # One of two arguments is required, but not both.
    out.add_argument("--stdout", action="store_true", help="Print the result to STDOUT (in svg format).")
    out.add_argument("-o", "--out", help="Output file (file.svg, file.png, file.jpg, etc...)",
                     metavar="path/to/file.{ext}")
    args = argparser.parse_args()

    # Custom check for case when empty string was explicitely passed, for example:  --out ""
    # It seems that argparse does not check it. :-(
    if getattr(args, "in") == "":
        argparser.error("argument -i/--in: expected not empty file path.")
    if args.out == "":
        argparser.error("argument -o/--out: expected not empty file path.")

    return args


def main() -> None:
    args = parse_args()

    svg_file = getattr(args, "in")  # "args.in" not works, because "in" is keyword in Python.
    with open(svg_file, "r") as f:
        svg_text = f.read()

    if args.replacements:
        template = Template(svg_text)
        svg_text = template.render(**args.replacements)

    if args.stdout:
        print(svg_text)
        return

    output_file = args.out
    containing_directory, file_name_ext = os.path.split(output_file)
    if containing_directory and not os.path.exists(containing_directory):
        os.makedirs(containing_directory)
    extension = os.path.splitext(file_name_ext)[1]
    if extension.lower() == ".svg":
        with open(output_file, "w") as f:
            f.write(svg_text)
        return

    # Saving to other format...
    convert_and_save_to_file(svg_text, output_file)


if __name__ == "__main__":
    main()
