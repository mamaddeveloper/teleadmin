
def is_type(param_type, param_value, param_name):
    if not isinstance(param_value, param_type):
        raise ValueError("%s is not %s" % (param_name, param_type))
