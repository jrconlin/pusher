import json
import sys

from pywebpush import WebPusher
import configargparse


def get_args(sysargs=sys.argv):
    parser = configargparse.ArgumentParser(
        description="builds test data vectors for webpush",
        default_config_files=['config.ini']
    )
    parser.add_argument('-c', '--config',
                        help="config file path",
                        dest="config_file",
                        is_config_file=True)
    parser.add_argument('-s', '--subscription_info',
                        help="subscription info JSON block",
                        dest="sub_info",
                        default="subscription.json")
    parser.add_argument('-d', '--data',
                        help="path of file with data to send",
                        dest="data",
                        default="data")
    parser.add_argument('-o', '--output',
                        help="encrypted data output file path",
                        dest="output",
                        default="encrypted.data")
    parser.add_argument('--send',
                        help="just send the message, don't display it",
                        dest="send",
                        action="store_true",
                        default=False)
    args = parser.parse_args(sysargs)
    return args, parser


def main(sysargs):
    args, parser = get_args(sysargs)
    try:
        sub_info_data = open(args.sub_info)
        data = open(args.data)
        sub_info = json.loads(sub_info_data.read())
        pusher = WebPusher(sub_info)
        if args.send:
            status = pusher.send(data.read())
            print ("Data sent: {}", repr(status))
            return
        result = pusher.encode(data.read())
        out = open(args.output, "wb")
        out.write(result.get('body'))
        out.flush()
        print("""
curl -v -X POST "{url}" \\
-H "crypto-key:keyid=p256dh;dh={pub}" \\
-H "content-encoding:aesgcm" \\
-H "encryption:keyid=p256dh;salt={salt}" \\
-H "ttl:60" \\
--data-binary @{output}
""".format(
            url=sub_info.get('endpoint'),
            pub=result.get('crypto_key'),
            salt=result.get('salt'),
            output=args.output
        ))
    except Exception as e:
        print(repr(e))


if __name__ == '__main__':
    main(sys.argv[1:])
