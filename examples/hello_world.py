"""Minimialistic pysketcher example."""
import pysketcher as ps
from pysketcher.backend.matplotlib import MatplotlibBackend


def main(backend=MatplotlibBackend) -> ps.Figure:
    code = ps.Text("print 'Hello, World!'", ps.Point(2.5, 1.5))

    code.style.fontsize = 24
    code.style.font_family = ps.TextStyle.FontFamily.MONO
    code.style.fill_color = ps.TextStyle.Color.GREY

    fig = ps.Figure(0.0, 5.0, 0.0, 3.0, backend=backend)
    fig.add(code)
    return fig


if __name__ == "__main__":
    fig = main()
    fig.show()
