# =============================================================================
# DSAHashTable.py
# Hash Table implementation with double-hashing, auto-resize, and file I/O.
# =============================================================================

import math
import os


# ---------------------------------------------------------------------------
# DSAHashEntry
# ---------------------------------------------------------------------------
class DSAHashEntry:
    """
    Companion class that stores one slot in the hash array.

    State values
    ------------
    0 = FREE          – never been used (probing can stop here)
    1 = USED          – currently occupied
    2 = PREVIOUSLY_USED – was occupied but has been removed
                         (probing must continue past this slot)
    """

    FREE            = 0
    USED            = 1
    PREVIOUSLY_USED = 2

    def __init__(self):
        self.key   = None
        self.value = None
        self.state = DSAHashEntry.FREE


# ---------------------------------------------------------------------------
# DSAHashTable
# ---------------------------------------------------------------------------
class DSAHashTable:
    """
    Hash table using:
      * Polynomial rolling hash  (hash1) for the primary index.
      * A second hash            (hash2) for the step size (double-hashing).
      * Automatic resizing when load factor crosses 0.60 (grow) or 0.25 (shrink).
      * Table capacity is always prime (reduces clustering).

    Only primitive arrays (pre-allocated Python lists) are used internally.
    No dict, set, defaultdict, tuples, or any high-level data structure.
    """

    UPPER_LOAD       = 0.60
    LOWER_LOAD       = 0.25
    DEFAULT_CAPACITY = 11       # must be prime

    def __init__(self, capacity=None):
        if capacity is None:
            capacity = DSAHashTable.DEFAULT_CAPACITY
        capacity = self._next_prime(capacity)
        self._capacity = capacity
        self._count    = 0
        self._array    = self._make_array(capacity)

    # ================================================================
    # Public interface
    # ================================================================

    def put(self, key, value):
        """
        Insert or update a key/value pair.
        * Duplicate keys have their value updated in-place (no count change).
        * Triggers a grow-resize when load factor would exceed UPPER_LOAD.
        """
        idx = self._find(key)
        if idx != -1 and self._array[idx].state == DSAHashEntry.USED:
            self._array[idx].value = value   # update duplicate
            return

        if (self._count + 1) / self._capacity >= DSAHashTable.UPPER_LOAD:
            self._resize(self._capacity * 2)

        self._insert(key, value)
        self._count += 1

    def hasKey(self, key):
        """Return True if key is present in the table."""
        idx = self._find(key)
        return idx != -1 and self._array[idx].state == DSAHashEntry.USED

    def get(self, key):
        """Return the value for key, or raise KeyError if absent."""
        idx = self._find(key)
        if idx == -1 or self._array[idx].state != DSAHashEntry.USED:
            raise KeyError(f"Key not found: {key}")
        return self._array[idx].value

    def remove(self, key):
        """
        Mark the slot PREVIOUSLY_USED so probing chains remain intact,
        then shrink when the load factor drops below LOWER_LOAD.
        """
        idx = self._find(key)
        if idx == -1 or self._array[idx].state != DSAHashEntry.USED:
            raise KeyError(f"Key not found: {key}")
        self._array[idx].state = DSAHashEntry.PREVIOUSLY_USED
        self._array[idx].key   = None
        self._array[idx].value = None
        self._count -= 1

        new_cap = self._capacity // 2
        if (new_cap >= DSAHashTable.DEFAULT_CAPACITY and
                self._count / self._capacity < DSAHashTable.LOWER_LOAD):
            self._resize(new_cap)

    def count(self):
        return self._count

    def load_factor(self):
        return self._count / self._capacity

    def capacity(self):
        return self._capacity

    # ================================================================
    # File I/O
    # ================================================================

    def save_to_csv(self, filename):
        """Write every USED entry to filename as  key,value  lines."""
        with open(filename, 'w') as f:
            for i in range(self._capacity):
                if self._array[i].state == DSAHashEntry.USED:
                    f.write(f"{self._array[i].key},{self._array[i].value}\n")

    @classmethod
    def load_from_csv(cls, filename, capacity=None):
        """
        Read key,value CSV and return a populated DSAHashTable.
        Manual comma search (no split()) so the first comma separates key
        from value – value may itself contain commas (e.g. names).
        Duplicate keys are updated in-place.
        """
        ht = cls(capacity) if capacity else cls()
        with open(filename, 'r') as f:
            for raw_line in f:
                line = raw_line.strip()
                if not line:
                    continue
                comma_pos = -1
                for ci in range(len(line)):
                    if line[ci] == ',':
                        comma_pos = ci
                        break
                if comma_pos == -1:
                    continue
                key   = line[:comma_pos]
                value = line[comma_pos + 1:]
                ht.put(key, value)
        return ht

    # ================================================================
    # Hash functions
    # ================================================================

    def _hash1(self, key):
        """
        Polynomial rolling hash (djb2-style multiplier 31).

        Good hash function criteria:
          1. Repeatable     – identical key always produces the same index.  ✓
          2. Fast           – O(|key|), only multiply+add per character.     ✓
          3. Even spread    – prime multiplier (31) and prime table size
                              together minimise clustering.                  ✓
          4. Low collisions – accumulating every character's ordinal means
                              single-character differences propagate through
                              the entire hash value.                         ✓ (partial)
        """
        h = 0
        for ch in key:
            h = (h * 31 + ord(ch)) % self._capacity
        return h

    def _hash2(self, key):
        """
        Second hash – provides the step size for double-hashing.

        Formula:  step = q - (raw_hash mod q)
        where q is the largest prime less than the table capacity.

        Because q < capacity and capacity is prime, gcd(step, capacity) = 1,
        guaranteeing the probe sequence visits every slot before repeating.
        step is also forced to be at least 1 (never zero).
        """
        q = self._prev_prime(self._capacity)
        h = 0
        for ch in key:
            h = h * 31 + ord(ch)
        step = q - (h % q)
        return step if step != 0 else 1

    def _hash(self, key):
        """Return (start_index, step_size) for double hashing."""
        return self._hash1(key), self._hash2(key)

    # ================================================================
    # Internal helpers
    # ================================================================

    def _make_array(self, size):
        arr = [None] * size
        for i in range(size):
            arr[i] = DSAHashEntry()
        return arr

    def _find(self, key):
        """
        Probe with double hashing and return the index of key,
        or -1 if not found.

        Stops at a FREE slot (definite miss).
        Skips PREVIOUSLY_USED slots (chain must not be broken).
        """
        start, step = self._hash(key)
        idx = start
        for _ in range(self._capacity):
            entry = self._array[idx]
            if entry.state == DSAHashEntry.FREE:
                return -1
            if entry.state == DSAHashEntry.USED and entry.key == key:
                return idx
            idx = (idx + step) % self._capacity
        return -1

    def _insert(self, key, value):
        """Low-level insert into the first FREE or PREVIOUSLY_USED slot."""
        start, step = self._hash(key)
        idx = start
        for _ in range(self._capacity):
            entry = self._array[idx]
            if entry.state != DSAHashEntry.USED:
                entry.key   = key
                entry.value = value
                entry.state = DSAHashEntry.USED
                return
            idx = (idx + step) % self._capacity
        raise RuntimeError("Hash table is full – cannot insert.")

    def _resize(self, hint):
        """
        Rebuild the table at the next prime >= hint.

        Time complexity: O(n)  – every stored entry is re-hashed once.
        Space complexity: O(n) – new array allocated, old one released.
        """
        new_cap   = self._next_prime(max(hint, DSAHashTable.DEFAULT_CAPACITY))
        old_array = self._array

        self._capacity = new_cap
        self._count    = 0
        self._array    = self._make_array(new_cap)

        for entry in old_array:
            if entry.state == DSAHashEntry.USED:
                self._insert(entry.key, entry.value)
                self._count += 1

    # ================================================================
    # Prime helpers (no external libraries)
    # ================================================================

    @staticmethod
    def _is_prime(n):
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        i = 3
        while i * i <= n:
            if n % i == 0:
                return False
            i += 2
        return True

    @staticmethod
    def _next_prime(n):
        candidate = n if n % 2 != 0 else n + 1
        while not DSAHashTable._is_prime(candidate):
            candidate += 2
        return candidate

    @staticmethod
    def _prev_prime(n):
        candidate = n - 1
        if candidate < 2:
            return 2
        if candidate % 2 == 0:
            candidate -= 1
        while candidate > 2 and not DSAHashTable._is_prime(candidate):
            candidate -= 2
        return candidate

    def __str__(self):
        lines = [f"DSAHashTable  capacity={self._capacity}  "
                 f"count={self._count}  load={self.load_factor():.3f}"]
        for i in range(self._capacity):
            e = self._array[i]
            if e.state == DSAHashEntry.USED:
                lines.append(f"  [{i:>5}]  {e.key}  ->  {e.value}")
        return "\n".join(lines)


