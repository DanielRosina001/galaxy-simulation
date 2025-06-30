import numpy as np
import matplotlib.pyplot as plt
from colour_rendering.colour_system import cs_hdtv as cs, xyz_from_xy
from colour_rendering.led_fit import lam, fit_led_xy, get_led_data, get_led_spec

led_colours=['red', 'green', 'blue']

# Target chromaticity coordinates: Illuminant D65
B_xy = 0.3127, 0.3291
fit_coeffs, led_spec = fit_led_xy(B_xy, True, cs, led_colours)
print(cs.spec_to_xyz(led_spec)[:2], 'approximates', B_xy)
print('with the following coefficients of', led_colours)
print(fit_coeffs)

# Get HTML codes for the target and fitted colours.
led_html = cs.spec_to_rgb(led_spec, out_fmt='html')
B_html = cs.rgb_to_hex(cs.xyz_to_rgb(xyz_from_xy(*B_xy)))
print('HTML code for target colour:', B_html)
print('HTML code for fitted colour:', led_html)

# Plot the total LED spectrum and its component intensities.
fig, ax = plt.subplots()
ax.plot(lam, led_spec, 'k')
Iled = get_led_data(led_colours)
ax.plot(lam, fit_coeffs[0] * Iled[0], c='tab:red')
ax.plot(lam, fit_coeffs[1] * Iled[1], c='tab:green')
ax.plot(lam, fit_coeffs[2] * Iled[2], c='tab:blue')
ax.set_xlabel('$\lambda\;/\mathrm{nm}$')
ax.set_ylabel('Normalized Intensity (arb. units)')
plt.show()