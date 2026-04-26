from transformers import pipeline

_classifier = None


def _get_classifier():
    """Lazy-load the zero-shot classifier so startup isn't blocked."""
    global _classifier
    if _classifier is None:
        _classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli"
        )
    return _classifier


def is_agriculture_related(text, threshold=0.55):
    labels = ["agriculture and farming", "other"]
    result = _get_classifier()(text, labels)

    return (
        result["labels"][0] == "agriculture and farming"
        and result["scores"][0] >= threshold
    )
