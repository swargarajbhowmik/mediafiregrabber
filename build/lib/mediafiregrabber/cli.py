import argparse
import mediafiregrabber

def download():
    parser = argparse.ArgumentParser(description="Download Mediafire Folders/Files.")
    parser.add_argument("url", nargs="+", help="<Mediafire URL>")
    parser.add_argument("--path", default=None, help="path to save downloaded file(s)")
    args = parser.parse_args()

    for url in args.url:
        try:
            mediafiregrabber.download(url, save=args.path)
        except:
            print(f"Failed to download from {url}.")

if __name__ == "__main__":
    download()