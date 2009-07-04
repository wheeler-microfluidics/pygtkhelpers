import gtk
from pygtkhelpers.objectlist import ObjectList, Cell, Column





class IconInfo(object):
    def __init__(self, stock_name, name):
        self.stock_name = stock_name
        self.name = name



icons = ObjectList([
    Column(title='Stock Data', cells=[
        Cell('stock_name', gtk.Pixmap, use_stock=True),
        Cell('stock_name', str),
        ]),
    Column('name', str, 'Name'),
    ])

for id in gtk.stock_list_ids():
    lookup = gtk.stock_lookup(id)
    if lookup is None:
        continue
    stock_name, name = gtk.stock_lookup(id)[:2]
    name = name.replace('_', '')
    icons.append(IconInfo(stock_name, name))

scroll = gtk.ScrolledWindow()
scroll.add(icons)

win = gtk.Window()
win.add(scroll)

win.show_all()
win.connect('destroy', gtk.main_quit)
gtk.main()
