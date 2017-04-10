#! /usr/bin/env python
from mATLASplotlib import canvases
import ROOT
import numpy as np

# Generate some ROOT data - MC prediction
hpx_MC = ROOT.TH1F("hpx_MC", "This is the MC px distribution", 40, -4, 4)
for x in np.random.normal(size=50000):
    hpx_MC.Fill(x, 0.2)

# Generate some ROOT data - data
hpx_data = ROOT.TH1F("hpx_data", "This is the data px distribution", 40, -4, 4)
for x in np.random.normal(size=10000):
    hpx_data.Fill(x)
print "Data integral, max", hpx_data.Integral(), hpx_data.GetMaximum()

# Generate some ROOT data - fit to data
fit_fn = ROOT.TF1("fit_fn", "gaus", -4, 4)
hpx_data.Fit(fit_fn, "LEMN")
mu, sigma = fit_fn.GetParameter(1), fit_fn.GetParameter(2)
mu_err, sigma_err = fit_fn.GetParError(1), fit_fn.GetParError(2)

# OK, now we're ready to use mATLASplotlib
# Let's start by opening a canvas
canvas = canvases.Simple(shape="rectangular")
# We'll plot some datasets on it
canvas.plot_dataset(hpx_data, style="scatter yerror", label="Data 2009", colour="black")
canvas.plot_dataset(hpx_MC, style="bar", label="Non-diffractive minimum bias", colour="gold")
canvas.plot_dataset(fit_fn, style="smooth line", label="Gaussian fit", colour="red")
# Let's add a legend (automatically generated from the 'label' arguments above)
canvas.add_legend(0.05, 0.96, fontsize="large", anchor_to="upper left")
# ... and some text with details of the fit
canvas.add_text(0.05, 0.7, "$\mu = ({{{0:.2f}}}\pm{{{1:.2f}}})\,$ GeV\n$\sigma = ({{{0:.2f}}}\pm{{{1:.2f}}})\,$ GeV".format(mu, mu_err, sigma, sigma_err))
# Now an ATLAS label on the right hand side
canvas.add_ATLAS_label(0.95, 0.96, plot_type="Preliminary", anchor_to="upper right")
# ... and a sqrts label with no luminosity stated
canvas.add_luminosity_label(0.95, 0.90, sqrts_TeV=0.9, luminosity=None, anchor_to="upper right")
# Set the axis titles
canvas.set_axis_label("x", "$p_x$ [GeV]")
canvas.set_axis_label("y", "Events / 0.2 GeV")
# ... and ranges (optional, since matplotlib is very good at picking appropriate ranges)
canvas.set_axis_range("x", (-5.0, 5.0))
canvas.set_axis_range("y", (0, 1200))
# Finally save to a file (.pdf will be used by default)
canvas.save_to_file("example_fig_01")
