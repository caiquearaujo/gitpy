import argparse;

def init_args (subparsers: argparse._SubParsersAction):
	subparsers.add_parser('init', help='Initialize a new repository.');
	return subparsers;

def commit_args (subparsers: argparse._SubParsersAction):
	subparsers.add_parser('commit', help='Commit all changes.');
	return subparsers;

def feature_args (subparsers: argparse._SubParsersAction):
	cmd = subparsers.add_parser('feature', help='Create a new feature branch.');
	act = cmd.add_subparsers(dest='action', help='Action to be executed.');

	act.add_parser('create', help='Create a new feature branch.');
	act.add_parser('finish', help='Finish a feature branch.');

	return subparsers;

def hotfix_args (subparsers: argparse._SubParsersAction):
	cmd = subparsers.add_parser('hotfix', help='Create a new hotfix branch.');
	act = cmd.add_subparsers(dest='action', help='Action to be executed.');

	act.add_parser('create', help='Create a new hotfix branch.');
	act.add_parser('finish', help='Finish a hotfix branch.');

	return subparsers;

def perf_args (subparsers: argparse._SubParsersAction):
	cmd = subparsers.add_parser('perf', help='Create a new performance branch.');
	act = cmd.add_subparsers(dest='action', help='Action to be executed.');

	act.add_parser('create', help='Create a new performance branch.');
	act.add_parser('finish', help='Finish a performance branch.');

	return subparsers;

def ping_args (subparsers: argparse._SubParsersAction):
	cmd = subparsers.add_parser('ping', help='See if remote exists.');
	return subparsers;