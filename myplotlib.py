
def lighten_color(color, amount=1.0):
    """
    Lightens the given color by multiplying (1-luminosity) by the given amount.
    Input can be matplotlib color string, hex string, or RGB tuple.

    Examples:
    >> lighten_color('g', 0.3)
    >> lighten_color('#F034A3', 0.6)
    >> lighten_color((.3,.55,.1), 0.5)
    """
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])


def plot_as_emf(figure, **kwargs):
    import subprocess, os

    inkscape_path = kwargs.get('inkscape', r'C:\Program Files\Inkscape\inkscape.exe')
    filepath = kwargs.get('filename', None)
    print(filepath)
    if filepath is not None:
        path, filename = os.path.split(filepath)
        filename, extension = os.path.splitext(filename)

        svg_filepath = os.path.join(path, filename+'.svg')
        emf_filepath = os.path.join(path, filename+'.emf')

        figure.savefig(svg_filepath, format='svg')

        subprocess.call([inkscape_path, svg_filepath, '--export-emf', emf_filepath])
        os.remove(svg_filepath)

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import numpy as np
    x = np.arange(0, 10, 0.01)
    y = np.sin(x)
    fig = plt.figure()
    plt.plot(x, y)
    plt.xlabel(r'$\alpha$')
    plot_as_emf(fig, filename=r'C:\Users\Administrator\Desktop\emfplot.png')