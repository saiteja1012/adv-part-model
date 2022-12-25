import os
from PIL import Image
import numpy as np
import pathlib
import random
import shutil


CLASSES = {
    "Quadruped": 4,
    "Biped": 5,
    "Fish": 4,
    "Bird": 5,
    "Snake": 2,
    "Reptile": 4,
    "Car": 3,
    "Bicycle": 4,
    "Boat": 2,
    "Aeroplane": 5,
    "Bottle": 2,
}

metaclass_to_class = {
    "Aeroplane": set(),
    "Quadruped": set(),
    "Biped": set(),
    "Fish": set(),
    "Bird": set(),
    "Snake": set(),
    "Reptile": set(),
    "Car": set(),
    "Bicycle": set(),
    "Boat": set(),
    "Bottle": set(),
}

for path, subdirs, files in os.walk(
    "/data/kornrapatp/PartImageNet/PartSegmentations/All-imagenetclass-segtrain"
):
    for name in files:
        if ".tif" in name:
            metaclass = path.split("/")[-1]
            imagenet_class = name.split("_")[0]
            metaclass_to_class[metaclass].add(imagenet_class)


numpart = 1
imagenet_classes_part_num = {}
for k, v in metaclass_to_class.items():
    numpart += CLASSES[k] * len(v)
    for imagenet_class in v:
        imagenet_classes_part_num[imagenet_class] = CLASSES[k]
imagenet_classes_part_num = dict(sorted(imagenet_classes_part_num.items()))
print(f"Total part in new dataset: {numpart}")


# make directories
os.mkdir(
    "/data/kornrapatp/PartImageNet/PartSegmentations/All-imagenetclass-segtrain-processed"
)
for partition in ["train", "val", "test"]:
    os.mkdir(
        "/data/kornrapatp/PartImageNet/PartSegmentations/All-imagenetclass-segtrain-processed"
        + "/"
        + partition
    )
    for c in imagenet_classes_part_num.keys():
        os.mkdir(
            "/data/kornrapatp/PartImageNet/PartSegmentations/All-imagenetclass-segtrain-processed"
            + "/"
            + partition
            + "/"
            + c
        )
        with open(
            "/data/kornrapatp/PartImageNet/PartSegmentations/All-imagenetclass-segtrain-processed"
            + "/"
            + partition
            + "/"
            + c
            + ".txt",
            "w",
        ) as f:
            f.write("")

classes = sorted(CLASSES.keys())
print(classes)
class_starting_index = {}
curid = 1

for c in classes:
    class_starting_index[c] = curid
    curid += CLASSES[c]

print(class_starting_index)


imagenet_class_starting_index = {}
imagenet_indices = {}
curid = 1

for c in imagenet_classes_part_num.keys():
    imagenet_class_starting_index[c] = curid
    imagenet_indices[c] = [
        i for i in range(curid, curid + imagenet_classes_part_num[c])
    ]
    curid += imagenet_classes_part_num[c]


def save_pil_image(img, path):
    image_path = os.path.join(path)
    pil_img = Image.fromarray(img)
    pil_img.save(image_path)


fileList = {}
# Rewrite segmentation labels
for path, subdirs, files in os.walk(
    "/data/kornrapatp/PartImageNet/PartSegmentations/All-imagenetclass-segtrain"
):
    for name in files:
        className = path.split("/")[-1]
        if ".tif" in name:
            img = np.asarray(Image.open(os.path.join(path, name)))
            imagenet_className = name.split("_")[0]
            np_min = np.amin(
                np.where(
                    img != 0,
                    img,
                    999,
                ).astype(np.int32)
            )
            if np_min != class_starting_index[className]:
                print(np_min, class_starting_index[className])
            new_img = np.where(
                img != 0,
                img
                - (
                    class_starting_index[className]
                    - imagenet_class_starting_index[imagenet_className]
                ),
                np.zeros(img.shape),
            ).astype(np.int32)
            # print(img.dtype, new_img.dtype, np.amax(new_img), className)
            save_pil_image(
                new_img,
                os.path.join(
                    "/data/kornrapatp/PartImageNet/PartSegmentations/All-imagenetclass-segtrain-processed",
                    path.split("/")[-2],
                    imagenet_className,
                    name,
                ),
            )
            if path.split("/")[-2] + "/" + imagenet_className not in fileList:
                fileList[path.split("/")[-2] + "/" + imagenet_className] = []
            fileList[path.split("/")[-2] + "/" + imagenet_className].append(
                imagenet_className + "/" + name.split(".")[0] + "\n"
            )

for k, v in fileList.items():
    v = sorted(v)
    with open(
        "/data/kornrapatp/PartImageNet/PartSegmentations/All-imagenetclass-segtrain-processed"
        + "/"
        + k
        + ".txt",
        "w",
    ) as f:
        for name in v:
            f.write(name)
