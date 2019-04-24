import constants

class Feature(object):
    def __init__(self, f):
        self.f = f
    def __call__(self, *args):
        return self.f(*args)
    def __add__(self, r):
        return Feature(lambda *args: self(*args)+r(*args))
    def __radd__(self, r):
        return Feature(lambda *args: r(*args)+self(*args))
    def __mul__(self, r):
        return Feature(lambda *args: self(*args)*r)
    def __rmul__(self, r):
        return Feature(lambda *args: r*self(*args))
    def __pos__(self, r):
        return self
    def __neg__(self):
        return Feature(lambda *args: -self(*args))
    def __sub__(self, r):
        return Feature(lambda *args: self(*args)-r(*args))
    def __rsub__(self, r):
        return Feature(lambda *args: r(*args)-self(*args))

def feature(f):
    return Feature(f)

def speed(s=1.):
    @feature
    def f(t, x, u):
        return (x[3]-s)**2
    return f

def truck_control(s1=1.):
    @feature
    def f(t, x, u):
        return (u[0]/s1)**2
    return f

def control(s1=constants.STEER_REWARD_SCALING, 
        s2=constants.ACCELERATION_REWARD_SCALING):
    """Compute the Gaussian-shaped reward for applying a control.
    Arguments:
    - s1: multiplier for the steering term.
    - s2: multiplier for the acceleration term.
    """
    @feature
    def f(t, x, u):
        return (u[0]*s1)**2 + (u[1]*s2)**2
    return f

def bounded_control(fw, bounds, width=0.05):
    # Arguments:
    # - fw: framework for computation. Either numpy or theano.tensor
    # - bounds: control bounds
    # - width: width of "Gaussian" around control bounds
    @feature
    def f(t, x, u):
        ret=0.
        for i, (a, b) in enumerate(bounds):
            return fw.exp((u[i]-b)/width) + fw.exp((a-u[i])/width)
    return f

if __name__ == '__main__':
    pass
