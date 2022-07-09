from sagemaker.inputs import TransformInput
from sagemaker.transformer import Transformer
from sagemaker.workflow.steps import TransformStep

from pipeline_cv.utils import get_retry_policies

def _get_transformer(
    step_create_model,
    model_instance_type,
    transform_path
):

    transformer = Transformer(
        model_name=step_create_model.properties.ModelName,
        instance_type=model_instance_type,
        instance_count=1,
        assemble_with="Line",
        output_path=transform_path
    )

    return transformer


def get_step_transform(
    step_create_model,
    model_instance_type,
    transform_path,
    transform_name,
    s3_batch_path
):

    transformer=_get_transformer(
        step_create_model,
        model_instance_type,
        transform_path,
    )


    step_transform = TransformStep(
        name=transform_name,
        transformer=transformer,
        inputs=TransformInput(
            data=s3_batch_path,
            content_type="csv",
            split_type="Line",
        ),
        retry_policies=get_retry_policies(),
    )

    return step_transform