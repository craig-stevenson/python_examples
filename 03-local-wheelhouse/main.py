from datetime import date

from dateutil.relativedelta import relativedelta


def main():
    today = date.today()
    print(f"Installed from ./wheels. One month from today is {today + relativedelta(months=1)}.")


if __name__ == "__main__":
    main()
