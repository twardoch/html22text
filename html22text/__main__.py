#!/usr/bin/env python3
import fire

from .html22text import html22text


def cli():
    fire.core.Display = lambda lines, out: print(*lines, file=out)
    fire.Fire(html22text)


if __name__ == "__main__":
    cli()
