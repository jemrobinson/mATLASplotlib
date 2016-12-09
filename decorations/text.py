class Text(object):
    def __init__(self, text):
        self.text = text
        self.default_fontsize = 16

    def draw(self, x, y, axes, ha, va, fontsize):
        axes.text(x, y, self.text, fontsize=[fontsize, self.default_fontsize][fontsize==None], ha=ha, va=va, transform=axes.transAxes)
