import argparse
import logging

from typing import Type

import pysketcher as ps
from pysketcher.backend.matplotlib import MatplotlibBackend
from pysketcher.backend.svg import SvgBackend


def main(
    backend: Type[ps.backend.Backend] = MatplotlibBackend,
    show: bool = False,
    filename: str = None
) -> None:

    i = 1
    shapes_dict = {}
    for fill_pattern in ps.Style.FillPattern:
        logging.info("Fill Pattern: %s", fill_pattern)
        name: str = "Rectangle.%d" % i
        rectangle = ps.Rectangle(ps.Point(i, 1), 1, 1).set_fill_pattern(fill_pattern)
        shapes_dict[name] = rectangle
        i = i + 1.5

    shapes = ps.Composition(shapes_dict)

    fig = ps.Figure(0.0, 20.0, 0.0, 3.0, backend=backend)
    fig.add(shapes)

    if show:
        fig.show()
    if filename:
        fig.save(filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='PySketcher Hatching Example.')
    parser.add_argument('--backend', choices=['svg', 'matplotlib'],
                        default='matplotlib')
    parser.add_argument('--show', const=True, default=False, action='store_const')
    parser.add_argument('--filename', default=None)

    backend_map = {
        'matplotlib': MatplotlibBackend,
        'svg': SvgBackend
    }

    args = parser.parse_args()

    main(backend=backend_map[args.backend], show=args.show, filename=args.filename)
