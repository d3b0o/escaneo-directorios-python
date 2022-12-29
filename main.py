import requests, argparse, time, sys, signal

def def_handler(sig, frame):
    print("\n\n[!] Saliendo... \n")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def parse_numbers(s):
    return [int(number) for number in s.split(",")]

parser = argparse.ArgumentParser()

parser.add_argument("-w", "--wordlist", type=str, required=True, help="Dictionary location")
parser.add_argument("-u", "--url", type=str, required=True, help="Target Url")
parser.add_argument("-s", "--status", type=parse_numbers, default=[], help="Ignored status codes")
parser.add_argument("-c", "--characters", type=parse_numbers, default=[], help="Pages with x characters will not be displayed")

args = parser.parse_args()

wordlist = args.wordlist
url = args.url
invalid_status = args.status
invalid_characters = args.characters

print("\nScan started on {} at {}".format(time.strftime("%d/%m/%y"),time.strftime("%H:%M:%S")))
print("\nTarget: {}".format(url))
print("Wordlist: {}".format(wordlist))

header = "Status \t Char \t Times \t Payload"
print("\n{}\n{}\n{}".format("-" * (len(header) + 2), header, "-" * (len(header) + 2)))

def main(url, wordlist):
    times = 0
    with open(wordlist, "r") as f:
        for word in f:
            times += 1
            mostrar = True
            word = word.strip()

            test_url = url + "/" + word

            response = requests.get(test_url)
            content = response.text


            if response.status_code in invalid_status:
                mostrar = False

            if len(content) in invalid_characters:
                mostrar = False

            if mostrar:
                if response.status_code == 200:
                    print("\033[0;32m{}\033[0m \t \033[0;36m{}\033[0m \t {} \t '/{}'".format(response.status_code, len(content),times, word))
                elif response.status_code == 404:
                    print("\033[0;31m{}\033[0m \t \033[0;36m{}\033[0m \t {} \t '/{}'".format(response.status_code, len(content),times, word))
                else:
                    print("\033[1;33m{}\033[0m \t \033[0;36m{}\033[0m \t {} \t '/{}'".format(response.status_code, len(content),times, word))

if __name__ == "__main__":
    main(url, wordlist)
