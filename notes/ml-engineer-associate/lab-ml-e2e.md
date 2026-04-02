# SageMaker End-to-End Mini Lab (Enhanced, Low-Budget, Exam-Focused)

> Based on the SageMaker feature list you shared, this lab is designed to cover the highest-value SageMaker features for the AWS ML Engineer Associate exam, while staying practical and low-cost.

---

## Goal

Build a small but realistic end-to-end ML workflow in SageMaker that helps you understand:

- where each SageMaker feature fits in the lifecycle
- what to use in real scenarios
- how AWS frames these features in exam questions
- how to keep costs under control

This lab is intentionally designed to be:

- easy to follow
- small enough to finish in one focused session
- broad enough to cover major SageMaker concepts
- cheap enough to stay roughly under **USD $10–$15** if you clean up properly and do not leave resources running

---

## What This Lab Covers

This lab touches the following SageMaker features from your list: Studio, Training Jobs, Processing, Feature Store, Clarify, Debugger, Experiments, Model Registry, Endpoints, Batch Transform, Serverless Inference, Pipelines, Model Monitor, Autopilot, Hyperparameter Tuning, Automatic Model Tuning, Spot Training, Inference Recommender, and the conceptual differences around Async Inference and Multi-Model Endpoints.

---

## Exam Mental Model

Think in this order:

```text
Data -> Prepare -> Train -> Tune -> Explain -> Register -> Deploy -> Monitor -> Improve
```

Map SageMaker features to that lifecycle:

| Lifecycle Stage         | SageMaker Feature                              |
| ----------------------- | ---------------------------------------------- |
| Workspace               | Studio                                         |
| Prepare                 | Processing, Data Wrangler                      |
| Store reusable features | Feature Store                                  |
| Label                   | Ground Truth                                   |
| Train                   | Training Jobs                                  |
| Debug                   | Debugger                                       |
| Track                   | Experiments                                    |
| Tune                    | Hyperparameter Tuning / Automatic Model Tuning |
| Explain / fairness      | Clarify                                        |
| Register                | Model Registry                                 |
| Deploy                  | Endpoints / Serverless / Async / Multi-Model   |
| Batch scoring           | Batch Transform                                |
| Recommend infra         | Inference Recommender                          |
| Monitor                 | Model Monitor                                  |
| Automate                | Pipelines                                      |
| AutoML                  | Autopilot                                      |

---

# Lab Architecture

```text
S3
 └── Raw Data
      └── Processing
           ├── Processed Train/Validation Data
           ├── Feature Store (concept/light)
           └── Clarify / Monitoring artifacts
                └── Training Job
                     ├── Debugger outputs
                     ├── Experiment tracking
                     └── Hyperparameter Tuning
                          └── Best Model
                               ├── Model Registry
                               ├── Serverless Endpoint
                               ├── Batch Transform
                               └── Model Monitor
```

---

# Rough Cost Prediction

This is a **rough estimate only**, not a guarantee. Actual cost depends on region, run duration, instance type, and whether you leave anything running.

## If you run the lab carefully and shut everything down

| Component                          |              Rough Cost |
| ---------------------------------- | ----------------------: |
| Studio usage for a short session   |             $0.50–$2.00 |
| Processing job on small instance   |             $0.30–$1.00 |
| One training job                   |             $0.50–$1.50 |
| Small hyperparameter tuning run    |             $1.50–$4.00 |
| Clarify or monitoring light runs   |             $0.50–$2.00 |
| Batch Transform                    |             $0.20–$0.80 |
| Serverless inference short testing |             $0.10–$0.50 |
| S3 storage / logs                  | very low, usually cents |

## Total realistic rough range

- **Lean path:** about **$4 to $8**
- **Full path with optional extras:** about **$8 to $15**

## Biggest cost risks

| Resource                        | Risk Level | Why                         |
| ------------------------------- | ---------- | --------------------------- |
| Real-time endpoint left running | High       | can keep charging           |
| Studio apps left open           | Medium     | hidden idle cost            |
| Too many tuning jobs            | Medium     | each launches more training |
| Clarify / monitoring large jobs | Medium     | processing-style compute    |
| Large instance types            | High       | fast cost increase          |

## Cost-control rules

- use small instances only
- keep hyperparameter tuning tiny
- use **Serverless Inference**, not a long-lived standard endpoint
- run only one model
- clean up everything at the end
- do optional sections only if you have time and budget

