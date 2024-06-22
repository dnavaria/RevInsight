from app import RevInsightCore
import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        RevInsightCore(fp=sys.argv[1]).run(
            export_fp=sys.argv[2],
        )
    else:
        raise ValueError("Please provide the path to the orders file")

    # RevInsightCore(fp="data/orders.csv").run(
    #     export_fp="data/report.xlsx",
    # )
