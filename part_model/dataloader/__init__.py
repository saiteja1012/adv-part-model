# from .part_imagenet import PART_IMAGENET_BBOX

# DATASET_DICT = {
#     'part-imagenet-bbox': PART_IMAGENET_BBOX
# }


from .part_imagenet_corrupt import PART_IMAGENET_CORRUPT
from .part_imagenet_mixed_next import PART_IMAGENET_MIXED
from .cityscapes import CITYSCAPES
from .part_imagenet import PART_IMAGENET, PART_IMAGENET_BBOX
from .part_imagenet_geirhos import PART_IMAGENET_GEIRHOS
from .pascal_part import PASCAL_PART
from .pascal_voc import PASCAL_VOC
from .util import COLORMAP

DATASET_DICT = {
    'cityscapes': CITYSCAPES,
    'pascal-part': PASCAL_PART,
    'pascal-voc': PASCAL_VOC,
    'part-imagenet': PART_IMAGENET,
    'part-imagenet-geirhos': PART_IMAGENET_GEIRHOS,
    'part-imagenet-mixed': PART_IMAGENET_MIXED,
    'part-imagenet-corrupt': PART_IMAGENET_CORRUPT,
    'part-imagenet-bbox': PART_IMAGENET_BBOX
}


def load_dataset(args):
    loader = DATASET_DICT[args.dataset]['loader']
    return loader(args)
