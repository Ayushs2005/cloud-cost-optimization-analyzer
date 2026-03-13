import boto3
import datetime

def fetch_cost_data():
    client = boto3.client("ce")

    end = datetime.date.today()
    start = end - datetime.timedelta(days=7)

    response = client.get_cost_and_usage(
        TimePeriod={"Start": str(start), "End": str(end)},
        Granularity="DAILY",
        Metrics=["UnblendedCost"],
        GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}],
    )

    results = []

    for day in response["ResultsByTime"]:
        for group in day["Groups"]:
            service = group["Keys"][0]
            cost = float(group["Metrics"]["UnblendedCost"]["Amount"])

            results.append({
                "service": service,
                "cost": cost,
                "date": day["TimePeriod"]["Start"]
            })

    return results
