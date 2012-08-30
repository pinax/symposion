class InlineSet(object):
    
    def __init__(self, obj, field, delimiter):
        self.obj = obj
        self.field = field
        self.data = set([x for x in getattr(obj, field).split(delimiter) if x])
        self.delimiter = delimiter
    
    def __iter__(self):
        return iter(self.queryset())
    
    def __len__(self):
        return self.queryset().count()
    
    def queryset(self):
        return self.obj.__class__._default_manager.filter(pk__in=self.data)
    
    def add(self, obj, commit=True):
        """
        Add given room to the set, but check if it can exist
        before adding it.
        """
        self.data.add(obj.pk)
        self._update_model(commit=commit)
    
    def remove(self, obj, commit=True):
        self.data.remove(obj.pk)
        self._update_model(commit=commit)
    
    def _update_model(self, commit=True):
        value = self.delimiter.join([str(x) for x in self.data])
        setattr(self.obj, self.field, value)
        if commit:
            self.obj.save(force_update=True)