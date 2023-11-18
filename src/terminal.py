import colorama;
import sys;

class Terminal:
	@staticmethod
	def commitTypes ():
		commit_types = {
			1: { 'emoji': ':sparkles:', 'type': 'feat', 'txt': "Features" },
			2: { 'emoji': ':bug:', 'type': 'fix', 'txt': "Bug Fixes" },
			3: { 'emoji': ':books:', 'type': 'docs', 'txt': "Documentation" },
			4: { 'emoji': ':gem:', 'type': 'style', 'txt': "Styles" },
			5: { 'emoji': ':package:', 'type': 'refactor', 'txt': "Code Refactoring" },
			6: { 'emoji': ':racehorse:', 'type': 'perf', 'txt': "Performance Improvements" },
			7: { 'emoji': ':rotating_light:', 'type': 'test', 'txt': "Tests" },
			8: { 'emoji': ':wrench:', 'type': 'build', 'txt': "Builds" },
			9: { 'emoji': ':gear:', 'type': 'ci', 'txt': "Continuous Integrations" },
			10: { 'emoji': ':recycle:', 'type': 'chore', 'txt': "Chores" },
			11: { 'emoji': ':rewind:', 'type': 'revert', 'txt': "Reverts" },
			12: { 'emoji': ':arrow_double_up:', 'type': 'dependencies', 'txt': "Dependencies" },
			13: { 'emoji': ':arrow_double_up:', 'type': 'peerDependencies', 'txt': "Peer dependencies" },
			14: { 'emoji': ':arrow_double_up:', 'type': 'devDependencies', 'txt': "Dev dependencies" },
			15: { 'emoji': ':card_index:', 'type': 'metadata', 'txt': "Metadata" },
			16: { 'emoji': ':bookmark:', 'type': 'version', 'txt': "Version tag" },
			17: { 'emoji': ':lock:', 'type': 'security', 'txt': "Security" },
			18: { 'emoji': ':pencil:', 'type': 'text', 'txt': "Text" },
			19: { 'emoji': ':ambulance:', 'type': 'critical', 'txt': "Critical changes" },
			20: { 'emoji': ':ok_hand:', 'type': 'review', 'txt': "Code review" },
			21: { 'emoji': ':recycle:', 'type': 'review', 'txt': "Content review" },
			22: { 'emoji': ':bricks:', 'type': 'other', 'txt': "Other" },
			23: { 'emoji': '', 'type': 'abort', 'txt': "Abort commit" },
		};

		type = 0;

		print();

		while (type <= 0):
			for key in commit_types.keys():
				print(colorama.Fore.YELLOW, '[', key, ']', colorama.Fore.RESET ,'\t', commit_types[key]['txt']);

			try:
				print();
				type = int(input('[*] Set the commit type' + colorama.Fore.GREEN + ' > ' + colorama.Fore.RESET));
			except:
				type = 0;

		if ( type == 23 ):
			Terminal.success('Commit aborted successfully.');

		return commit_types[type];

	@staticmethod
	def askInput (question: str, max: int = -1, required: bool = True, default: str = None):
		while True:
			message = question;

			if ( default ):
				message += colorama.Fore.YELLOW + ' [' + default + ']' + colorama.Fore.RESET  + colorama.Fore.GREEN + ' > ' + colorama.Fore.RESET;

			response = input(message);

			if ( max < 0 ):
				max = len(response);

			if ( required ) :
				if ( len(response) == 0 and default != None ):
					return default;

				if ( len(response) != 0 and len(response) <= max ):
					return response;

				Terminal.printErr('Unexpected value', 'You need to set an answer...');

				if (len(response) > max):
					Terminal.printErr('Unexpected value', 'Maximum of {m} character(s) limit reached...\n'.format(m=max));
			else:
				if ( default != None ):
					return default;

				return response or "";

	@staticmethod
	def askYN (question: str, default: str = 'yes'):
		valid = {"yes": True, "y": True, "no": False, "n": False};

		if default is None:
			prompt = " [y/n] ";
		elif default == "yes":
			prompt = " [Y/n] ";
		elif default == "no":
			prompt = " [y/N] ";
		else:
			default = 'yes';
			prompt = " [Y/n] ";

		while True:
			choice = input(question + prompt + colorama.Fore.GREEN + '> ' + colorama.Fore.RESET).lower();

			if default is not None and choice == "":
				return valid[default];
			elif choice in valid:
				return valid[choice];
			else:
				Terminal.printErr('Unexpected value', 'Please, ask with: `y`, `n`, `yes` ou `no`.');

	@staticmethod
	def shouldContinue():
		_continue = Terminal.askYN('Do you want to continue?');

		if ( _continue == False ):
			Terminal.success('Operation aborted successfully...');

	@staticmethod
	def err (err = 'Erro', message = 'Something went wrong'):
		Terminal.printErr(err, message);
		sys.exit(2);

	@staticmethod
	def success (message = 'Everything is fine...'):
		Terminal.printSuccess(message);
		sys.exit();

	@staticmethod
	def warning (message = 'Everything is fine...'):
		Terminal.printWarning(message);

	@staticmethod
	def spacing ():
		print("\n");

	@staticmethod
	def printErr (err = 'Erro', message = 'Something went wrong'):
		print(
			colorama.Back.RED
			+ err + ' >'
			+ colorama.Back.RESET
			+ colorama.Fore.RED
			+ ' ' + message
			+ colorama.Fore.RESET
		);

	@staticmethod
	def printSuccess (message = 'Something went wrong'):
		print(colorama.Fore.GREEN + message + colorama.Fore.RESET);

	@staticmethod
	def printWarning (message = 'Something went wrong'):
		print(colorama.Fore.YELLOW + message + colorama.Fore.RESET);
