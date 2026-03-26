from DSAStack import DSAStack
from DSAQueue import CircularQueue


class EquationSolver:
    """
    Solves a mathematical equation given in INFIX notation by:
      1. Converting it to POSTFIX notation  (also called Reverse Polish Notation)
      2. Evaluating the postfix expression to get the numeric answer

    THE TWO-STEP PROCESS
    Step 1 — _parse_infix_to_postfix()
        Uses the Shunting-Yard algorithm (invented by Edsger Dijkstra).
        Reads the infix string token by token and reorders tokens into a
        postfix CircularQueue.  A DSAStack is used to temporarily hold
        operators while we work out where they belong in postfix order.

    Step 2 — _evaluate_postfix()
        Reads the postfix queue token by token.
          - If a token is a NUMBER  →  push it onto an operand stack.
          - If a token is an OPERATOR  →  pop two numbers from the stack,
            apply the operation, push the result back.
        After all tokens are processed, the single remaining stack value
        is the final answer.

    Example
        solver = EquationSolver()
        print(solver.solve("3 + 4 * 2"))          # → 11.0
        print(solver.solve("( 3 + 4 ) * 2"))      # → 14.0
        print(solver.solve("10 / 2 - 3"))         # →  2.0
    """

    def solve(self, equation: str) -> float:
        """
        Solve *equation* by:
          1. Convert infix to postfix
          2. Evaluate the postfix expression

        Parameters
            equation :str e.g. "( 3 + 4 ) * 2"
        """
        # Step 1: parse the infix string into a postfix queue of tokens
        postfix_queue = self._parse_infix_to_postfix(equation)

        # Step 2: evaluate that postfix queue to get the numeric answer
        return self._evaluate_postfix(postfix_queue)

    # MANUAL TOKENISER BECASUE WE CANT USE SPLIT 
    def _next_token(self, equation: str, start: int):
        """
        Order ofoperations:
        1. Skip any space characters that appear before the token.
        2. Look at the first non-space character:
             a. If it is an operator (+, -, *, /)
             b. Otherwise it is the start of a number.
        3. Return a tuple: (token_string, new_position)
           The caller stores new_position and passes it in next time
        4. Return value when there are no more tokens
        Return ("", length_of_string) Meaning its complete

        Parameters
        equation : str   The full equation string.
        start    : int   Character index to begin scanning from.
        """
        length = len(equation)

        #  Phase 1: skip leading spaces 
        pos = start
        while pos < length and equation[pos] == " ":
            pos += 1

        # If we ran off the end there are no more tokens
        if pos >= length:
            return ("", length)

        #  Phase 2: classify the first non-space character 
        ch = equation[pos]

        if ch in "+-*/()":
            # Single-character token — operators and parentheses are always
            # exactly one character long.  Advance pos by 1 and return.
            return (ch, pos + 1)

        #  Phase 3: multi-character numeric token 
        # Record where the number starts, then advance until we hit a space
        # or the end of the string.
        token_start = pos
        while pos < length and equation[pos] != " ":
            pos += 1

        # Return the slice between token_start and pos (the number string)
        return (equation[token_start:pos], pos)

    # STEP 1 — INFIX TO POSTFIX  using Shunting-Yard Algorithm

    def _parse_infix_to_postfix(self, equation: str) -> CircularQueue:
        """
        Convert an infix equation string into a postfix CircularQueue.
        Parameters
        equation : str   Space-delimited infix equation.
        Returns
        CircularQueue   Items in postfix order, ready for evaluation.
        """
        # The operator stack temporarily holds operators and '(' while we
        # work out where they belong in the postfix output.
        op_stack = DSAStack()

        # The output queue will contain tokens in postfix order.
        # We use CircularQueue because it gives O(1) enqueue and dequeue.
        postfix_queue = CircularQueue()

        pos = 0
        length = len(equation)

        # - Main token-processing loop --
        while pos < length:

            # Get the next token and advance our position in the string
            token, pos = self._next_token(equation, pos)

            # Sentinel value means we've consumed the whole string
            if token == "":
                break

            # We only ever need to look at the first character to decide
            # what kind of token this is.
            first_char = token[0]

            #  CASE 1: open parenthesis 
            if first_char == "(":
                # Push '(' as a barrier.  It will stop operators in the
                # outer expression from being popped while we handle the
                # sub-expression enclosed by this bracket pair.
                op_stack.push("(")

            #  CASE 2: close parenthesis 
            elif first_char == ")":
                # Pop operators off the stack and send them to the postfix
                # queue until we find the matching '('.
                while (not op_stack.is_empty()) and op_stack.top() != "(":
                    postfix_queue.enqueue(op_stack.pop())

                # If the stack ran empty before we found '(' the brackets
                # are mismatched — the equation is invalid.
                if op_stack.is_empty():
                    raise ValueError("Mismatched parentheses – no matching '('.")

                # Discard the '(' — it does not appear in postfix notation
                op_stack.pop()

            #  CASE 3: operator (+, -, *, /) 
            elif first_char in "+-*/":
                # Stop taking away last val if:
                #   - the stack is empty
                #   - the top is '('  (it's a sub-expression boundary)
                #   - the top has LOWER precedence than the current operator
                while (not op_stack.is_empty() and
                       op_stack.top() != "(" and
                       self._precedence_of(op_stack.top()) >= self._precedence_of(first_char)):
                    postfix_queue.enqueue(op_stack.pop())

                # Now push the current operator — it will stay until a
                # lower/equal-precedence operator or ')' forces it out.
                op_stack.push(first_char)

            #  CASE 4: numeric operand 
            else:
                # Convert the token string to a float and enqueue it
                # directly — operands always go straight to the output.
                try:
                    operand = float(token)
                except ValueError:
                    raise ValueError(
                        f"Unexpected token '{token}' – not a number or operator.")
                postfix_queue.enqueue(operand)

        # - End-of-input: flush remaining operators -
        # Any operators still on the stack belong at the end of the
        # postfix expression.  Pop them all in order.
        while not op_stack.is_empty():
            top = op_stack.pop()
            # If we find a '(' here, there was no matching ')' — error.
            if top == "(":
                raise ValueError("Mismatched parentheses – unclosed '('.")
            postfix_queue.enqueue(top)

        return postfix_queue

    # STEP 2 — EVALUATE POSTFIX
    def _evaluate_postfix(self, postfix_queue: CircularQueue) -> float:
        """
        Evaluate a postfix expression stored in *postfix_queue*.
        
        Scan through the postfix queue one token at a time using a
        single operand stack:

          If the token is a NUMBER  →  push it onto the operand stack.

          If the token is an OPERATOR  →
              Remove the TOP item  → this is the RIGHT-hand operand (op2)
              Remove the NEXT item → this is the LEFT-hand operand  (op1)
              Compute  op1 <operator> op2
              Push the result back onto the stack.


        Parameters
        -
        postfix_queue : CircularQueue
            Queue of tokens in postfix order (floats and single-char strings).

        Returns
        -
        float  — the final computed result.
        """
        # This stack holds operands (numbers) waiting to be consumed
        # by an operator.
        operand_stack = DSAStack()

        # Process every token in the postfix queue from front to rear
        while not postfix_queue.is_empty():
            term = postfix_queue.dequeue()

            if isinstance(term, str):
                # - OPERATOR token -
                # We need exactly two operands to perform a binary operation.
                if operand_stack.get_count() < 2:
                    raise ValueError(
                        "Malformed postfix expression – not enough operands.")

                # Remove in reverse order: top of stack is the RIGHT operand
                op2 = operand_stack.pop()   # right-hand side of the operation
                op1 = operand_stack.pop()   # left-hand side of the operation

                # Perform the arithmetic and push the result back so it can
                # be used as an operand by a later operator.
                result = self._execute_operation(term, op1, op2)
                operand_stack.push(result)

            else:
                # - OPERAND token -
                # It is a numeric value — push it onto the operand stack
                # so it can be picked up when the next operator arrives.
                operand_stack.push(float(term))

        # After processing all tokens exactly ONE value should remain —
        # the final answer.  If there are more (or fewer), the expression
        # was malformed.
        if operand_stack.get_count() != 1:
            raise ValueError(
                "Malformed postfix expression – leftover operands on stack.")

        return operand_stack.pop()

    # ==================================================================
    # HELPER — OPERATOR PRECEDENCE
    # ==================================================================

    def _precedence_of(self, op: str) -> int:
        """
        Return an integer representing how tightly *op* binds its operands.

        WHY PRECEDENCE MATTERS
        -
        In standard arithmetic, multiplication and division bind more
        tightly than addition and subtraction.  "3 + 4 * 2" means
        "3 + (4 * 2)" not "(3 + 4) * 2".

        We encode this by assigning integer levels:
          +  and  -   →  precedence 1  (lower)
          *  and  /   →  precedence 2  (higher)

        During infix-to-postfix conversion, a higher-precedence operator
        on the stack is popped BEFORE a lower-precedence incoming operator
        is pushed.  This ensures higher-priority operations end up earlier
        in the postfix queue and are therefore evaluated first.

        '(' and unknown symbols return 0 so they are never accidentally
        popped by a regular operator.

        We use if/elif instead of a dict or hashmap (both are restricted).

        Parameters
        -
        op : str   A single-character operator string.

        Returns
        -
        int  — 0 (lowest / unknown), 1 (+ -), or 2 (* /)
        """
        if op == "+" or op == "-":
            return 1       # addition and subtraction — lowest precedence
        elif op == "*" or op == "/":
            return 2       # multiplication and division — higher precedence
        else:
            return 0       # '(' or anything unrecognised — treated as lowest

    # ==================================================================
    # HELPER — EXECUTE A BINARY OPERATION
    # ==================================================================

    def _execute_operation(self, op: str, op1: float, op2: float) -> float:
        """
        Apply the binary operator *op* to left operand *op1* and right
        operand *op2*, and return the result.

        OPERAND ORDER
        -
        op1 is the LEFT-hand operand and op2 is the RIGHT-hand operand.
        This matters for subtraction and division:
            op1 - op2  →  "10 - 3" = 7    (correct)
            op2 - op1  →  "3 - 10" = -7   (wrong!)

        DIVISION BY ZERO CHECK
        -
        Dividing by zero is undefined.  We check for it explicitly and
        raise a ZeroDivisionError with a meaningful message rather than
        letting Python produce a cryptic error or infinity value.

        Parameters
        -
        op  : str    Single-character operator: '+', '-', '*', or '/'.
        op1 : float  Left-hand operand.
        op2 : float  Right-hand operand.

        Returns
        -
        float  — the result of op1 <op> op2.

        Raises
        
        ZeroDivisionError  if op is '/' and op2 is 0.
        ValueError         if op is not one of the four supported operators.
        """
        if op == "+":
            return op1 + op2

        elif op == "-":
            # Order matters: op1 is the left side, op2 is the right side
            return op1 - op2

        elif op == "*":
            return op1 * op2

        elif op == "/":
            # Guard against division by zero before performing the operation
            if op2 == 0.0:
                raise ZeroDivisionError("Division by zero in equation.")
            return op1 / op2

        else:
            # This should never happen if _parse_infix_to_postfix is working
            # correctly, but we raise an error just in case.
            raise ValueError(f"Unknown operator '{op}'.")
