#!/usr/bin/env python3
"""Merge several CVAT "CVAT for images 1.1" exports (e.g. an OMS task and a DMS task) into one.

  python scripts/merge_exports.py oms.zip dms.zip --exclude S09,S10 --out export_final.zip
  python scripts/merge_exports.py oms.zip --only S09,S10 --out export_extra.zip

Each input may be the .zip CVAT exports or annotations.xml itself. The output is a zip holding
only annotations.xml (no images). Meta (labels) is taken from the first file; <image> elements
from all files are appended and renumbered. Duplicate image names stop the merge.
Standard library only.
"""
import argparse
import os
import sys
import xml.etree.ElementTree as ET
import zipfile


def load(path):
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as z:
            names = [n for n in z.namelist() if n.endswith(".xml")]
            if not names:
                sys.exit(f"{path}: zip không có file .xml")
            return ET.fromstring(z.read(names[0]))
    return ET.parse(path).getroot()


def main():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+", help="các file export (.zip hoặc .xml)")
    ap.add_argument("--out", required=True, help="file zip đầu ra, ví dụ export_final.zip")
    ap.add_argument("--only", help="chỉ giữ ảnh có mã này, ví dụ S09,S10 (S09 gồm S09_rgb và S09_ir)")
    ap.add_argument("--exclude", help="bỏ ảnh có mã này, ví dụ S09,S10")
    args = ap.parse_args()
    only = [t.strip().upper() for t in args.only.split(",")] if args.only else None
    excl = [t.strip().upper() for t in args.exclude.split(",")] if args.exclude else []

    def keep(name):
        stem = os.path.splitext(name)[0].upper()
        codes = (stem.split("_")[0], stem)
        if only is not None and not any(c in only for c in codes):
            return False
        return not any(c in excl for c in codes)

    roots = [load(p) for p in args.inputs]
    seen, images = {}, []
    for path, root in zip(args.inputs, roots):
        for img in root.findall("image"):
            name = os.path.basename(img.get("name", ""))
            if not keep(name):
                continue
            if name in seen:
                sys.exit(f"Ảnh '{name}' có trong cả {seen[name]} và {path}. Không gộp.")
            seen[name] = path
            images.append(img)

    base = roots[0]
    for img in base.findall("image"):
        base.remove(img)

    images.sort(key=lambda el: os.path.basename(el.get("name", "")))
    for i, img in enumerate(images):
        img.set("id", str(i))
        base.append(img)

    for size in base.iter("size"):  # meta/task/size or meta/job/size
        size.text = str(len(images))

    ET.indent(base) if hasattr(ET, "indent") else None
    data = ET.tostring(base, encoding="utf-8", xml_declaration=True)
    with zipfile.ZipFile(args.out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("annotations.xml", data)

    for path, root in zip(args.inputs, roots):
        print(f"  {path}: {sum(1 for v in seen.values() if v == path)} ảnh")
    print(f"Đã gộp {len(images)} ảnh -> {args.out}")


if __name__ == "__main__":
    main()
