from sagemaker import get_execution_role
from sagemaker.inputs import CreateModelInput
from sagemaker.model import Model
from sagemaker.session import Session
from sagemaker.workflow.steps import CreateModelStep

from pipeline_cv.xgboost import get_xgboost_image_uri


def _get_model(
    training_instance_type,
    step_train,
):
    model = Model(
        image_uri=get_xgboost_image_uri(training_instance_type),
        model_data=step_train.properties.ModelArtifacts.S3ModelArtifacts,
        sagemaker_session=Session(),
        role=get_execution_role(),
    )

    return model

def get_step_model(
    training_instance_type,
    step_train,
    model_name,
    model_instance_type
):

    model = _get_model(
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
