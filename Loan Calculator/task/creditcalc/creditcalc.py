import math
import argparse
import sys

parser = argparse.ArgumentParser(description="Loan calculator")

parser.add_argument("--type", type=str, help="Type of payment: annuity or diff")
parser.add_argument("--payment", type=float, help="Monthly payment amount")
parser.add_argument("--principal", type=float, help="Loan principal")
parser.add_argument("--periods", type=int, help="Number of months")
parser.add_argument("--interest", type=float, help="Annual interest rate (without % sign)")

args = parser.parse_args()

if args.type not in ("annuity", "diff"):
    print("Incorrect parameters")
    sys.exit()

if args.interest is None:
    print("Incorrect parameters")
    sys.exit()

params = [args.principal, args.payment, args.periods, args.interest]
if sum(p is not None for p in params) < 3:
    print("Incorrect parameters")
    sys.exit()

if any(p is not None and p < 0 for p in [args.principal, args.payment, args.periods, args.interest]):
    print("Incorrect parameters")
    sys.exit()

if args.type == "diff" and args.payment is not None:
    print("Incorrect parameters")
    sys.exit()

i = args.interest / (12 * 100)

if args.type == "diff":
    total_paid = 0
    for m in range(1, args.periods + 1):
        d = args.principal / args.periods + i * (args.principal - (args.principal * (m - 1) / args.periods))
        payment = math.ceil(d)
        total_paid += payment
        print(f"Month {m}: payment is {payment}")
    print(f"\nOverpayment = {int(total_paid - args.principal)}")

elif args.type == "annuity":

    if args.principal and args.payment and not args.periods:
        n = math.ceil(math.log(args.payment / (args.payment - i * args.principal), 1 + i))
        years, months = divmod(n, 12)
        if years > 0 and months > 0:
            print(f"It will take {years} years and {months} months to repay this loan!")
        elif years > 0:
            print(f"It will take {years} years to repay this loan!")
        else:
            print(f"It will take {months} months to repay this loan!")
        print(f"Overpayment = {int(args.payment * n - args.principal)}")


    elif args.principal and args.periods and not args.payment:
        annuity = math.ceil(args.principal * (i * (1 + i) ** args.periods) / ((1 + i) ** args.periods - 1))
        print(f"Your annuity payment = {annuity}!")
        print(f"Overpayment = {int(annuity * args.periods - args.principal)}")


    elif args.payment and args.periods and not args.principal:
        principal = math.floor(args.payment / ((i * (1 + i) ** args.periods) / ((1 + i) ** args.periods - 1)))
        print(f"Your loan principal = {principal}!")
        print(f"Overpayment = {int(args.payment * args.periods - principal)}")

    else:
        print("Incorrect parameters")