---

# Prerequisites

Before starting, make sure you have:

- an AWS account
- SageMaker Studio access
- permission to run SageMaker jobs
- an execution role for SageMaker
- an S3 bucket or permission to use SageMaker default bucket

---

# Step 1 — Open SageMaker Studio

## What to do

1. Open AWS Console.
2. Search for **Amazon SageMaker AI**.
3. Open **Studio**.
4. Launch a **JupyterLab** space or app.
5. Create a new Python notebook.

## Why this step matters

SageMaker Studio is the main managed development environment for ML work.

## What you learn

- Studio is the central workspace for building ML solutions.
- In the exam, when AWS asks for a unified managed environment for ML development, Studio is usually the answer.

---

# Step 2 — Set Up the Notebook Environment

Run:

```python
!pip -q install sagemaker scikit-learn pandas numpy boto3
```

Then import and initialize:

```python
import os
import json
import time
import boto3
import sagemaker
import pandas as pd
import numpy as np

from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split

session = sagemaker.Session()
region = boto3.Session().region_name
role = sagemaker.get_execution_role()
bucket = session.default_bucket()

prefix = "ml-associate-sagemaker-enhanced-lab"

print("Region:", region)
print("Bucket:", bucket)
print("Role:", role)
```

## What you learn

- SageMaker jobs rely heavily on **S3**.
- The **execution role** is what lets SageMaker access S3 and create jobs.
- This is foundational for almost every SageMaker workflow.

---

# Step 3 — Create a Small Dataset and Upload It to S3

We will use a simple built-in housing dataset so the lab stays easy and fast.

Run:

```python
df = fetch_california_housing(as_frame=True).frame.copy()
df.rename(columns={"MedHouseVal": "target"}, inplace=True)

train_df, temp_df = train_test_split(df, test_size=0.3, random_state=42)
val_df, batch_df = train_test_split(temp_df, test_size=0.5, random_state=42)

os.makedirs("data", exist_ok=True)

train_df.to_csv("data/train_raw.csv", index=False)
val_df.to_csv("data/val_raw.csv", index=False)

batch_input_df = batch_df.drop(columns=["target"]).head(50)
batch_input_df.to_csv("data/batch_input.csv", index=False, header=False)

train_raw_s3 = session.upload_data("data/train_raw.csv", bucket=bucket, key_prefix=f"{prefix}/raw")
val_raw_s3 = session.upload_data("data/val_raw.csv", bucket=bucket, key_prefix=f"{prefix}/raw")
batch_input_s3 = session.upload_data("data/batch_input.csv", bucket=bucket, key_prefix=f"{prefix}/raw")

print(train_raw_s3)
print(val_raw_s3)
print(batch_input_s3)
```

## What you learn

- A clean ML workflow starts with clear dataset separation:
  - training
  - validation
  - inference input

- Many exam questions are easier if you mentally separate these three.

## Rough cost

Negligible.

---

# Step 4 — Run a SageMaker Processing Job

This is for preprocessing and feature engineering, not model training.

Create the preprocessing script:

```python
%%writefile preprocess.py
import os
import pandas as pd
from sklearn.preprocessing import StandardScaler

input_train = "/opt/ml/processing/input/train/train_raw.csv"
input_val = "/opt/ml/processing/input/val/val_raw.csv"

output_train = "/opt/ml/processing/output/train/train.csv"
output_val = "/opt/ml/processing/output/val/val.csv"

train_df = pd.read_csv(input_train)
val_df = pd.read_csv(input_val)

feature_cols = [c for c in train_df.columns if c != "target"]

scaler = StandardScaler()
train_df[feature_cols] = scaler.fit_transform(train_df[feature_cols])
val_df[feature_cols] = scaler.transform(val_df[feature_cols])

train_df = train_df[["target"] + feature_cols]
val_df = val_df[["target"] + feature_cols]

os.makedirs(os.path.dirname(output_train), exist_ok=True)
os.makedirs(os.path.dirname(output_val), exist_ok=True)

train_df.to_csv(output_train, index=False, header=False)
val_df.to_csv(output_val, index=False, header=False)
```

Run the job:

