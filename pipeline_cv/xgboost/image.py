from sagemaker.session import Session
from sagemaker.image_uris import retrieve


def get_xgboost_image_uri(
    training_instance_type,
    version="1.2-2"
):

    sagemaker_session = Session()

    image_uri = retrieve(
        framework="xgboost",
        region=sagemaker_session.boto_region_name,
        version=version,
        py_version="py3",
        instance_type=training_instance_type,
    )

    return image_uri