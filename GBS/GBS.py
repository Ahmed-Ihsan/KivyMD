import geocoder

def location():
    g = geocoder.ip('me')
    return g, g.latlng