import matplotlib
from mATLASplotlib import canvases

def test_text():
    canvas = canvases.Simple()
    canvas.plot_dataset([0, 1], [5, 10], style="scatter")
    initial_text_elements = [child for child in canvas.subplots["main"].get_children() if isinstance(child, matplotlib.text.Text)]
    canvas.add_text(0.5, 0.5, "Sample", anchor_to="lower left")
    final_text_elements = [child for child in canvas.subplots["main"].get_children() if isinstance(child, matplotlib.text.Text)]
    # "Sample" label consists of one element: Sample
    assert len(final_text_elements) - len(initial_text_elements) == 1
    assert len([t for t in final_text_elements if t.get_text() == "Sample"]) == 1
    canvas.close()

def test_text_lower_left():
    canvas = canvases.Simple()
    canvas.plot_dataset([0, 1], [5, 10], style="scatter")
    canvas.add_text(0.5, 0.5, "Sample", anchor_to="lower left")
    text_elements = [child for child in canvas.subplots["main"].get_children() if isinstance(child, matplotlib.text.Text)]
    assert [t for t in text_elements if t.get_text() == "Sample"][0].get_ha() == "left"
    assert [t for t in text_elements if t.get_text() == "Sample"][0].get_va() == "bottom"
    # Lower left should position the "Sample" at 0.5, 0.5
    assert [t for t in text_elements if t.get_text() == "Sample"][0].get_position() == (0.5, 0.5)
    canvas.close()

def test_text_lower_right():
    canvas = canvases.Simple()
    canvas.plot_dataset([0, 1], [5, 10], style="scatter")
    canvas.add_text(0.5, 0.5, "Sample", anchor_to="lower right")
    text_elements = [child for child in canvas.subplots["main"].get_children() if isinstance(child, matplotlib.text.Text)]
    assert [t for t in text_elements if t.get_text() == "Sample"][0].get_ha() == "right"
    assert [t for t in text_elements if t.get_text() == "Sample"][0].get_va() == "bottom"
    # Lower right should position the "Sample" at 0.5, 0.5
    assert [t for t in text_elements if t.get_text() == "Sample"][0].get_position() == (0.5, 0.5)
    canvas.close()

def test_text_upper_left():
    canvas = canvases.Simple()
    canvas.plot_dataset([0, 1], [5, 10], style="scatter")
    canvas.add_text(0.5, 0.5, "Sample", anchor_to="upper left")
    text_elements = [child for child in canvas.subplots["main"].get_children() if isinstance(child, matplotlib.text.Text)]
    assert [t for t in text_elements if t.get_text() == "Sample"][0].get_ha() == "left"
    assert [t for t in text_elements if t.get_text() == "Sample"][0].get_va() == "top"
    # Upper left should position the "Sample" at 0.5, 0.5
    assert [t for t in text_elements if t.get_text() == "Sample"][0].get_position() == (0.5, 0.5)
    canvas.close()

def test_text_upper_right():
    canvas = canvases.Simple()
    canvas.plot_dataset([0, 1], [5, 10], style="scatter")
    canvas.add_text(0.5, 0.5, "Sample", anchor_to="upper right")
    text_elements = [child for child in canvas.subplots["main"].get_children() if isinstance(child, matplotlib.text.Text)]
    assert [t for t in text_elements if t.get_text() == "Sample"][0].get_ha() == "right"
    assert [t for t in text_elements if t.get_text() == "Sample"][0].get_va() == "top"
    # Upper right should position the "Sample" at 0.5, 0.5
    assert [t for t in text_elements if t.get_text() == "Sample"][0].get_position() == (0.5, 0.5)
    canvas.close()




