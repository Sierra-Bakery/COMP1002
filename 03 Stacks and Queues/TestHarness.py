"""
TestHarness.py  –  Manual tests for DSAStack, ShufflingQueue, CircularQueue,
                   and EquationSolver.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from DSAStack import DSAStack
from DSAQueue import ShufflingQueue, CircularQueue
from EquationSolver import EquationSolver


def check(label, actual, expected, tol=1e-9):
    if isinstance(expected, float):
        ok = abs(actual - expected) < tol
    else:
        ok = (actual == expected)
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] {label}")
    if not ok:
        print(f"         expected={expected!r}  got={actual!r}")
    return ok


# ===========================================================================
# 1. DSAStack
print("=" * 60)
print("DSAStack tests")
print("=" * 60)

s = DSAStack(5)
check("new stack is empty",         s.is_empty(),   True)
check("new stack count is 0",       s.get_count(),  0)

s.push(10)
s.push("hello")
s.push(3.14)
check("count after 3 pushes",       s.get_count(),  3)
check("top after 3 pushes",         s.top(),        3.14)
check("is_empty False after pushes",s.is_empty(),   False)

val = s.pop()
check("pop returns top",            val,            3.14)
check("count after pop",            s.get_count(),  2)
check("new top after pop",          s.top(),        "hello")

# Fill to capacity
s2 = DSAStack(3)
s2.push(1); s2.push(2); s2.push(3)
check("full stack is_full",         s2.is_full(),   True)

try:
    s2.push(4)
    print("  [FAIL] push on full stack should raise")
except Exception:
    print("  [PASS] push on full stack raises exception")

# Empty stack pop
s3 = DSAStack()
try:
    s3.pop()
    print("  [FAIL] pop on empty stack should raise")
except Exception:
    print("  [PASS] pop on empty stack raises exception")

# Mixed types (general-purpose Object[] test)
s4 = DSAStack(10)
s4.push(42)
s4.push("text")
s4.push(3.14)
s4.push(True)
check("mixed types – count",        s4.get_count(), 4)
check("mixed types – top",          s4.top(),       True)
s4.pop()
check("mixed types – top after pop",s4.top(),       3.14)


# ===========================================================================
# 2. ShufflingQueue
print()
print("=" * 60)
print("ShufflingQueue tests")
print("=" * 60)

q = ShufflingQueue(5)
check("new queue is empty",         q.is_empty(),   True)

q.enqueue("a"); q.enqueue("b"); q.enqueue("c")
check("count after 3 enqueues",     q.get_count(),  3)
check("peek front",                 q.peek(),       "a")

v = q.dequeue()
check("dequeue returns front",      v,              "a")
check("count after dequeue",        q.get_count(),  2)
check("peek after dequeue",         q.peek(),       "b")

q.enqueue("d"); q.enqueue("e"); q.enqueue("f")
check("count after more enqueues",  q.get_count(),  5)
check("full queue is_full",         q.is_full(),    True)

try:
    q.enqueue("g")
    print("  [FAIL] enqueue on full queue should raise")
except Exception:
    print("  [PASS] enqueue on full queue raises exception")

# Drain and verify FIFO
order = []
while not q.is_empty():
    order.append(q.dequeue())
check("FIFO drain order",           order,          ["b","c","d","e","f"])

try:
    q.dequeue()
    print("  [FAIL] dequeue on empty queue should raise")
except Exception:
    print("  [PASS] dequeue on empty queue raises exception")

# Re-use after full drain
q.enqueue("x"); q.enqueue("y")
check("re-use after drain count",   q.get_count(),  2)
check("re-use after drain peek",    q.peek(),       "x")


# ===========================================================================
# 3. CircularQueue
print()
print("=" * 60)
print("CircularQueue tests")
print("=" * 60)

cq = CircularQueue(4)
check("new circular queue empty",   cq.is_empty(),  True)

cq.enqueue(1); cq.enqueue(2); cq.enqueue(3); cq.enqueue(4)
check("full circular queue",        cq.is_full(),   True)

v = cq.dequeue()
check("dequeue from circular",      v,              1)
check("count after dequeue",        cq.get_count(), 3)

# Wrap-around: rear wraps when enqueue follows dequeue
cq.enqueue(5)
check("count after wrap enqueue",   cq.get_count(), 4)
check("full after wrap",            cq.is_full(),   True)

order2 = []
while not cq.is_empty():
    order2.append(cq.dequeue())
check("FIFO after wrap-around",     order2,         [2, 3, 4, 5])

# Re-use after full drain
cq.enqueue(10); cq.enqueue(20)
check("re-use count",               cq.get_count(), 2)
check("re-use peek",                cq.peek(),      10)

# Multiple wrap-arounds
cq2 = CircularQueue(3)
cq2.enqueue("a"); cq2.enqueue("b"); cq2.enqueue("c")
cq2.dequeue(); cq2.dequeue()          # front advances to index 2
cq2.enqueue("d"); cq2.enqueue("e")   # rear wraps to index 1
order3 = []
while not cq2.is_empty():
    order3.append(cq2.dequeue())
check("multiple wrap-arounds FIFO", order3,         ["c", "d", "e"])


# ===========================================================================
# 4. EquationSolver
print()
print("=" * 60)
print("EquationSolver tests")
print("=" * 60)

solver = EquationSolver()

# Basic single operations
check("3 + 4",                      solver.solve("3 + 4"),                   7.0)
check("10 - 3",                     solver.solve("10 - 3"),                  7.0)
check("3 * 4",                      solver.solve("3 * 4"),                  12.0)
check("10 / 4",                     solver.solve("10 / 4"),                  2.5)

# Precedence: * before +
check("3 + 4 * 2",                  solver.solve("3 + 4 * 2"),              11.0)
check("2 * 3 + 4",                  solver.solve("2 * 3 + 4"),              10.0)

# Parentheses override precedence
check("( 3 + 4 ) * 2",             solver.solve("( 3 + 4 ) * 2"),          14.0)
check("2 * ( 3 + 4 )",             solver.solve("2 * ( 3 + 4 )"),          14.0)

# Left-to-right ordering for same-precedence ops (critical for - and /)
check("10 - 3 - 2",                 solver.solve("10 - 3 - 2"),              5.0)
check("10 / 2 / 5",                 solver.solve("10 / 2 / 5"),              1.0)
check("8 - 3 + 2",                  solver.solve("8 - 3 + 2"),               7.0)

# Nested parentheses
check("( 1 + 2 ) * ( 3 + 4 )",     solver.solve("( 1 + 2 ) * ( 3 + 4 )"), 21.0)
check("( ( 2 + 3 ) * 4 )",         solver.solve("( ( 2 + 3 ) * 4 )"),     20.0)

# Mixed longer expressions
check("2 + 3 * 4 - 1",             solver.solve("2 + 3 * 4 - 1"),          13.0)
check("100 / ( 2 + 3 )",           solver.solve("100 / ( 2 + 3 )"),        20.0)
check("1 + 2 * 3 + 4 * 5",        solver.solve("1 + 2 * 3 + 4 * 5"),      27.0)

# Floating-point operands
check("1.5 + 2.5",                  solver.solve("1.5 + 2.5"),               4.0)
check("0.1 * 10",                   solver.solve("0.1 * 10"),                1.0)
check("7.5 / 2.5",                  solver.solve("7.5 / 2.5"),               3.0)

# Single operand (edge case)
check("42",                         solver.solve("42"),                      42.0)

# Division by zero
try:
    solver.solve("5 / 0")
    print("  [FAIL] divide by zero should raise ZeroDivisionError")
except ZeroDivisionError:
    print("  [PASS] divide by zero raises ZeroDivisionError")

# Mismatched parentheses – unclosed
try:
    solver.solve("( 3 + 4")
    print("  [FAIL] unclosed '(' should raise ValueError")
except ValueError:
    print("  [PASS] unclosed '(' raises ValueError")

# Mismatched parentheses – no opening paren
try:
    solver.solve("3 + 4 )")
    print("  [FAIL] unmatched ')' should raise ValueError")
except ValueError:
    print("  [PASS] unmatched ')' raises ValueError")

print()
print("All tests complete.")
