import matplotlib
import mATLASplotlib

def test_luminosity_label():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1], [5, 10], style="scatter")
        initial_text_elements = [child for child in canvas.subplots["main"].get_children() if isinstance(child, matplotlib.text.Text)]
        canvas.add_luminosity_label(0.5, 0.5, sqrts_TeV=13, luminosity=36.1, units="fb-1", anchor_to="lower left")
        final_text_elements = [child for child in canvas.subplots["main"].get_children() if isinstance(child, matplotlib.text.Text)]
        assert len(final_text_elements) - len(initial_text_elements) == 1
        luminosity_text = [t for t in final_text_elements if t.get_position() == (0.5, 0.5)][0]
        assert "sqrt" in luminosity_text.get_text()
        assert "13" in luminosity_text.get_text()
        assert "TeV" in luminosity_text.get_text()
        assert "36.1" in luminosity_text.get_text()
