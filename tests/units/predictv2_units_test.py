import pytest

from app.utils import predict, predict_nv_model


@pytest.mark.parametrize(
    "features, expected",
    [
        ([1.0, 2.0, 3.0], [3.0, 5.0, 7.0]),
        ([5.0], [11.0]),
        ([0.0, -1.0], [1.0, -1.0]),
    ],
)
def test_predict_nv_model_nominal(features, expected):
    result = predict_nv_model(features)
    assert result == pytest.approx(expected)


def test_predict_nv_model_empty_list_raises_exception():
    with pytest.raises(ValueError):
        predict_nv_model([])


def test_model_v1_is_not_regressed():
    # Le modèle historique doit continuer à appliquer y = 2x.
    assert predict([1.0, 2.0, 3.0]) == pytest.approx([2.0, 4.0, 6.0])