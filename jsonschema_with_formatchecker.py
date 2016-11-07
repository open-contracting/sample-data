from jsonschema.cli import *
from jsonschema import FormatChecker


def main(args=sys.argv[1:]):
    sys.exit(run(arguments=parse_args(args=args)))


def run(arguments, stdout=sys.stdout, stderr=sys.stderr):
    error_format = arguments["error_format"]
    validator = arguments["validator"](schema=arguments["schema"], format_checker=FormatChecker()) # add a format_checker here; only line that differs in this function compared to original jsonschema.cli
    errored = False
    for instance in arguments["instances"] or ():
        for error in validator.iter_errors(instance):
            stderr.write(error_format.format(error=error))
            errored = True
    return errored


if __name__ == '__main__':
    main()
