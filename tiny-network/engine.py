# A whole neural network, from scratch, in plain Python.
# After Andrej Karpathy's micrograd. No numpy, no torch: just numbers that remember
# where they came from, so they can pass blame backward.
import random, math, json

class Value:
    """One number, plus the gradient: how much the loss would change if this number nudged up."""
    def __init__(self, data, _children=()):
        self.data = data
        self.grad = 0.0
        self._backward = lambda: None
        self._prev = _children

    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other))
        def _backward():
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward
        return out

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other))
        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward
        return out

    def relu(self):
        out = Value(self.data if self.data > 0 else 0.0, (self,))
        def _backward():
            self.grad += (out.data > 0) * out.grad
        out._backward = _backward
        return out

    def backward(self):
        # walk the graph backward and hand each number its share of the blame
        order, seen = [], set()
        def build(v):
            if v not in seen:
                seen.add(v)
                for child in v._prev:
                    build(child)
                order.append(v)
        build(self)
        self.grad = 1.0
        for v in reversed(order):
            v._backward()

    __radd__ = __add__
    __rmul__ = __mul__
    def __neg__(self): return self * -1
    def __sub__(self, other): return self + (-other)


class Neuron:
    def __init__(self, n_in, linear=False):
        self.w = [Value(random.uniform(-1, 1)) for _ in range(n_in)]
        self.b = Value(0.0)
        self.linear = linear
    def __call__(self, x):
        act = sum((wi * xi for wi, xi in zip(self.w, x)), self.b)
        return act if self.linear else act.relu()
    def parameters(self): return self.w + [self.b]


class Layer:
    def __init__(self, n_in, n_out, linear=False):
        self.neurons = [Neuron(n_in, linear) for _ in range(n_out)]
    def __call__(self, x):
        out = [n(x) for n in self.neurons]
        return out[0] if len(out) == 1 else out
    def parameters(self): return [p for n in self.neurons for p in n.parameters()]


class MLP:
    def __init__(self, n_in, hidden):
        sizes = [n_in] + hidden + [1]
        self.layers = [Layer(sizes[i], sizes[i + 1], linear=(i == len(sizes) - 2))
                       for i in range(len(sizes) - 1)]
    def __call__(self, x):
        for layer in self.layers:
            x = layer(x)
        return x
    def parameters(self): return [p for l in self.layers for p in l.parameters()]


# ---------------- training ----------------
model, X, Y = None, [], []

def setup(points_json, hidden_json, seed):
    global model, X, Y
    random.seed(seed)
    pts = json.loads(points_json)
    X = [(p[0], p[1]) for p in pts]
    Y = [p[2] for p in pts]                  # labels are +1 or -1
    model = MLP(2, json.loads(hidden_json))
    return len(model.parameters())

def train_step(lr, batch_size):
    idx = random.sample(range(len(X)), min(batch_size, len(X)))
    scores = [model([Value(X[i][0]), Value(X[i][1])]) for i in idx]
    # "max-margin" loss: zero once a point is on the right side by a margin of 1
    losses = [(1 + -Y[i] * s).relu() for i, s in zip(idx, scores)]
    data_loss = sum(losses) * (1.0 / len(losses))
    reg_loss = 1e-4 * sum(p * p for p in model.parameters())
    loss = data_loss + reg_loss
    for p in model.parameters():
        p.grad = 0.0
    loss.backward()
    for p in model.parameters():
        p.data -= lr * p.grad                 # the entire learning rule
    acc = sum((Y[i] > 0) == (s.data > 0) for i, s in zip(idx, scores)) / len(idx)
    weights = [[[[w.data for w in n.w], n.b.data] for n in l.neurons] for l in model.layers]
    return json.dumps({"loss": loss.data, "acc": acc, "weights": weights})
