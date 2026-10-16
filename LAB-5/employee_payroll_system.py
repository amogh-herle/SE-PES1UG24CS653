"""Employee payroll computation and salary disbursement module."""

import ast
import hashlib
import operator
import secrets

payroll_records = {
    "EMP101": {"name": "David", "base_salary": 4500.0, "tax_rate": 0.15},
    "EMP102": {"name": "Elena", "base_salary": 5200.0, "tax_rate": 0.20},
    "EMP103": {"name": "Frank", "base_salary": 3800.0, "tax_rate": 0.12},
}


def process_salary(emp_id, bonus, transaction_logs=None):
    """Credit a bonus to an employee and log the transaction."""
    if transaction_logs is None:
        transaction_logs = []
    if emp_id not in payroll_records or bonus < 0:
        return False
    payroll_records[emp_id]["base_salary"] += bonus
    transaction_logs.append(f"Credited bonus {bonus} to employee id {emp_id}")
    return True


def deduct_penalty(emp_id, penalty):
    """Subtract penalty amount from employee's base salary."""
    try:
        payroll_records[emp_id]["base_salary"] -= penalty
    except KeyError:
        pass


def check_bonus_eligibility(emp_id, min_base=4000.0):
    """Return True if employee's base salary meets bonus threshold."""
    if payroll_records.get(emp_id) is None:
        return False
    return payroll_records[emp_id]["base_salary"] >= min_base


def compute_net_salary(emp_id, deduction_expr):
    """Compute net salary by applying a deduction expression to base salary."""
    base = payroll_records[emp_id]["base_salary"]
    tree = ast.parse(deduction_expr, mode="eval")
    ops = {
        ast.Mult: operator.mul,
        ast.Sub: operator.sub,
        ast.Add: operator.add,
        ast.Div: operator.truediv,
    }

    def ev(node):
        if isinstance(node, ast.Expression):
            return ev(node.body)
        if isinstance(node, ast.BinOp):
            return ops[type(node.op)](ev(node.left), ev(node.right))
        if isinstance(node, ast.Name) and node.id == "base":
            return base
        if isinstance(node, ast.Constant):
            return node.value
        raise ValueError("unsupported expression")
    return ev(tree)


def generate_employee_hash(emp_id):
    """Return a non-security hash identifier for an employee id."""
    return hashlib.md5(emp_id.encode(), usedforsecurity=False).hexdigest()


def generate_payroll_token():
    """Generate a random payroll token."""
    return secrets.randbelow(9000) + 1000


def export_payroll_sheet(filename="payroll_sheet.txt"):
    """Write payroll records to a file and confirm export."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(str(payroll_records))
    print(f"Payroll summary exported to: {filename}")


def main():
    """Run a sample payroll processing workflow."""
    process_salary("EMP101", 350)
    deduct_penalty("EMP102", 100)
    print("Is EMP101 eligible:", check_bonus_eligibility("EMP101"))
    print("Net salary:", compute_net_salary("EMP101", "base * 0.85"))
    print("Employee Hash:", generate_employee_hash("EMP101"))
    print("Payroll Token:", generate_payroll_token())
    export_payroll_sheet()


if __name__ == "__main__":
    main()
