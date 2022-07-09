from sagemaker import get_execution_role
from sagemaker.estimator import Estimator
from sagemaker.image_uris import retrieve
from sagemaker.session import Session
from sagemaker.inputs import TrainingInput
from sagemaker.workflow.steps import TrainingStep

from pipeline_cv.utils.retry import get_retry_policies


def _get_xgboost_image_uri(
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


def _get_xgboost_estimator(
    training_instance_type,
    hyperparameters,
    model_path
):
    xgb_train = Estimator(
        image_uri=_get_xgboost_image_uri(training_instance_type),
        hyperparameters=hyperparameters,
        instance_type=training_instance_type,
        instance_count=1,
        output_path=model_path,
        role=get_execution_role(),
    )

    return xgb_train


def get_step_train(
    train_name,
    training_instance_type,
    hyperparameters,
    model_path,
    s3_data_path
):

    step_train = TrainingStep(
        name=train_name,
        estimator=_get_xgboost_estimator(
            training_instance_type,
            hyperparameters,
            model_path
        ),
        inputs={
            "train": TrainingInput(
                s3_data=f"{s3_data_path}/train/",
                content_type="text/csv"
            ),
            "validation": TrainingInput(
                s3_data=f"{s3_data_path}/validation/",
                content_type="text/csv"
            )
        },
        retry_policies=get_retry_policies(),
    )

    return step_train