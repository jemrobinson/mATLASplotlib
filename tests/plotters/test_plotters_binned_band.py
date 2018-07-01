import matplotlib
import mATLASplotlib

def test_binned_band():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1, 2], [0.5, 0.5, 0.5], [2, 4, 6], [1, 1, 1], style="binned band")
        polycollections = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.collections.PolyCollection)]
        assert len(polycollections) == 1