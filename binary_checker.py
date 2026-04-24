#!/usr/bin/env python3
import sys

def is_binary(path, chunk_size=1024):
    try:
        with open(path, 'rb') as f:
            chunk = f.read(chunk_size)
            if not chunk:
                return False  # empty file → treat as text

            # If there are null bytes, it's very likely binary
            if b'\x00' in chunk:
                return True

            # Define what we consider "text" bytes
            text_bytes = bytearray(range(32, 127)) + b'\n\r\t\f\b'

            # Count non-text bytes
            nontext = sum(byte not in text_bytes for byte in chunk)

            # If more than 30% are non-text, treat as binary
            return (nontext / len(chunk)) > 0.3

    except Exception:
        # On error (e.g., file not readable), treat as binary
        return True


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file>", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]

    if is_binary(path):
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
