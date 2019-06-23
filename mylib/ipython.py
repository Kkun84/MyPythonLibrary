import io
import base64
import IPython


def display_mp4(path, *, height='auto', width='auto'):
    # html = IPython.display.HTML(f'''
    # <video autoplay loop controls>
    # <source src={video}
    # </video>
    height = str(height)
    width = str(width)
    if height[-2:] != 'px' and height[-1] != '%':
        height += 'px'
    if width[-2:] != 'px' and width[-1] != '%':
        width += 'px'
    video = io.open(path, 'r+b').read()
    encoded = base64.b64encode(video)
    html = IPython.display.HTML(f'''
    <video autoplay loop controls style="height:{height}; width:{width}">
    <source src="data:video/mp4;base64,{encoded.decode('ascii')}" type="video/mp4" />
    </video>
    ''')
    IPython.display.display(html)
