class _Underscore:
    """Translates _.foo(...) into lambda x: x.foo(...)"""
    
    def __getattr__(self, name):
        return _MethodCaller(name)
    

class _MethodCaller:
    
    def __init__(self, method):
        self.method = method
        
    def __call__(self, *args, **kwargs):
        def call(obj):
            return getattr(obj, self.method)(*args, **kwargs)
        return call
    

_ = _Underscore()
