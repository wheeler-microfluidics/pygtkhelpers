import gtk



class Column(object):
    def __init__(self, attr, type, format="%s"):
        self.attr = attr
        self.type = type

        self.format ="%s"


    #XXX: might be missplaced
    def _data_func(self, column, cell, model, iter):
        obj = model.get_value(iter, 0)
        #XXX allow a callback?
        data = getattr(obj, self.attr)
        #XXX: types
        cell.set_property('text', self.format%data)

    #XXX: might be missplaced
    @property
    def viewcolumn(self):
        title = self.attr.capitalize()
        col = gtk.TreeViewColumn(title)
        #XXX: extend to more types
        cell = gtk.CellRendererText()
        col.pack_start(cell)
        col.set_cell_data_func(cell, self._data_func)
        return col

class ObjectList(gtk.TreeView):

    def __init__(self, columns=(), filtering=False, sorting=False):
        gtk.TreeView.__init__(self)

        self.treeview = gtk.TreeView()
        #XXX: make replacable
        self.model = gtk.ListStore(object)
        self.set_model(self.model)

        self.columns = tuple(columns)
        for col in columns:
            self.append_column(col.viewcolumn)

        self._id_to_iter = {}

    def __len__(self):
        return len(self.model)

    def __contains__(self, item):
        """identity based check of membership"""
        return id(item) in self._id_to_iter

    def __iter__(self):
        for row in self.model:
            yield row[0]

    def __getitem__(self, index):
        return self.model[index][0]

    def append(self, item):
        if id(item) in self._id_to_iter:
            raise ValueError("item %s allready in list"%item )
        modeliter = self.model.append((item,))
        self._id_to_iter[id(item)] = modeliter

    def extend(self, iter):
        for item in iter:
            self.append(item)

    def clear(self):
        self.model.clear()
        self._id_to_iter.clear()
