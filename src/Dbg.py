import datetime
import inspect
is_debug = True

def dbg(*args, **kwargs):
    """ Debug Output, print only happens if is_debug is set to true
    """
    if is_debug:
        current_frame = inspect.currentframe()
        caller_frame = current_frame.f_back
        caller_func = caller_frame.f_code.co_name
        class_name = None
        caller_locals = caller_frame.f_locals
        if 'self' in caller_locals:
            class_name = caller_locals['self'].__class__.__name__
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if class_name:
            print(f"[{timestamp}] [{class_name}.{caller_func}]", *args, **kwargs)
        else:
            print(f"[{timestamp}] [{caller_func}]", *args, **kwargs)
            
def dbgassert(condition, message="Assertion failed"):
    if not condition:
        current_frame = inspect.currentframe()
        caller_frame = current_frame.f_back
        
        caller_function = caller_frame.f_code.co_name
        
        class_name = None
        
        caller_locals = caller_frame.f_locals
        
        if 'self' in caller_locals:
            class_name = caller_locals['self'].__class__.__name__
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if class_name:
            print(f"[{timestamp}] [{class_name}.{caller_function}] {message}")
        else:
            print(f"[{timestamp}] [{caller_function}] {message}")