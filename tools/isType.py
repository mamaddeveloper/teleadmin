
def is_type(param_type, param_value, param_name):
    if not isinstance(param_value, param_type):
        raise ValueError("%s is not %s, it is %s" % (param_name, param_type, type(param_value)))
