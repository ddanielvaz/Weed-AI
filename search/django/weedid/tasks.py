from __future__ import absolute_import, unicode_literals
import json
from celery import shared_task
from weedcoco.repo.deposit import deposit
from weedcoco.index.indexing import ElasticSearchIndex
from weedcoco.index.thumbnailing import thumbnailing
from weedid.models import Dataset
from weedid.utils import make_upload_entity_fields
from core.settings import THUMBNAILS_DIR, REPOSITORY_DIR, DOWNLOAD_DIR
from pathlib import Path


@shared_task
def submit_upload_task(weedcoco_path, image_dir, upload_id):
    upload_entity = Dataset.objects.get(upload_id=upload_id)
    upload_entity.status = "P"
    upload_entity.status_details = ""

    # Update fields in database
    # XXX: maybe this should be delayed
    with open(weedcoco_path) as f:
        weedcoco = json.load(f)
    for k, v in make_upload_entity_fields(weedcoco).items():
        setattr(upload_entity, k, v)

    upload_entity.save()
    try:
        new_weedcoco_path = deposit(
            Path(weedcoco_path),
            Path(image_dir),
            Path(REPOSITORY_DIR),
            Path(DOWNLOAD_DIR),
            upload_id,
        )
    except Exception as e:
        upload_entity.status = "F"
        upload_entity.status_details = str(e)
        upload_entity.save()
    else:
        update_index_and_thumbnails.delay(new_weedcoco_path, upload_id)


@shared_task
def update_index_and_thumbnails(
    weedcoco_path,
    upload_id,
    thumbnails_dir=THUMBNAILS_DIR,
    repository_dir=REPOSITORY_DIR,
):
    upload_entity = Dataset.objects.get(upload_id=upload_id)
    try:
        es_index = ElasticSearchIndex(
            Path(weedcoco_path),
            Path(thumbnails_dir),
            es_host="elasticsearch",
            es_port=9200,
            upload_id=upload_id,
        )
        es_index.modify_coco()
        es_index.post_to_index()
        thumbnailing(Path(thumbnails_dir), Path(repository_dir))
    except Exception as e:
        upload_entity.status = "F"
        upload_entity.status_details = str(e)
    else:
        upload_entity.status = "C"
        upload_entity.status_details = "It has been successfully uploaded."
    finally:
        upload_entity.save()