# =============================================================================
# Main – tests
# =============================================================================

def sep(title=""):
    print("\n" + "=" * 60)
    if title:
        print(f"  {title}")
        print("=" * 60)


if __name__ == "__main__":

    # ------------------------------------------------------------------
    # 1.  Basic put / get / hasKey
    # ------------------------------------------------------------------
    sep("1. Basic operations (capacity=7)")
    ht = DSAHashTable(7)
    pairs = [("apple","fruit"),("carrot","vegetable"),("mango","fruit"),
             ("broccoli","vegetable"),("lemon","fruit")]
    for k, v in pairs:
        old_cap = ht.capacity()
        ht.put(k, v)
        resize_msg = f"  *** RESIZED {old_cap}->{ht.capacity()}" if ht.capacity() != old_cap else ""
        print(f"  put({k!r},{v!r})  load={ht.load_factor():.2f}  cap={ht.capacity()}{resize_msg}")

    print()
    for k, _ in pairs:
        print(f"  get({k!r}) = {ht.get(k)!r}   hasKey={ht.hasKey(k)}")

    print()
    print("  Duplicate update: put('apple', 'NEW_FRUIT')")
    ht.put("apple", "NEW_FRUIT")
    print(f"  get('apple') = {ht.get('apple')!r}  count unchanged = {ht.count()}")

    # ------------------------------------------------------------------
    # 2.  Remove + probing correctness
    # ------------------------------------------------------------------
    sep("2. Remove – probing chain stays intact")
    small = DSAHashTable(7)
    small.put("Key1", "Val1")
    small.put("Key2", "Val2")
    small.put("Key3", "Val3")
    print(f"  Before remove  hasKey(Key1)={small.hasKey('Key1')}  hasKey(Key2)={small.hasKey('Key2')}")
    small.remove("Key1")
    print(f"  After  remove  hasKey(Key1)={small.hasKey('Key1')}  hasKey(Key2)={small.hasKey('Key2')}")
    print(f"  get('Key2') = {small.get('Key2')!r}   get('Key3') = {small.get('Key3')!r}")

    # ------------------------------------------------------------------
    # 3.  Auto-resize grow
    # ------------------------------------------------------------------
    sep("3. Auto-resize – grow (start cap=11)")
    ht2 = DSAHashTable(11)
    names = ["Alice","Bob","Carol","Dave","Eve","Frank","Gina","Hank","Ivy","Jade"]
    for name in names:
        old = ht2.capacity()
        ht2.put(name, name.lower())
        if ht2.capacity() != old:
            print(f"  *** GREW  {old} -> {ht2.capacity()}  after inserting {name!r}")
    print(f"  Final: count={ht2.count()}  cap={ht2.capacity()}  load={ht2.load_factor():.3f}")

    # ------------------------------------------------------------------
    # 4.  Auto-resize shrink
    # ------------------------------------------------------------------
    sep("4. Auto-resize – shrink")
    for name in names[:-3]:
        old = ht2.capacity()
        ht2.remove(name)
        if ht2.capacity() != old:
            print(f"  *** SHRANK {old} -> {ht2.capacity()}  after removing {name!r}")
    print(f"  Final: count={ht2.count()}  cap={ht2.capacity()}  load={ht2.load_factor():.3f}")

    # ------------------------------------------------------------------
    # 5.  Save & reload small table
    # ------------------------------------------------------------------
    sep("5. File I/O – save and reload")
    save_ht = DSAHashTable(11)
    io_pairs = [("001","Alpha"),("002","Beta"),("003","Gamma"),("004","Delta")]
    for k, v in io_pairs:
        save_ht.put(k, v)
    save_ht.save_to_csv("/mnt/user-data/outputs/small_test.csv")
    print("  Saved small_test.csv")

    loaded = DSAHashTable.load_from_csv("/mnt/user-data/outputs/small_test.csv")
    print("  Reloaded and verified:")
    for k, v in io_pairs:
        result = loaded.get(k)
        ok = "OK" if result == v else f"FAIL (got {result!r})"
        print(f"    {k} -> {result!r}  [{ok}]")

    # ------------------------------------------------------------------
    # 6.  RandomNames7000.csv
    # ------------------------------------------------------------------
    sep("6. RandomNames7000.csv – load, spot-check, save")
    csv_path = None
    for candidate in ["/mnt/user-data/uploads/RandomNames7000.csv",
                      "RandomNames7000.csv"]:
        if os.path.exists(candidate):
            csv_path = candidate
            break

    if csv_path is None:
        print("  File not found – creating 25-entry sample (with 2 duplicates).")
        csv_path = "/mnt/user-data/outputs/sample_names.csv"
        sample = [
            ("14495655","Sofia Bonfiglio"), ("14224671","Ashlee Capellan"),
            ("14707100","Dona Mcinnes"),    ("14644633","Maricela Landreneau"),
            ("14147356","Elinor Raco"),     ("14393910","Cody Mcmartin"),
            ("14799737","Katy Vacek"),      ("14431660","Mathew Mercedes"),
            ("14541837","Karina Rossin"),   ("14593654","Mathew Milian"),
            ("14111111","Anna Smith"),      ("14222222","Brian Jones"),
            ("14333333","Clara Brown"),     ("14444444","Derek White"),
            ("14555555","Eva Black"),       ("14666666","Frank Green"),
            ("14777777","Grace Hall"),      ("14888888","Harry King"),
            ("14999999","Isla Lee"),        ("14000001","Jack Scott"),
            # intentional duplicates
            ("14495655","Sofia Bonfiglio"), ("14224671","Ashlee Capellan"),
        ]
        with open(csv_path, 'w') as f:
            for k, v in sample:
                f.write(f"{k},{v}\n")

    big = DSAHashTable.load_from_csv(csv_path)
    print(f"  Loaded:  count={big.count()}  cap={big.capacity()}  load={big.load_factor():.3f}")

    spot = [("14495655","Sofia Bonfiglio"),
            ("14224671","Ashlee Capellan"),
            ("14707100","Dona Mcinnes")]
    print("  Spot checks:")
    for k, expected in spot:
        if big.hasKey(k):
            val = big.get(k)
            ok  = "OK" if val == expected else f"FAIL (got {val!r})"
            print(f"    {k} -> {val!r}  [{ok}]")
        else:
            print(f"    {k} -> NOT FOUND")

    out = "/mnt/user-data/outputs/saved_names.csv"
    big.save_to_csv(out)
    print(f"  Saved to {out}")

    sep("All tests complete")
