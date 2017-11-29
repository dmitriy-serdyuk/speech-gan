#!/usr/bin/env python
import argparse


def main(path):
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Prepare VCTK data')
    parser.add_argument('path')
    args = parser.parse_args()
    main(**args.__dict__)
