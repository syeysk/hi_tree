def populate_kwargs_by_date(kwargs, field, date):
    if date:
        parts = date.split('-')
        kwargs[f'{field}_year'] = int(parts[0]) if parts[0] != '????' else None
        kwargs[f'{field}_month'] = int(parts[1]) if parts[1] != '??' else None
        kwargs[f'{field}_day'] = int(parts[2]) if parts[2] != '??' else None


def populate_kwargs_by_part_date(kwargs, arg_options):
    for kind in ['start', 'end']:
        for part in ['year', 'month', 'day']:
            value = arg_options[f'{kind[0]}{part}']
            if value:
                kwargs[f'{kind}_{part}'] = value


def add_date_args_to_parser(parser):
    parser.add_argument('--sdate', nargs='?', type=str, required=False)
    parser.add_argument('--edate', nargs='?', type=str, required=False)
    parser.add_argument('--syear', nargs='?', type=int, required=False)
    parser.add_argument('--smonth', nargs='?', type=int, required=False)
    parser.add_argument('--sday', nargs='?', type=int, required=False)
    parser.add_argument('--eyear', nargs='?', type=int, required=False)
    parser.add_argument('--emonth', nargs='?', type=int, required=False)
    parser.add_argument('--eday', nargs='?', type=int, required=False) 