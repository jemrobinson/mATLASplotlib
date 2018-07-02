import matplotlib
import pytest
import mATLASplotlib

def test_atlas_text():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1], [5, 10], style="scatter")
        initial_text_elements = [child for child in canvas.subplots["main"].get_children() if isinstance(child, matplotlib.text.Text)]
        canvas.add_ATLAS_label(0.5, 0.5, anchor_to="lower left")
        final_text_elements = [child for child in canvas.subplots["main"].get_children() if isinstance(child, matplotlib.text.Text)]
        # "ATLAS" label consists of one element: ATLAS
        assert len(final_text_elements) - len(initial_text_elements) == 1
        assert len([t for t in final_text_elements if t.get_text() == "ATLAS"]) == 1


def test_atlas_text_internal():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1], [5, 10], style="scatter")
        initial_text_elements = [child for child in canvas.subplots["main"].get_children() if isinstance(child, matplotlib.text.Text)]
        canvas.add_ATLAS_label(0.5, 0.5, plot_type="Internal", anchor_to="lower left")
        final_text_elements = [child for child in canvas.subplots["main"].get_children() if isinstance(child, matplotlib.text.Text)]
        # "ATLAS Internal" label consists of three elements: ATLASI (invisible), ATLAS and Internal
        assert len(final_text_elements) - len(initial_text_elements) == 3
        assert len([t for t in final_text_elements if t.get_text() == "ATLASI"]) == 1
        assert len([t for t in final_text_elements if t.get_text() == "ATLAS"]) == 1
        assert len([t for t in final_text_elements if t.get_text() == "Internal"]) == 1


def test_atlas_text_lower_left():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1], [5, 10], style="scatter")
        canvas.add_ATLAS_label(0.5, 0.5, plot_type="Internal", anchor_to="lower left")
        text_elements = [child for child in canvas.subplots["main"].get_children() if isinstance(child, matplotlib.text.Text)]
        assert [t for t in text_elements if t.get_text() == "ATLAS"][0].get_ha() == "left"
        assert [t for t in text_elements if t.get_text() == "ATLAS"][0].get_va() == "bottom"
        # Lower left should position the "ATLAS" at 0.5, 0.5
        assert [t for t in text_elements if t.get_text() == "ATLAS"][0].get_position() == (0.5, 0.5)


def test_atlas_text_lower_right():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1], [5, 10], style="scatter")
        canvas.add_ATLAS_label(0.5, 0.5, plot_type="Internal", anchor_to="lower right")
        text_elements = [child for child in canvas.subplots["main"].get_children() if isinstance(child, matplotlib.text.Text)]
        assert [t for t in text_elements if t.get_text() == " Internal"][0].get_ha() == "right"
        assert [t for t in text_elements if t.get_text() == " Internal"][0].get_va() == "bottom"
        # Lower right should position the " Internal" at 0.5, 0.5 -- note the spacing
        assert [t for t in text_elements if t.get_text() == " Internal"][0].get_position() == (0.5, 0.5)


def test_atlas_text_upper_left():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1], [5, 10], style="scatter")
        canvas.add_ATLAS_label(0.5, 0.5, plot_type="Internal", anchor_to="upper left")
        text_elements = [child for child in canvas.subplots["main"].get_children() if isinstance(child, matplotlib.text.Text)]
        assert [t for t in text_elements if t.get_text() == "ATLAS"][0].get_ha() == "left"
        assert [t for t in text_elements if t.get_text() == "ATLAS"][0].get_va() == "top"
        # Upper left should position the "ATLAS" at 0.5, 0.5
        assert [t for t in text_elements if t.get_text() == "ATLAS"][0].get_position() == (0.5, 0.5)


def test_atlas_text_upper_right():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1], [5, 10], style="scatter")
        canvas.add_ATLAS_label(0.5, 0.5, plot_type="Internal", anchor_to="upper right")
        text_elements = [child for child in canvas.subplots["main"].get_children() if isinstance(child, matplotlib.text.Text)]
        assert [t for t in text_elements if t.get_text() == " Internal"][0].get_ha() == "right"
        assert [t for t in text_elements if t.get_text() == " Internal"][0].get_va() == "top"
        # Upper right should position the " Internal" at 0.5, 0.5 -- note the spacing
        assert [t for t in text_elements if t.get_text() == " Internal"][0].get_position() == (0.5, 0.5)

def test_atlas_text_incorrect_alignment():
    with mATLASplotlib.canvases.Simple() as canvas:
        canvas.plot_dataset([0, 1], [5, 10], style="scatter")
        with pytest.raises(NotImplementedError):
            mATLASplotlib.decorations.atlas_text.draw_ATLAS_text(canvas.subplots["main"], (0.5, 0.5), ("center", "top"), plot_type="Internal")


def test_atlas_text_renderer():
    if hasattr(matplotlib.backends, "backend_agg"):
        matplotlib.pyplot.switch_backend("agg")
        with mATLASplotlib.canvases.Simple() as canvas:
            canvas.plot_dataset([0, 1], [5, 10], style="scatter")
            canvas.add_ATLAS_label(0.5, 0.5, plot_type="Internal", anchor_to="upper right")
        matplotlib.pyplot.switch_backend("pdf")

