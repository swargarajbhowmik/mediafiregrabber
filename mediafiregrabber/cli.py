import argparse
import mediafiregrabber

def download():
    parser = argparse.ArgumentParser(description="Download Mediafire Files.")
    parser.add_argument("url", nargs="+", help="<Mediafire URL>")
    args = parser.parse_args()

    for url in args.url:
        try:
            mediafiregrabber.download(url)
        except:
            print(f"Failed to download from {url}.")

if __name__ == "__main__":
    download()