```python
from sagemaker.sklearn.processing import SKLearnProcessor
from sagemaker.processing import ProcessingInput, ProcessingOutput

processor = SKLearnProcessor(
    framework_version="1.2-1",
    role=role,
    instance_type="ml.m5.large",
    instance_count=1,
    sagemaker_session=session
)

processor.run(
    code="preprocess.py",
    inputs=[
        ProcessingInput(source=train_raw_s3, destination="/opt/ml/processing/input/train"),
        ProcessingInput(source=val_raw_s3, destination="/opt/ml/processing/input/val"),
    ],
    outputs=[
        ProcessingOutput(
            source="/opt/ml/processing/output/train",
            destination=f"s3://{bucket}/{prefix}/processed/train"
        ),
        ProcessingOutput(
            source="/opt/ml/processing/output/val",
            destination=f"s3://{bucket}/{prefix}/processed/val"
        ),
    ],
    wait=True,
    logs=True
)
```

## What you learn

- **Processing** is for data prep.
- Exam trap: do not confuse Processing with Training Jobs.
- This is where you would clean, normalize, and engineer features.

## Rough cost

About **$0.30–$1.00**.

---

# Step 5 — Feature Store (Light Conceptual Step)

Feature Store is useful when multiple models or teams reuse features.

Run a light setup example:

```python
from sagemaker.feature_store.feature_group import FeatureGroup

feature_group_name = "house-price-features"

feature_group = FeatureGroup(
    name=feature_group_name,
    sagemaker_session=session
)

print("Feature Group object created:", feature_group_name)
```

## What you learn

- Feature Store is a central place to reuse features.
- Exam clue: “online and offline store” or “reusable features across models.”

## Important note

A full Feature Store setup needs more permissions and supporting services. For this lab, understanding the concept is enough.

## Rough cost

Usually negligible for this light conceptual step.

---

# Step 6 — Training Job with SageMaker Experiments

Now train a built-in XGBoost model and track the run.

Run:

```python
from sagemaker.image_uris import retrieve
from sagemaker.estimator import Estimator
from sagemaker.inputs import TrainingInput
from sagemaker.experiments import Experiment
from sagemaker.experiments.run import Run

processed_train_s3 = f"s3://{bucket}/{prefix}/processed/train"
processed_val_s3 = f"s3://{bucket}/{prefix}/processed/val"

xgb_image = retrieve(
    framework="xgboost",
    region=region,
    version="1.7-1",
    image_scope="training"
)

estimator = Estimator(
    image_uri=xgb_image,
    role=role,
    instance_count=1,
    instance_type="ml.m5.large",
    volume_size=5,
    output_path=f"s3://{bucket}/{prefix}/training-output",
    sagemaker_session=session
)

estimator.set_hyperparameters(
    objective="reg:squarederror",
    num_round=50,
    max_depth=5,
    eta=0.2,
    subsample=0.8,
    min_child_weight=3
)

experiment = Experiment.create(
    experiment_name="house-price-exp",
    sagemaker_session=session
)

with Run(
    experiment_name=experiment.experiment_name,
    run_name="xgb-baseline-run",
    sagemaker_session=session,
):
    estimator.fit(
        {
            "train": TrainingInput(processed_train_s3, content_type="text/csv"),
            "validation": TrainingInput(processed_val_s3, content_type="text/csv"),
        },
        wait=True,
        logs=True
    )
```

## What you learn

- **Training Jobs** run model training on managed infrastructure.
- **Experiments** help track and compare runs.
- Exam clue: if AWS mentions tracking runs, metrics, or model comparisons, think Experiments.

## Rough cost

About **$0.50–$1.50**.

---

# Step 7 — Add Debugger

Debugger helps inspect training behavior.

Run:

```python
from sagemaker.debugger import DebuggerHookConfig

estimator.debugger_hook_config = DebuggerHookConfig(
    s3_output_path=f"s3://{bucket}/{prefix}/debugger-output"
)
```

Then retrain if you want the debugger to capture outputs:

```python
estimator.fit(
    {
        "train": TrainingInput(processed_train_s3, content_type="text/csv"),
        "validation": TrainingInput(processed_val_s3, content_type="text/csv"),
    },
    wait=True,
    logs=True
)
```

## What you learn

- Debugger helps detect training issues such as bad learning behavior.
- Exam clue: “monitor tensors” or “debug training anomalies.”

## Rough cost

Mostly tied to the training job you rerun. Add roughly **$0.50–$1.50** if you rerun.

