
def get_png_base64(filename):
    fr = open(filename,'r')
    buf = fr.read()
    return buf
