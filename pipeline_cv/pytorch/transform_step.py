from sagemaker.inputs import TransformInput
from sagemaker.transformer import Transformer
from sagemaker.workflow.steps import TransformStep

from pipeline_cv.utils import get_retry_policies

def _get_transformer(
    step_create_model,
    model_instance_type,
    dst_test_path
):

    transformer = Transformer(
        model_name=step_create_model.properties.ModelName,
        instance_type=model_instance_type,
        instance_count=1,
        output_path=dst_test_path
    )

    return transformer


def get_step_transform(
    step_create_model,
    model_instance_type,
    dst_test_path,
    transform_name,
    src_test_path
):

    transformer=_get_transformer(
        step_create_model,
        model_instance_type,
        dst_test_path,
    )


    step_transform = TransformStep(
        name=transform_name,
        transformer=transformer,
        inputs=TransformInput(
            data=src_test_path,
            data_type="S3Prefix",
            content_type="application/x-image",
        ),
        retry_policies=get_retry_policies(),
    )

    return step_transform