---

# Step 8 — Hyperparameter Tuning

Keep this intentionally small so the cost stays low.

Run:

```python
from sagemaker.tuner import HyperparameterTuner, IntegerParameter, ContinuousParameter

hyperparameter_ranges = {
    "max_depth": IntegerParameter(3, 6),
    "eta": ContinuousParameter(0.1, 0.3),
    "subsample": ContinuousParameter(0.6, 1.0),
    "min_child_weight": IntegerParameter(1, 6),
}

tuner = HyperparameterTuner(
    estimator=estimator,
    objective_metric_name="validation:rmse",
    hyperparameter_ranges=hyperparameter_ranges,
    objective_type="Minimize",
    max_jobs=3,
    max_parallel_jobs=2
)

tuner.fit(
    {
        "train": TrainingInput(processed_train_s3, content_type="text/csv"),
        "validation": TrainingInput(processed_val_s3, content_type="text/csv"),
    },
    wait=True,
    logs=True
)

best_estimator = tuner.best_estimator()
print(best_estimator.model_data)
```

## What you learn

- SageMaker Hyperparameter Tuning launches multiple training jobs automatically.
- Exam clue: “optimize model performance automatically.”
- “Automatic Model Tuning” and “Hyperparameter Tuning” are closely related in exam wording.

## Rough cost

About **$1.50–$4.00** depending on runtime.

---

# Step 9 — Optional Spot Training Mindset

You may not need to run this in the lab, but you should know it.

Example:

```python
estimator.use_spot_instances = True
estimator.max_wait = 3600
estimator.max_run = 1800
```

## What you learn

- Spot Training reduces cost.
- Tradeoff: jobs can be interrupted.
- Exam clue: “lower cost training acceptable with interruption risk.”

## Rough cost impact

Potentially cheaper than normal training.

---

# Step 10 — Clarify (Concept + Light Setup)

Clarify helps with explainability and bias detection.

Run a light setup:

```python
from sagemaker.clarify import ClarifyProcessor

clarify_processor = ClarifyProcessor(
    role=role,
    instance_count=1,
    instance_type="ml.m5.large",
    sagemaker_session=session
)

print("Clarify processor ready.")
```

## What you learn

- Clarify is for explainability and fairness.
- Exam clue: “SHAP values,” “bias detection,” or “model transparency.”

## Rough cost

A real Clarify processing run may add about **$0.50–$2.00**.

---

# Step 11 — Register the Best Model in Model Registry

Run:

```python
from sagemaker.model import Model
from sagemaker.model_metrics import ModelMetrics, MetricsSource

model = Model(
    image_uri=retrieve("xgboost", region=region, version="1.7-1", image_scope="inference"),
    model_data=best_estimator.model_data,
    role=role,
    sagemaker_session=session,
)

metrics_json = {
    "regression_metrics": {
        "rmse": {"value": 0.0}
    }
}

with open("metrics.json", "w") as f:
    json.dump(metrics_json, f)

metrics_s3 = session.upload_data("metrics.json", bucket=bucket, key_prefix=f"{prefix}/metrics")

model_metrics = ModelMetrics(
    model_statistics=MetricsSource(
        s3_uri=metrics_s3,
        content_type="application/json"
    )
)

model_package = model.register(
    content_types=["text/csv"],
    response_types=["text/csv"],
    inference_instances=["ml.m5.large"],
    transform_instances=["ml.m5.large"],
    model_package_group_name="house-price-lab-model-group",
    approval_status="Approved",
    model_metrics=model_metrics,
    description="House price lab model"
)

print(model_package.model_package_arn)
```

## What you learn

- Model Registry is for versioning and approval workflows.
- Exam clue: “approve/reject models,” “governance,” or “promote to production.”

## Rough cost

Usually low. Mostly storage and metadata related.

---

# Step 12 — Deploy with Serverless Inference

Use serverless to keep cost low.

Run:

```python
from sagemaker.serverless import ServerlessInferenceConfig

serverless_config = ServerlessInferenceConfig(
    memory_size_in_mb=2048,
    max_concurrency=2
)

predictor = best_estimator.deploy(
    serverless_inference_config=serverless_config,
    serializer=sagemaker.serializers.CSVSerializer(),
    deserializer=sagemaker.deserializers.CSVDeserializer()
)

endpoint_name = predictor.endpoint_name
print("Endpoint:", endpoint_name)
```

