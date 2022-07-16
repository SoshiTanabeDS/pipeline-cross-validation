from pipeline_cv.xgboost import get_step_train
from pipeline_cv.xgboost import get_step_model
from pipeline_cv.xgboost import get_step_transform


def create_steps(
    train_name,
    src_train_path,
    src_test_path,
    dst_model_path,
    dst_test_path,
    training_instance_type,
    model_instance_type,
    hyperparameters,
):

    train_name = train_name.replace("-", "_")
    model_name = train_name.replace("_", "-")
    transform_name = train_name + "_test"

    step_train = get_step_train(
        train_name,
        training_instance_type,
        hyperparameters,
        dst_model_path,
        src_train_path,
    )

    step_create_model = get_step_model(
        training_instance_type,
        step_train,
        model_name,
        model_instance_type
    )

    step_transform = get_step_transform(
        step_create_model,
        model_instance_type,
        dst_test_path,
        transform_name,
        src_test_path
    )

    steps = [
        step_train,
        step_create_model,
        step_transform,
    ]

    return steps
