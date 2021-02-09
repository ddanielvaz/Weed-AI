from weedcoco.stats import WeedCOCOStats


SMALL_WEEDCOCO = {
    "images": [
        {
            "id": 46,
            "file_name": "cwfid_images/046_image.png",
            "license": 0,
            "agcontext_id": 0,
            "width": 1296,
            "height": 966,
        },
        {
            "id": 1,
            "file_name": "cwfid_images/001_image.png",
            "license": 0,
            "agcontext_id": 0,
            "width": 1296,
            "height": 966,
        },
        {
            "id": 2,
            "file_name": "cwfid_images/001_image.png",
            "license": 0,
            "agcontext_id": 1,
            "width": 1296,
            "height": 966,
        },
    ],
    "annotations": [
        {
            "id": 0,
            "image_id": 46,
            "category_id": 0,
            "segmentation": [[596, 207, 521]],
            "iscrowd": 0,
        },
        {
            "id": 1,
            "image_id": 46,
            "category_id": 0,
            "segmentation": [[689, 787, 589, 745]],
            "iscrowd": 0,
        },
        {
            "id": 2,
            "image_id": 46,
            "category_id": 1,
            "segmentation": [[486, 335, 399]],
            "iscrowd": 0,
        },
        {
            "id": 3,
            "image_id": 1,
            "category_id": 1,
            "segmentation": [[810, 225, 841, 234]],
            "iscrowd": 0,
        },
        {
            "id": 4,
            "image_id": 1,
            "category_id": 1,
            "segmentation": [[1070, 626, 1055, 722]],
            "iscrowd": 0,
        },
        {
            "id": 5,
            "image_id": 2,
            "category_id": 1,
            "segmentation": [[810, 225, 841, 234]],
            "iscrowd": 0,
        },
    ],
    "categories": [
        {
            "name": "crop: daugus carota",
            "common_name": "carrot",
            "species": "daugus carota",
            "eppo_taxon_code": "DAUCS",
            "eppo_nontaxon_code": "3UMRC",
            "role": "crop",
            "id": 0,
        },
        {
            "name": "weed: unspecified",
            "species": "UNSPECIFIED",
            "role": "weed",
            "id": 1,
        },
    ],
    "info": {
        "version": 1,
        "description": "Cwfid annotations converted into WeedCOCO",
        "id": 0,
    },
    "license": [
        {
            "id": 0,
            "license_name": "CC BY 4.0",
            "license_fullname": "Creative Commons Attribution 4.0",
            "license_version": "4.0",
            "url": "https://creativecommons.org/licenses/by/4.0/",
        }
    ],
    "agcontexts": [
        {
            "id": 0,
            "agcontext_name": "cwfid",
            "crop_type": "other",
            "bbch_growth_range": [10, 20],
            "soil_colour": "grey",
            "surface_cover": "none",
            "surface_coverage": "0-25",
            "weather_description": "sunny",
            "location_lat": 53,
            "location_long": 11,
            "location_datum": 4326,
            "camera_make": "JAI AD-130GE",
            "camera_lens": "Fujinon TF15-DA-8",
            "camera_lens_focallength": 15,
            "camera_height": 450,
            "camera_angle": 90,
            "camera_fov": 22.6,
            "photography_description": "Mounted on boom",
            "lighting": "natural",
            "cropped_to_plant": False,
        },
        {"id": 1},
    ],
}


def test_annotations():
    stats = WeedCOCOStats(SMALL_WEEDCOCO)
    assert len(stats.annotations) == len(SMALL_WEEDCOCO["annotations"])
    annot2 = stats.annotations.set_index("annotation_id").loc[2]
    assert annot2["image_id"] == 46
    assert annot2["agcontext_id"] == 0
    assert annot2["category_id"] == 1

    assert stats.summary.index.names == ["agcontext_id", "category_id"]
    assert stats.summary.reset_index().to_dict(orient="records") == [
        {"agcontext_id": 0, "category_id": 0, "annotation_count": 2, "image_count": 1},
        {"agcontext_id": 0, "category_id": 1, "annotation_count": 3, "image_count": 2},
        {"agcontext_id": 1, "category_id": 1, "annotation_count": 1, "image_count": 1},
    ]
