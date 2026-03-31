from bisect import bisect_left

class InterpolatingDoubleTreeMap:
    """Python version of WPILib's InterpolatingDoubleTreeMap (linear interpolation)."""

    def __init__(self):
        self._keys = []
        self._values = []

    def put(self, key: float, value: float):
        """Insert a key-value pair. Keeps keys sorted."""
        i = bisect_left(self._keys, key)
        if i < len(self._keys) and self._keys[i] == key:
            self._values[i] = value
        else:
            self._keys.insert(i, key)
            self._values.insert(i, value)

    def get(self, key: float) -> float:
        """Return value for key; interpolate linearly if key not present."""
        if not self._keys:
            return None
        i = bisect_left(self._keys, key)
        
        # Exact match
        if i < len(self._keys) and self._keys[i] == key:
            return self._values[i]
        
        # Key smaller than smallest
        if i == 0:
            return self._values[0]
        
        # Key larger than largest
        if i == len(self._keys):
            return self._values[-1]
        
        # Interpolate between floor and ceiling
        x0, x1 = self._keys[i-1], self._keys[i]
        y0, y1 = self._values[i-1], self._values[i]
        return y0 + (y1 - y0) * (key - x0) / (x1 - x0)

    def clear(self):
        """Clears the map."""
        self._keys.clear()
        self._values.clear()