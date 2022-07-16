from sagemaker import get_execution_role
from sagemaker.estimator import Estimator
from sagemaker.inputs import TrainingInput
from sagemaker.workflow.steps import TrainingStep

from pipeline_cv.utils import get_retry_policies
from pipeline_cv.xgboost import get_xgboost_image_uri


def _get_xgboost_estimator(
    training_instance_type,
    hyperparameters,
    dst_model_path
):
    xgb_train = Estimator(
        image_uri=get_xgboost_image_uri(training_instance_type),
        hyperparameters=hyperparameters,
        instance_type=training_instance_type,
        instance_count=1,
        output_path=dst_model_path,
        role=get_execution_role(),
    )

    return xgb_train


def get_step_train(
    train_name,
    training_instance_type,
    hyperparameters,
    dst_model_path,
    src_train_path
):

    step_train = TrainingStep(
        name=train_name,
        estimator=_get_xgboost_estimator(
            training_instance_type,
            hyperparameters,
            dst_model_path
        ),
        inputs={
            "train": TrainingInput(
                s3_data=f"{src_train_path}/train/",
                content_type="text/csv"
            ),
            "validation": TrainingInput(
                s3_data=f"{src_train_path}/validation/",
                content_type="text/csv"
            )
        },
        retry_policies=get_retry_policies(),
    )

    return step_train