## What you learn

- Serverless Inference is good for sporadic or light traffic.
- Exam clue: “sporadic traffic,” “lower cost,” “no need to manage infrastructure.”

## Rough cost

Usually about **$0.10–$0.50** for short tests.

---

# Step 13 — Understand Endpoint vs Async vs Multi-Model

You do not need to fully run these for the lab, but you must know them.

## Real-Time Endpoint

Use when:

- low latency matters
- requests are interactive

## Async Inference

Use when:

- payloads are large
- processing takes longer
- response does not need to be immediate

## Multi-Model Endpoint

Use when:

- you have many small models
- cost optimization matters
- one shared endpoint is enough

## What you learn

This is a favorite exam comparison area. The feature table you shared highlights these scenario differences clearly.

---

# Step 14 — Real-Time Inference Test

Run:

```python
sample = batch_input_df.iloc[[0]]
payload = ",".join(map(str, sample.iloc[0].tolist()))

prediction = predictor.predict(payload)
print("Prediction:", prediction)
```

## What you learn

- This is classic real-time inference.
- Endpoint = immediate prediction for apps and services.

## Rough cost

Usually only cents for light testing.

---

# Step 15 — Batch Transform

Run:

```python
transformer = best_estimator.transformer(
    instance_count=1,
    instance_type="ml.m5.large",
    output_path=f"s3://{bucket}/{prefix}/batch-output",
    accept="text/csv",
    assemble_with="Line"
)

transformer.transform(
    data=batch_input_s3,
    content_type="text/csv",
    split_type="Line"
)

transformer.wait()
print("Batch transform completed.")
```

## What you learn

- Batch Transform is for offline or bulk predictions.
- Exam clue: “large dataset prediction,” “not real-time.”

## Rough cost

About **$0.20–$0.80**.

---

# Step 16 — Model Monitor

Set up basic capture and baseline generation.

Run:

```python
from sagemaker.model_monitor import DataCaptureConfig, DefaultModelMonitor
from sagemaker.model_monitor.dataset_format import DatasetFormat

data_capture_config = DataCaptureConfig(
    enable_capture=True,
    sampling_percentage=100,
    destination_s3_uri=f"s3://{bucket}/{prefix}/datacapture"
)
```

Delete and redeploy the endpoint with capture enabled:

```python
predictor.delete_endpoint(delete_endpoint_config=True)

predictor = best_estimator.deploy(
    serverless_inference_config=serverless_config,
    serializer=sagemaker.serializers.CSVSerializer(),
    deserializer=sagemaker.deserializers.CSVDeserializer(),
    data_capture_config=data_capture_config
)
```

Create the monitor:

```python
monitor = DefaultModelMonitor(
    role=role,
    instance_count=1,
    instance_type="ml.m5.large",
    volume_size_in_gb=5,
    max_runtime_in_seconds=1800,
    sagemaker_session=session
)

monitor.suggest_baseline(
    baseline_dataset=f"{processed_val_s3}/val.csv",
    dataset_format=DatasetFormat.csv(header=False),
    output_s3_uri=f"s3://{bucket}/{prefix}/monitor/baseline",
    wait=True,
    logs=True
)
```

Make a few sample requests:

```python
for i in range(5):
    row = batch_input_df.iloc[[i]]
    payload = ",".join(map(str, row.iloc[0].tolist()))
    print(i, predictor.predict(payload))
```

## What you learn

- Model Monitor detects drift and data quality issues.
- It needs a baseline.
- Exam clue: “drift,” “production data quality,” or “monitor deployed models.”

## Rough cost

About **$0.50–$2.00** depending on how much you run.

---

# Step 17 — Pipelines (Light Conceptual Step)

Run:

```python
from sagemaker.workflow.pipeline import Pipeline

pipeline = Pipeline(
    name="house-price-lab-pipeline",
    steps=[]
)

print("Pipeline object created.")
```

## What you learn

- Pipelines automate the ML lifecycle.
- Exam clue: “CI/CD for ML,” “automate end-to-end workflow.”

## Rough cost

Negligible for a simple object creation example.

---

# Step 18 — Optional Autopilot

Only do this if you have time and budget.

Run:

