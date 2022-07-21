from sagemaker import get_execution_role
from sagemaker.inputs import CreateModelInput
from sagemaker.model import Model
from sagemaker.session import Session
from sagemaker.workflow.steps import CreateModelStep

from pipeline_cv.utils import get_image_uri


def _get_model(
    entry_point,
    training_instance_type,
    step_train,
):
    image_uri = get_image_uri(
            "pytorch",
            training_instance_type,
            "1.8.1"
    )

    model = Model(
        image_uri=image_uri,
        model_data=step_train.properties.ModelArtifacts.S3ModelArtifacts,
        sagemaker_session=Session(),
        role=get_execution_role(),
        entry_point=entry_point
    )

    return model

def get_step_model(
    entry_point,
    training_instance_type,
    step_train,
    model_name,
    model_instance_type
):
    model = _get_model(
        entry_point,
        training_instance_type,
        step_train
    )
    
    inputs = CreateModelInput(
        instance_type=model_instance_type,
    )

    step_create_model = CreateModelStep(
        name=model_name,
        model=model,
        inputs=inputs,
    )

    return step_create_model
