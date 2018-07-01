import matplotlib
import mATLASplotlib

def test_bar_chart():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1], [0.5, 0.5], [5, 10], None, style="bar")
        bars = [c for c in canvas.subplots["main"].get_children() if isinstance(c, matplotlib.patches.Rectangle)]
        # Widths are increased by 0.005 to avoid zero-width gaps
        assert bars[0].get_width() == 1.005
        assert bars[0].get_height() == 5
        assert bars[1].get_width() == 1.005
        assert bars[1].get_height() == 10
