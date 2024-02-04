import replicate
from replicate.exceptions import ModelError
from replicate.prediction import PredictionCollection, Prediction, Version
from typing import Any, Dict, Optional

class ExtendedPrediction(Prediction):
    id: str
    error: Optional[str]
    input: Optional[Dict[str, Any]]
    logs: Optional[str]
    output: Optional[Any]
    status: str
    version: Optional[Version]
    started_at: Optional[str]
    created_at: Optional[str]
    completed_at: Optional[str]
    metrics: Optional[Dict[str, Any]]

PredictionCollection.model = ExtendedPrediction

def custom_predict(version, **kwargs):
    prediction = version._client.predictions.create(version=version, input=kwargs)
    schema = version.get_transformed_schema()
    output = schema["components"]["schemas"]["Output"]
    if (
        output.get("type") == "array"
        and output.get("x-cog-array-type") == "iterator"
    ):
        return prediction.output_iterator()

    prediction.wait()
    if prediction.status == "failed":
        raise ModelError(prediction.error)
    return prediction

def run_replicate(input):
    model = replicate.models.get("jonbesga/epicrealism-test")
    version = model.versions.get("43731a7cab2d1f14406bc301c1f1e34d18befcbb61702190fcd3041306afcbdb")
    inputs = {
        'prompt': input,
    }
    prediction = custom_predict(version, **inputs)
    return prediction