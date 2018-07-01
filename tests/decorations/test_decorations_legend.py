import matplotlib
import mATLASplotlib

def test_legend():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1], [5, 10], style="scatter", label="Test")
        canvas.add_legend(0.5, 0.5)
        legend_element = canvas.subplots["main"].get_legend()
        assert isinstance(legend_element, matplotlib.legend.Legend)
        assert len(legend_element.get_texts()) == 1
        assert [t.get_text() for t in legend_element.get_texts()][0] == "Test"