```python
from sagemaker import AutoML

automl = AutoML(
    role=role,
    target_attribute_name="target",
    max_candidates=3,
    sagemaker_session=session
)

automl.fit(train_raw_s3)
```

## What you learn

- Autopilot automates model building and tuning.
- Exam clue: “no ML expertise,” “automatically builds, trains, tunes.”

## Rough cost

Can vary. For a small run, maybe **$1–$5+**.
Skip it if you want to stay safer on budget.

---

# Step 19 — Optional Inference Recommender Mindset

You may not run this, but know the purpose.

## What it does

Inference Recommender helps choose instance types for serving models based on performance and cost needs.

## What you learn

- Exam clue: “best deployment instance for cost/performance balance.”

---

# Step 20 — Full Shutdown and Cleanup

This is the most important operational step.

## Delete endpoint

```python
predictor.delete_endpoint(delete_endpoint_config=True)
```

## Delete models

```python
sm = boto3.client("sagemaker")

for model in sm.list_models()["Models"]:
    name = model["ModelName"]
    if "house-price" in name or prefix in name:
        sm.delete_model(ModelName=name)
        print("Deleted model:", name)
```

## Delete endpoint configs

```python
for cfg in sm.list_endpoint_configs()["EndpointConfigs"]:
    name = cfg["EndpointConfigName"]
    if "house-price" in name or prefix in name:
        sm.delete_endpoint_config(EndpointConfigName=name)
        print("Deleted endpoint config:", name)
```

## Delete model package group manually if needed

Model package groups are often easier to review and delete from the console after the lab.

## Stop Studio apps completely

In SageMaker Studio:

1. Go to running apps.
2. Shut down all notebook or JupyterLab apps.
3. Make sure no kernel is left running.

## Delete S3 lab data

```python
s3 = boto3.resource("s3")
bucket_obj = s3.Bucket(bucket)
bucket_obj.objects.filter(Prefix=prefix).delete()
print("Deleted S3 lab data under prefix:", prefix)
```

## Optional cleanup targets

You may also review and clean:

- experiment artifacts
- debugger outputs
- model monitor outputs
- batch transform outputs
- CloudWatch logs if needed

## What you learn

- Many AWS lab costs come from forgetting to clean up.
- In real engineering work, cleanup is part of the design, not an afterthought.

---

# Final Cost Summary

## Minimal exam-focused run

If you do:

- Processing
- Training
- Small HPO
- Registry
- Serverless test
- Batch Transform
- Light monitoring

Expect about:

**USD $4 to $8**

## Full enhanced run with more extras

If you also do:

- rerun training with Debugger
- Clarify
- Autopilot
- more monitoring

Expect about:

**USD $8 to $15 or a bit more**

## Safer recommendation

If your budget is strict, do this path:

1. Processing
2. Training
3. Tiny HPO
4. Registry
5. Serverless inference
6. Batch Transform
7. Light Model Monitor
8. Cleanup immediately

That gives you the best exam value for the least cost.

---

# Final Exam Trigger Table

| If the question says...                  | Best SageMaker answer                          |
| ---------------------------------------- | ---------------------------------------------- |
| Unified ML development environment       | Studio                                         |
| Clean and transform data before training | Processing                                     |
| Reusable shared features                 | Feature Store                                  |
| Track experiment runs                    | Experiments                                    |
| Debug training behavior                  | Debugger                                       |
| Find best hyperparameters                | Hyperparameter Tuning / Automatic Model Tuning |
| Explain predictions or detect bias       | Clarify                                        |
| Approve and version models               | Model Registry                                 |
| Real-time low-latency inference          | Endpoint                                       |
| Sporadic low-traffic inference           | Serverless Inference                           |
| Large payload or long-running inference  | Async Inference                                |
| Many small models on one endpoint        | Multi-Model Endpoints                          |
| Bulk prediction over files               | Batch Transform                                |
| Detect drift in deployed model data      | Model Monitor                                  |
| Automate ML workflow                     | Pipelines                                      |
| Auto-build models with minimal expertise | Autopilot                                      |
| Lower-cost interruptible training        | Spot Training                                  |
| Choose best inference infra              | Inference Recommender                          |

---

# Final Advice

Do not try to memorize SageMaker feature names in isolation.

Instead, memorize this:

1. where it sits in the lifecycle
2. what problem it solves
3. how AWS phrases that problem in exam questions

That is how you answer quickly and correctly.

---
