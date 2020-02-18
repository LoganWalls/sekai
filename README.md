## Sekai - 世界

Named for the Japanese word 世界 meaning "world", Sekai is a minimalist framework for defining simple grid-world
simulations.

---
### Basic usage
A Sekai simulation has three main components: a `State`, an `Engine`, and a `Renderer`. In addition, a `State` is
populated by `Objects` which represent all of the elements of the simulation that will interact with each other:
(agents, items, goals, environmental features, etc.).

#### States & Objects
To initialize a `State` the only required parameters are the dimensions of the state's grid (`n_rows` and `n_columns`).
While conceptually the state has one grid, a `State` in Sekai actually has two grids: `State.objects` and `State.tiles`.
`State.object`is the "main" grid where most of your objects will live (agents, items, goals, etc.). In Sekai, only one
object can occupy a grid space at a time, so `State.tiles` is provided as a secondary grid to store static environmental
features and other "background" elements which can occupy the same tile as objects.

```python
from sekai import State

state = State(n_columns=10, n_rows=10)
```

You can create objects in Sekai by defining a new class which inherits from the `SekaiObject` class, and the behavior of
the object is specified by overriding two functions: `SekaiObject.tick` and `SekaiObject.collide`.

- `SekaiObject.tick`
    - This function is called once per time-step (per "tick").
    - Has access to the current `State`, as well as the `SekaiObject`'s current `x` and `y` position.
    - Modifies the `State` to reflect the object's behavior at the current time-step.
- `SekaiObject.collide`
    - Is called whenever another object tries to enter this object's position on the grid.
    - Has access to a reference to the colliding object, the current `State`, and this object's current `x` and `y`
    position.
    - Should return a boolean defining whether or not the colliding object should be allowed to pass.
    - Can (optionally) modify the `State`.
 
```python
from sekai import State, SekaiObject

# Define an object
class KitKat(SekaiObject):
    display = "🍫"

    def __init__(self, deliciousness: int = 100):
        self.deliciousness = deliciousness

    def collide(self, other, state: State, x: int, y: int):
        state.reward += self.deliciousness
        return True

# Define a state
state = State(n_columns=10, n_rows=10)

# Place a KitKat into the world.
state.objects[10, 10] = KitKat()
```