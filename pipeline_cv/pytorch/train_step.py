from sagemaker import get_execution_role
from sagemaker.pytorch import PyTorch
from sagemaker.workflow.steps import TrainingStep

from pipeline_cv.utils import get_retry_policies


def _get_pytorch_estimator(
    training_instance_type,
    hyperparameters,
    volume_size,
    dst_model_path
):
    pytorch_estimator = PyTorch(
        entry_point="train.py",
        role=get_execution_role(),
        train_instance_type=training_instance_type,
        train_instance_count=1,
        volume_size = volume_size,
        hyperparameters=hyperparameters,
        framework_version="1.10.2",
        py_version="py3",
        output_path=dst_model_path,
    )

    return pytorch_estimator

def get_step_train(
    train_name,
    training_instance_type,
    hyperparameters,
    dst_model_path,
    src_train_path
):

    step_train = TrainingStep(
        name=train_name,
        estimator=_get_pytorch_estimator(
            training_instance_type,
            hyperparameters,
            dst_model_path
        ),
        inputs={
            "train": f"{src_train_path}/train/",
            "test": f"{src_train_path}/validation/",
        },
        retry_policies=get_retry_policies(),
    )

    return step_train
