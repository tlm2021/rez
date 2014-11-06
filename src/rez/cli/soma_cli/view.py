"""
View a profile.
"""


def setup_parser(parser, completions=False):
    parser.add_argument(
        "-t", "--tools", action="store_true",
        help="list tools")
    parser.add_argument(
        "-p", "--packages", action="store_true",
        help="list package requests")
    parser.add_argument(
        "-L", "--lock", action="store_true",
        help="show active lock, if any")
    parser.add_argument(
        "-r", "--removals", action="store_true",
        help="list package or tool removals")
    parser.add_argument(
        "-b", "--brief", action="store_true",
        help="print in brief mode")
    parser.add_argument(
        "-s", "--simple", action="store_true",
        help="print in simple mode (good for diffing)")
    parser.add_argument(
        "-e", "--expanded", action="store_true",
        help="print in expanded mode. This mode dumps the file contents of each "
        "override")
    parser.add_argument(
        "-a", "--all", action="store_true",
        help="shortcut for -tpLrv")
    parser.add_argument(
        "--time", type=str,
        help="ignore profile updates after the given time. Supported formats "
        "are: epoch time (eg 1393014494), or relative time (eg -10s, -5m, "
        "-0.5h, -10d)")
    parser.add_argument(
        "PROFILE",
        help="name of profile to view")


def command(opts, parser, extra_arg_groups=None):
    from rez.util import get_epoch_time_from_str
    from soma.production_config import ProductionConfig

    if opts.all:
        opts.tools = True
        opts.packages = True
        opts.lock = True
        opts.removals = True
        opts.verbose = 1

    time_ = get_epoch_time_from_str(opts.time) if opts.time else None
    pc = ProductionConfig.get_current_config(time_=time_)
    profile = pc.profile(opts.PROFILE)

    if opts.expanded:
        profile.dump(verbose=opts.verbose)
    elif opts.simple:
        profile.print_simple_info()
    else:
        nada = ((opts.packages, opts.tools, opts.lock).count(True) == 0)
        packages = opts.packages or nada

        if opts.brief:
            profile.print_brief_info(packages=packages,
                                     tools=opts.tools,
                                     lock=opts.lock,
                                     verbose=opts.verbose)
        else:
            profile.print_info(packages=packages,
                               tools=opts.tools,
                               lock=opts.lock,
                               removals=opts.removals,
                               verbose=opts.verbose)
