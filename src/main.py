import requests
import argparse

from config import Config
from too.crawler import GovTooCrawler

# requests.adapters.DEFAULT_RETRIES=50

parser = argparse.ArgumentParser()

parser.add_argument(
    "-c",
    "--config",
    required = True
)


def main() -> None:
    args = parser.parse_args()
    cfg = Config(args.config)

    gov_url = f"{cfg.gov_url}?{cfg.gov_url_vote_endpoint}"

    gtc = GovTooCrawler(cfg)

    for g in gtc:
        print(g)

if __name__ == "__main__":
    main()