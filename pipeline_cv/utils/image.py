from sagemaker.session import Session
from sagemaker.image_uris import retrieve


def get_image_uri(
    framework,
    training_instance_type,
    version
):

    sagemaker_session = Session()

    image_uri = retrieve(
        framework=framework,
        region=sagemaker_session.boto_region_name,
        version=version,
        py_version="py3",
        instance_type=training_instance_type,
    )

    return image_uri