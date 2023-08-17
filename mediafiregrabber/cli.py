import argparse
import mediafiregrabber

def download():
    parser = argparse.ArgumentParser(description="Download Mediafire Folders/Files.")
    parser.add_argument("url", nargs="+", help="<Mediafire URL>")
    parser.add_argument("--path", default=None, help="path to save downloaded file(s)")
    args = parser.parse_args()
    if args.path:
        save = args.path
    else:
        save = "./"
    for url in args.url:
        try:
            mediafiregrabber.download(url, save=save)
        except Exception as e:
            print(f"Failed to download from {e}.")

if __name__ == "__main__":
    download()