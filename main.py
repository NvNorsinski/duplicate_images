import sys
from pathlib import Path

import imagehash
from PIL import Image

file_suffix = {
    ".jpg",
    ".jpeg"
}


def find_images(directory) -> list[Path]:
    """iterates though direcorys and adds file paths to list."""
    pictures = []

    for img in directory.rglob("*"):
        if img.is_file() and img.suffix.lower() in file_suffix:
            pictures.append(img)

    return pictures


def calc_hash(file) -> imagehash.ImageHash | None:
    """Calculates perceptual Hash for each image."""
    try:
        with Image.open(file) as img:
            # pHash is resolution independent
            return imagehash.phash(img)

    except Exception as e:
        print(f"FEHLER: {file}")
        print(f"       {e}")
        return None


def find_dupicate(images, threshold=5) -> list[Path]:
    """
    Comparisons of pHashes of pictures

    haming distance is an indicator of difference of the pHashes
    
    0 = identical Hash
    small value = similiar pictures
    """

    hashes = []

    print()
    print("Berechne Bild-Hashes...")
    print()

    for nr, file in enumerate(images, start=1):
        print(f"[{nr}/{len(images)}] {file}")

        hash_value = calc_hash(file)

        if hash_value is not None:
            hashes.append((file, hash_value))

    print()
    print("Vergleiche Bilder...")
    print()

    groups = []
    already_used = set()

    for i in range(len(hashes)):
        file_1, hash1 = hashes[i]

        if i in already_used:
            continue

        group = [(file_1, 0)]

        for j in range(i + 1, len(hashes)):
            file_2, hash2 = hashes[j]

            if j in already_used:
                continue

            distance = hash1 - hash2

            if distance <= threshold:
                group.append((file_2, distance))
                already_used.add(j)

        if len(group) > 1:
            groups.append(group)

    return groups


def main():
    # give directory as argument
    if len(sys.argv) < 2:
        print("Verwendung:")
        print()
        sys.exit(1)

    directory = Path(sys.argv[1])

    if not directory.exists():
        print(f"Ordner existiert nicht: {directory}")
        sys.exit(1)

    if not directory.is_dir():
        print(f"Das ist kein Ordner: {directory}")
        sys.exit(1)

    print("=" * 60)
    print("BILDER-DUPLIKAT-FINDER")
    print("=" * 60)
    print()
    print(f"Ordner: {directory}")
    print()

    images = find_images(directory)

    print(f"{len(images)} Bilder gefunden.")

    if not images:
        print("Keine Bilder gefunden.")
        return

    groups = find_dupicate(images)

    print()
    print("=" * 60)
    print("ERGEBNIS")
    print("=" * 60)
    print()

    if not groups:
        print("Keine möglichen Duplikate gefunden.")
        return

    print(f"{len(groups)} Duplikatgruppen gefunden.")
    print()

    for nr, group in enumerate(groups, start=1):
        print(f"--- Gruppe {nr} ---")


        for file, distance in group:
            try:
                with Image.open(file) as image:
                    width, height = image.size

                groesse_mb = file.stat().st_size / (1024 * 1024)

                print(
                    f"{file}"
                    f" | {width}x{height}"
                    f" | {groesse_mb:.2f} MB"
                    f" | Distance: {distance}"
                )

            except Exception:
                print(
                    f"{file}"
                    f" | Distance: {distance}"
                )

        print()


if __name__ == "__main__":
    main()